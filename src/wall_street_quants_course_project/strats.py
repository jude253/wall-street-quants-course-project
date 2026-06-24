"""Parameterized DMU (reversal) / momentum strategy helpers.

This file collects strategies that have been abstracted out of the
exploratory analysis notebooks into reusable, importable functions.
Once a strategy looks promising in a notebook, its logic is lifted here
so it can be shared across notebooks and tested in isolation.

The strategies currently in this file are the initial versions
(suffixed ``_v1``).  They are expected to be updated, edited, and
extended over time: as the research evolves, existing strategies may be
refined in place and new parameterizations added as ``_v2``, ``_v3``,
and so on.  Keeping older versions alongside newer ones lets past
results stay reproducible while the approach continues to develop.

The functions below are reusable versions of the exploratory strategy
code first written in
``analysis/20260622__explore_shorter_term_strategies.ipynb``.
They build a cross-sectional, price-neutral weight book from a momentum
signal, optionally filtered by a volume universe and a price-signal
percentile band, then score it on net (post-tcost) returns.

Pipeline
--------

    px ─┐
        ├─ pct_change ─> ret ─> rolling-mean signal ─┐
                                                     ├─> (vol filter) ─┐
    vol ─> rolling-mean rank ─> volume universe ─────┘                │
                                                                      ▼
            (price-signal percentile filter) ─> rank ─> neutralize ─> w
                                                                      │
                              w.shift() * ret ─> gross ─ tcost ─> net_ret

Usage
-----

    from wall_street_quants_course_project.strats import (
        calc_dmu_parameterized_v1,
        plot_dmu_variation_v1,
    )

    # Score a single parameterization.
    _, _, _, _, net_ret = calc_dmu_parameterized_v1(px, vol)

    # Plot the net cumulative return with its Sharpe in the title.
    plot_dmu_variation_v1(px, vol, vol_lower_pct=0.2, vol_upper_pct=0.5)
"""

import numpy as np
import matplotlib.pyplot as plt

from wall_street_quants_course_project.models import (
    PriceFrame,
    LevelFrame,
)


def calc_dmu_parameterized_v1(
    px: PriceFrame,
    vol: LevelFrame,
    px_lower_pct: float = 0.1,
    px_upper_pct: float = 0.9,
    px_ma_periods: int = 12,
    px_delay_periods: int = 1,
    keep_outside_px: bool = True,
    vol_lower_pct: float = 0.1,
    vol_upper_pct: float = 0.9,
    vol_ma_periods: int = 12,
    keep_outside_vol: bool = True,
    use_vol_filter: bool = True,
    tcost_bps: int = 20,
    reversal: bool = True,
) -> tuple:
    """Score a parameterized DMU/momentum strategy on net returns.

    Builds a cross-sectional, price-neutral weight book from a delayed
    rolling-mean return signal, optionally restricted to a volume
    universe and a price-signal percentile band, then returns the
    per-name and aggregate return series after transaction costs.

    Args:
        px: Price levels per symbol (columns) over time (index).
        vol: Traded volume per symbol, aligned to ``px``.
        px_lower_pct: Lower percentile bound for the price-signal filter.
        px_upper_pct: Upper percentile bound for the price-signal filter.
        px_ma_periods: Rolling window length for the return signal.
        px_delay_periods: Periods to delay (shift) the return signal by.
        keep_outside_px: If True, keep names in the tails of the signal
            distribution (outside the band); otherwise keep the middle.
        vol_lower_pct: Lower percentile bound for the volume filter.
        vol_upper_pct: Upper percentile bound for the volume filter.
        vol_ma_periods: Rolling window length for the volume average.
        keep_outside_vol: If True, keep names in the volume tails;
            otherwise keep the middle of the volume distribution.
        use_vol_filter: When False, the volume universe filter is
            skipped entirely.
        tcost_bps: Per-unit-turnover transaction cost in basis points.
        reversal: If True, flip the sign of the weights (DMU/reversal);
            if False, trade the signal directly (momentum).

    Returns:
        Tuple of ``(ret, w, port_contrib_ret, gross_ret, net_ret)`` where
        ``ret`` is per-name returns, ``w`` the price-neutral weights,
        ``port_contrib_ret`` each name's return contribution, and
        ``gross_ret`` / ``net_ret`` the pre- and post-tcost portfolio
        return series.

    Example:
        >>> _, _, _, _, net_ret = calc_dmu_parameterized_v1(px, vol)
        >>> sharpe = net_ret.mean() / net_ret.std() * np.sqrt(365)
    """
    ret = px.copy(deep=True).pct_change(fill_method=None)

    # Momentum signal: delayed moving average of returns.
    signal = (
        ret
        .shift(px_delay_periods)
        .rolling(px_ma_periods - px_delay_periods)
        .mean()
    )

    # Volume universe filter (skipped when use_vol_filter=False).
    if use_vol_filter:
        vol_pct_rank = (
            vol.rolling(vol_ma_periods).mean().rank(axis=1, pct=True)
        )
        if keep_outside_vol:
            in_vol_universe = (
                (vol_pct_rank <= vol_lower_pct)
                | (vol_pct_rank >= vol_upper_pct)
            )
        else:
            in_vol_universe = (
                (vol_pct_rank >= vol_lower_pct)
                & (vol_pct_rank <= vol_upper_pct)
            )
        signal = signal.where(in_vol_universe)

    # Price signal filter: keep outliers or the middle of the signal.
    signal_rank = signal.rank(axis=1, pct=True)
    if keep_outside_px:
        in_px_universe = (
            (signal_rank <= px_lower_pct)
            | (signal_rank >= px_upper_pct)
        )
    else:
        in_px_universe = (
            (signal_rank >= px_lower_pct)
            & (signal_rank <= px_upper_pct)
        )
    signal = signal.where(in_px_universe)

    # Rank, demean, and normalize into a price-neutral weight book.
    w = signal.rank(axis=1)
    w = w.subtract(w.mean(axis=1), axis=0)
    w = w.divide(w.abs().sum(axis=1), axis=0)
    if reversal:
        w = -1 * w

    port_contrib_ret = w.shift() * ret
    gross_ret = port_contrib_ret.sum(axis=1)
    to = (w.fillna(0) - w.shift().fillna(0)).abs().sum(axis=1)
    net_ret = gross_ret - to * tcost_bps * 1e-4

    return (ret, w, port_contrib_ret, gross_ret, net_ret)


def plot_dmu_variation_v1(
    px: PriceFrame,
    vol: LevelFrame,
    px_lower_pct: float = 0.1,
    px_upper_pct: float = 0.9,
    px_ma_periods: int = 12,
    px_delay_periods: int = 1,
    keep_outside_px: bool = True,
    vol_lower_pct: float = 0.1,
    vol_upper_pct: float = 0.9,
    vol_ma_periods: int = 12,
    keep_outside_vol: bool = True,
    use_vol_filter: bool = True,
    tcost_bps: int = 20,
    reversal: bool = True,
) -> None:
    """Plot a single DMU parameterization's net cumulative return.

    Runs :func:`calc_dmu_parameterized_v1` with the given parameters,
    annualizes the Sharpe ratio at ``sqrt(365)`` (daily cadence), and
    draws the net cumulative return curve with the Sharpe in the title.
    All parameters are forwarded verbatim to
    :func:`calc_dmu_parameterized_v1`; see that function for their
    meaning.

    Args:
        px: Price levels per symbol (columns) over time (index).
        vol: Traded volume per symbol, aligned to ``px``.

    Returns:
        None. Renders a matplotlib figure as a side effect.

    Example:
        >>> plot_dmu_variation_v1(
        ...     px, vol, vol_lower_pct=0.2, vol_upper_pct=0.5,
        ...     keep_outside_vol=False,
        ... )
    """
    with plt.rc_context({"font.size": 5}):
        fig, ax = plt.subplots(1, 1, sharex=True, sharey=True)

        (_, _, _, _, net_ret) = calc_dmu_parameterized_v1(
            px,
            vol,
            px_lower_pct=px_lower_pct,
            px_upper_pct=px_upper_pct,
            px_ma_periods=px_ma_periods,
            px_delay_periods=px_delay_periods,
            keep_outside_px=keep_outside_px,
            vol_lower_pct=vol_lower_pct,
            vol_upper_pct=vol_upper_pct,
            vol_ma_periods=vol_ma_periods,
            keep_outside_vol=keep_outside_vol,
            use_vol_filter=use_vol_filter,
            tcost_bps=tcost_bps,
            reversal=reversal,
        )
        sharpe = (net_ret.mean() / net_ret.std()) * np.sqrt(365)
        ax.set_title(f"SR: {sharpe:.2f}", fontsize=5)
        net_ret.cumsum().plot(ax=ax)
