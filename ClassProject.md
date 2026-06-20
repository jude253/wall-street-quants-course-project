## The Wall Street Quants Course Project:

### Statistical Arbitrage in Cryptocurrencies

1.  This project is designed to give you a chance to apply the concepts
    you've learned in class so far.
2.  It's also meant to provide an example of a research project that
    might be undertaken at a Quant Hedge Fund.

### Project Goal

Statistical arbitrage is a class of strategies that tries to discover
price-volume patterns that predict returns. It is one of the most
popular and successful quantitative hedge-fund strategies.

Cryptocurrency markets are still relatively new and should be fertile
grounds for finding market inefficiencies using statistical arbitrage
techniques. The two main patterns exploited in statistical arbitrage are
*momentum* and *reversal*.

***The goal of this project is to research profitable momentum and/or
reversal strategies in crypto**.*

### Research Outline

Please watch the momentum & reversal course videos if you haven't
already, they will serve as a rough research outline for this project.

In the videos, we provide guidance on how to find reversal and momentum,
as well as specific thoughts on applications to crypto. We've recapped
these points below.

Please use these as starting points for your research. You can either go
deep on one of the points or explore many. Also feel free to pursue any
ideas you may be excited about not listed here.

*How to find momentum:*

1.  Time Horizon
    a.  Longer time horizons generally lead to momentum.
    b.  Test different time horizons and see where momentum might exist.
2.  New Information / Activity
    a.  Times of heightened activity coupled with new information favor
        momentum.
    b.  Apply indicators of activity / new info (IE. Twitter activity,
        trading volume) to find stronger momentum.
3.  Seasonality
    a.  Similar seasons tend to show momentum.
    b.  What are the relevant seasons in crypto and do they show
        momentum? As we discussed, it could be worthwhile to explore
        times when institutions vs. retail trade (IE weekdays vs.
        weekends, day vs. night).
4.  Investment Themes
    a.  Investment "themes" or "styles" tend to show momentum.
    b.  We discussed some relevant themes in crypto. Do these or other
        themes you can think of show momentum?
5.  Technical Plays
    a.  Sometimes, predictable mechanical rebalancing leads to momentum.
    b.  Given the institutional crypto players, and their trading
        schedules (IE. usually during work-hours), is it possible to
        front-run them?

*How to find reversal:*

1.  Time Horizon
    a.  Shorter time horizons generally lead to reversal.
    b.  Test different time horizons and see where reversal might exist.
2.  Uninformed Trading
    a.  Uninformed (liquidity-driven) trades reverse more
    b.  Apply indicators of activity / new info (IE. Twitter activity,
        trading volume) and isolate cases of lower activity / info to
        strengthen reversal
    c.  Potentially draw upon ideas mentioned in the "Fire Sale" crypto
        video, which relied on uninformed trading during liquidations to
        find reversal.
3.  Correlation
    a.  Security A -- (Something Correlated to It) is more
        mean-reverting
    b.  Find either correlated pairs or baskets of crypto assets as
        discussed in the video on reversal/correlation.
4.  Macro
    a.  There is more reversal in times when there's more volatility and
        dislocation in the macro environment.
    b.  Test if this is true using the indicators of volatility /
        dislocation we discussed in class (implied volatility, realized
        volatility, return dispersion, pairwise correlation).

### Data

Cryptocurrency price-volume data is freely available. Please refer to
our "PriceData" lecture from week3 on how to grab crypto price-volume
data.

### Backtesting

To start, please use the "unconstrained" style of backtests we
introduced in the backtesting section of the course. If needed, we can
move onto other types of backtests later.

### Execution / Slippage

Cryptocurrencies can have commissions of \~7bps. While total slippage is
unknown and will depend on the trader's volume as well, let's assume
another 13 bps. So total all-in execution costs will be 20 bps for
market-orders. Limit orders will just have the 7 bps of commissions.

It's possible you will also have to try to alter trading to improve
execution. Please refer to our Execution -- Trading video for
guidelines.

### Weighting

During your research, it's very possible you find more than one strategy
you find compelling. For example, you may find 1 momentum strategy and 1
reversal strategy. Please refer to our videos on weighting for
guidelines on how to combine them appropriately.

### Performance Evaluation

Please provide the key performance evaluation metrics we've discussed in
class so far. This includes returns, volatility, sharpes, max drawdowns
and alpha / beta.
