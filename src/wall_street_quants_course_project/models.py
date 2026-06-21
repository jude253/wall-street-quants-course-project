import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series


class LevelFrame(pa.DataFrameModel):
    """Validates a wide-format dataframe of raw numeric levels.

    "Level" refers to the absolute value of a series at a point in time —
    as opposed to a change or return. Any quantity measured in its natural
    units qualifies: asset prices, trading volume, open interest, market
    cap, and so on.

    Columns: any number of float columns (one per asset or series), nullable.
    Index: DatetimeIndex (datetime64[ns]), PeriodIndex[M], or PeriodIndex[Y].

    Subtypes:
        PriceFrame  — columns are asset prices in quote-currency units

    Example (monthly BTC/ETH volume in base units):
                          BTCUSDT      ETHUSDT
        2021-01-01   125430.12   3812044.50
        2021-02-01    98201.77   2940183.21
        2021-03-01   143822.09   4102930.88
    """

    level_value: Series[float] = pa.Field(
        alias=".*", regex=True, nullable=True
    )

    class Config:
        coerce = False  # raises on dtype mismatch instead of silently casting
        strict = False  # allows extra columns beyond what's declared

    @pa.dataframe_check
    def index_is_time_like(cls, df: pd.DataFrame) -> bool:
        return isinstance(df.index, (pd.DatetimeIndex, pd.PeriodIndex))


class PctChangeFrame(pa.DataFrameModel):
    """Validates a wide-format dataframe of period-over-period percent changes.

    Each value is the fractional change from the prior period
    (e.g. 0.05 = +5%). The first row is always NaN — there is no prior
    period to compare against. Any LevelFrame can be differentiated into a
    PctChangeFrame: prices → returns, volume → volume growth rate, etc.

    Columns: any number of float columns (one per asset or series), nullable.
    Index: DatetimeIndex (datetime64[ns]), PeriodIndex[M], or PeriodIndex[Y].

    Subtypes:
        ReturnFrame  — columns are asset price returns

    Example (first row always NaN from pct_change):
                      BTCUSDT   ETHUSDT
        2021-01-01       NaN       NaN
        2021-02-01  -0.21752  -0.22847
        2021-03-01   0.46452   0.39568
    """

    pct_change_value: Series[float] = pa.Field(
        alias=".*", regex=True, nullable=True
    )

    class Config:
        coerce = False  # raises on dtype mismatch instead of silently casting
        strict = False  # allows extra columns beyond what's declared

    @pa.dataframe_check
    def index_is_time_like(cls, df: pd.DataFrame) -> bool:
        return isinstance(df.index, (pd.DatetimeIndex, pd.PeriodIndex))


class PriceFrame(LevelFrame):
    """Validates a wide-format price dataframe.

    Columns: any number of float price columns (one per asset ticker), nullable.
    Index: DatetimeIndex (datetime64[ns]), PeriodIndex[M], or PeriodIndex[Y].

    Example:
                          BTCUSDT  ETHUSDT
        2020-01-01 00:00   7230.71   130.18
        2020-01-01 04:00   7205.50   130.52
        2020-01-01 08:00   7195.80   130.84
    """


class ReturnFrame(PctChangeFrame):
    """Validates a wide-format percent-change return dataframe.

    Columns: any number of float return columns (one per asset ticker), nullable.
    Index: DatetimeIndex (datetime64[ns]), PeriodIndex[M], or PeriodIndex[Y].

    Example (first row is always NaN from pct_change):
                          BTCUSDT   ETHUSDT
        2020-01-01 00:00      NaN       NaN
        2020-01-01 04:00 -0.003487  0.002612
        2020-01-01 08:00 -0.001346  0.002452
    """


class WeightFrame(pa.DataFrameModel):
    """Base schema for any portfolio weight dataframe.

    Enforces a time-like index (DatetimeIndex or PeriodIndex) and float
    columns (one per asset ticker), but imposes no constraint on how the
    weights relate to each other across a row. Use a subtype when the
    portfolio construction has a known row-sum invariant.

    Subtypes:
        FullyInvestedWeightFrame  — rows sum to 1.0 (long-only, fully invested)
        PriceNeutralWeightFrame   — rows sum to 0.0 (long-short, dollar-neutral)
    """

    asset_weight: Series[float] = pa.Field(
        alias=".*", regex=True, nullable=True
    )

    class Config:
        coerce = False  # raises on dtype mismatch instead of silently casting
        strict = False  # allows extra columns beyond what's declared

    @pa.dataframe_check
    def index_is_time_like(cls, df: pd.DataFrame) -> bool:
        return isinstance(df.index, (pd.DatetimeIndex, pd.PeriodIndex))


class FullyInvestedWeightFrame(WeightFrame):
    """Long-only, fully invested weight frame. Rows sum to 1.0.

    Every unit of capital is allocated long across the universe — no shorts,
    no cash. Each weight is in [0, 1] and the row sum equals 1.0 at every
    timestamp where weights are not NaN.

    Example:
                          BTCUSDT  ETHUSDT
        2020-01-01 00:00     0.60     0.40
        2020-01-01 04:00     0.50     0.50
        2020-01-01 08:00     0.70     0.30
    """

    asset_weight: Series[float] = pa.Field(
        alias=".*", regex=True, nullable=True, ge=0, le=1
    )

    @pa.dataframe_check
    def weights_sum_to_one(cls, df: pd.DataFrame) -> pd.Series:
        row_sums = df.sum(axis=1)
        # allow small floating point drift; skip fully-NaN rows
        return row_sums.isna() | row_sums.between(0.999, 1.001)


class PriceNeutralWeightFrame(WeightFrame):
    """Dollar-neutral (price-neutral) long-short weight frame. Rows sum to 0.0.

    Every dollar long is matched by a dollar short — net capital exposure is
    zero. Weights are in [-1, 1] and the row sum equals 0.0 at every
    timestamp where weights are not NaN.

    Example:
                          BTCUSDT  ETHUSDT  ADAUSDT
        2020-01-02       -0.1667   0.1667   0.3333
        2020-01-03        0.1667   0.3333   0.0000
        2020-01-04        0.0000   0.1667   0.3333
    """

    asset_weight: Series[float] = pa.Field(
        alias=".*", regex=True, nullable=True, ge=-1, le=1
    )

    @pa.dataframe_check
    def weights_sum_to_zero(cls, df: pd.DataFrame) -> pd.Series:
        row_sums = df.sum(axis=1)
        # allow small floating point drift; skip fully-NaN rows
        return row_sums.isna() | row_sums.between(-0.001, 0.001)
