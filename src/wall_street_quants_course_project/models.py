import pandas as pd 
import pandera.pandas as pa
from pandera.typing import Series


class PriceFrame(pa.DataFrameModel):
    """Validates a wide-format price dataframe.

    Columns: any number of float price columns (e.g. one per asset ticker), nullable.
    Index: pandas DatetimeIndex (datetime64[ns]), PeriodIndex[M], or PeriodIndex[Y].

    Example:
                          BTCUSDT  ETHUSDT
        2020-01-01 00:00   7230.71   130.18
        2020-01-01 04:00   7205.50   130.52
        2020-01-01 08:00   7195.80   130.84
    """

    asset_price: Series[float] = pa.Field(alias=".*", regex=True, nullable=True)

    class Config:
        coerce = False  # raises on dtype mismatch instead of silently casting
        strict = False  # allows extra columns beyond what's declared

    @pa.dataframe_check
    def index_is_time_like(cls, df: pd.DataFrame) -> bool:
        return isinstance(df.index, (pd.DatetimeIndex, pd.PeriodIndex))


class ReturnFrame(pa.DataFrameModel):
    """Validates a wide-format percent-change return dataframe.

    Columns: any number of float return columns (e.g. one per asset ticker), nullable.
    Index: pandas DatetimeIndex (datetime64[ns]), PeriodIndex[M], or PeriodIndex[Y].

    Example (first row is always NaN from pct_change):
                          BTCUSDT   ETHUSDT
        2020-01-01 00:00      NaN       NaN
        2020-01-01 04:00 -0.003487  0.002612
        2020-01-01 08:00 -0.001346  0.002452
    """

    asset_ret: Series[float] = pa.Field(alias=".*", regex=True, nullable=True)

    class Config:
        coerce = False  # raises on dtype mismatch instead of silently casting
        strict = False  # allows extra columns beyond what's declared

    @pa.dataframe_check
    def index_is_time_like(cls, df: pd.DataFrame) -> bool:
        return isinstance(df.index, (pd.DatetimeIndex, pd.PeriodIndex))



class WeightFrame(pa.DataFrameModel):
    """Base schema for any portfolio weight dataframe.

    Enforces a time-like index (DatetimeIndex or PeriodIndex) and float columns
    (one per asset ticker), but imposes no constraint on how the weights relate
    to each other across a row. Use a subtype when the portfolio construction
    has a known row-sum invariant.

    Subtypes:
        FullyInvestedWeightFrame  — rows sum to 1.0  (long-only, fully invested)
        PriceNeutralWeightFrame   — rows sum to 0.0  (long-short, dollar-neutral)
    """

    asset_weight: Series[float] = pa.Field(alias=".*", regex=True, nullable=True)

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

    asset_weight: Series[float] = pa.Field(alias=".*", regex=True, nullable=True, ge=0, le=1)

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

    asset_weight: Series[float] = pa.Field(alias=".*", regex=True, nullable=True, ge=-1, le=1)

    @pa.dataframe_check
    def weights_sum_to_zero(cls, df: pd.DataFrame) -> pd.Series:
        row_sums = df.sum(axis=1)
        # allow small floating point drift; skip fully-NaN rows
        return row_sums.isna() | row_sums.between(-0.001, 0.001)