# Progress

This file is where the high-level progress of this project is tracked,
along with todos and other notes. It is meant as a quick, human-readable
log of what has been explored, what was learned, and what is next —
not a replacement for the detail in the analysis notebooks.

The sections at the top (Open Questions, TODOs) reflect the **current**
state of the work. The Progress Summary table at the bottom is the
**historical** record of what was done over time.

## Open Questions

- [ ] Is the high Sharpe at `delay>=1` a real, short-lived edge or still
      partly an artifact (costs, capacity, regime)?
- [ ] How much does survivorship bias inflate results? The universe is
      built from currently-`TRADING` USDT pairs, so dead/delisted coins
      are excluded — likely flatters reversal strategies. Needs to be
      quantified.
- [ ] Are the flat 20 bps transaction costs realistic for daily
      rebalancing on smaller/illiquid alts?

## TODOs

- [ ] Find crypto baseline to use as beta
    - Ideas: some sort of ETF? Plain UMD? BTC?
- [ ] Find calculate drawdowns and other eval metrics for strats

## Progress Summary

| Date | Commit | Files updated / added / changed | Notes (high-level learnings / summary) |
|---|---|---|---|
| 2026-06-16 | `a8c9b2c` | `README.md` | |
| 2026-06-16 | `ad87eac` | `pyproject.toml`, `__about__.py`, `__init__.py`, `tests/`, `.gitignore`, `README.md` | Set up hatch as the build tool. |
| 2026-06-16 | `aa06beb` | `analysis/20260616__umd_variations.ipynb`, `models.py` | First strategy work: UMD/DMU on monthly cadence (2021-2025). |
| 2026-06-17 | `b55fe30` | `analysis/20260616__umd_variations.ipynb` | |
| 2026-06-17 | `ca58f8f` | `analysis/20260616__umd_variations.ipynb` | Price-only trends seem to cap out around a Sharpe of ~1.0-1.3. |
| 2026-06-20 | `2db8d37` | `bin/build.sh`, `pyproject.toml`, `README.md`, `ClassProject.md`, `.gitignore`, `analysis/20260616__umd_variations.ipynb` | Added build script. |
| 2026-06-20 | `dacdcd9` | `analysis/20260620__explore_volume.ipynb`, `models.py` | Started exploring whether volume influences price. |
| 2026-06-20 | `a4959a0` | `analysis/20260620__explore_volume.ipynb` | Re-ran DMU on monthly data; roughly reproduces the earlier notebook (same shape, slightly lower), giving some confidence the pattern is not just an artifact of how months were split. |
| 2026-06-22 | `58c17a3` | `analysis/20260622__explore_shorter_term_strategies.ipynb` | Shifted thesis: chase higher-Sharpe edges over shorter horizons (that can be turned off when they fade) instead of a 2+ Sharpe over 5 years. Moved to daily cadence (2024-06 to 2026-06). |
| 2026-06-24 | `dcb77c7` | `analysis/20260622__explore_shorter_term_strategies.ipynb`, `strats.py` | Abstracted the parameterized DMU/volume strategy out of the notebook into `strats.py` (`*_v1`). |
| 2026-06-24 | `7f75685` | `analysis/20260622__explore_shorter_term_strategies.ipynb`, `strats.py` | Fixed markdown that wrongly described daily `px` as monthly. Renamed `px_delay_periods` -> `delay_periods` so it gates both the price signal and the volume filter. With/without-delay test: the eye-popping Sharpes (e.g. 10.3 with no delay) collapse with one bar of delay (~2.6) — much of the headline number was unrealistic same-bar timing; a real but short-lived edge remains at `delay>=1`. |