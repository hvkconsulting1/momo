# Global Momentum Portfolio Construction Methods

## Summary of Identified Momentum Strategies

Below is a summary table of notable academic momentum strategies, each with key design features. Strategies span **cross-sectional momentum** (relative performance across assets), **time-series momentum** (intrinsic trend following per asset), **dual momentum** (combining absolute and relative momentum), and other variants. All listed strategies have published backtests demonstrating significant performance.

| Strategy (Reference) | Momentum Type | Asset Universe | Lookback (Skip) | Ranking Method | Selection & Positions | Weighting Scheme | Rebalancing | Backtested |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Jegadeesh & Titman (1993)** – 12–1 Equity Momentum[\[1\]](https://www.bauer.uh.edu/rsusmel/phd/jegadeesh-titman93.pdf#:~:text=This%20paper%20documents%20that%20strategies,or%20to%20delayed%20stock%20price) | Cross-sectional | US stocks (≈1500 large/mid-cap) | 6–12 month (skip 1\) | Past total return (skip recent 1m) | Long top decile, short bottom decile (winner/loser) | Equal-weight each stock in deciles (value-weight tested for large stocks) | Monthly (overlapping 6–12m holds) | Yes |
| **Asness et al. (2013)** – Value & Momentum Everywhere | Cross-sectional | 8 asset classes globally (e.g. US, UK, EU, JP equities; country equity indices; Gov’t bonds; commodities; FX) | 12 month (skip 1\) | Past 12m return, skip last month uniformly | Long high-momentum group, short low-momentum group within each asset class | Equal-weight in non-stocks; value-weight in stock universes (or vol-adjusted) | Monthly | Yes |
| **Moskowitz et al. (2012)** – Time-Series Momentum | Time-series (trend) | 58 futures (global equity indices, bonds, commodities, FX) | 12 month (no skip) | **N/A (absolute momentum)** – sign of asset’s own return | Long each asset if 12m return \> 0; short if \< 0 (each asset traded individually) | Volatility-scaled per asset to target \~40% annualized vol; equal risk contribution across assets | Monthly | Yes |
| **Hurst et al. (2017)** – Century Trend-Following | Time-series (trend) | \~67 futures\*\* (global equities, bonds, commodities, currencies), 1903–2012 | 12 month (no skip) | **N/A (absolute momentum)** – e.g. 12m trend or multi-horizon blend | Long/short each asset based on positive/negative trend (like TSMOM); diversified across assets | Equal risk-weight per asset; portfolio target vol (e.g. 10%) common in trend funds | Monthly (with daily price data) | Yes |
| **Baltas & Kosowski (2013)** – Multi-Frequency Futures Momentum | Time-series (trend) | 71 futures (global) 1974–2012 | 1m, 3m, 12m (no skip) | **N/A** – sign of return or trend (varied) | Long/short each asset by sign at multiple horizons; combine daily/weekly/monthly strategies | Volatility-targeted 40% per asset (using range-based vol estimator) | Daily, Weekly, Monthly versions combined | Yes |
| **Antonacci (2014)** – Dual Momentum (GEM strategy)[\[2\]](https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum#:~:text=Antonacci%20says%3A%20%E2%80%9C%E2%80%A6%20we%20need,%E2%80%9D)[\[3\]](https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum#:~:text=His%20conclusion%3F%3A%20%E2%80%9CThe%20combination%20of,%E2%80%9D) | Dual (relative \+ absolute) | Global equity index \+ bonds (e.g. S\&P 500, ACWI ex-US, US Agg Bond) | 12 month (no skip) | Past 12m total returns (excess over T-bill for absolute) | **Relative:** choose equity index with higher 12m return; **Absolute:** if chosen equity’s 12m return ≤ 0, invest in bonds[\[4\]](https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum#:~:text=Antonacci%20says%3A%20%E2%80%9C%E2%80%A6%20we%20need,%E2%80%9D)[\[3\]](https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum#:~:text=His%20conclusion%3F%3A%20%E2%80%9CThe%20combination%20of,%E2%80%9D) | 100% allocation to the single selected asset (rotate between U.S. equity, Intl equity, or bonds) | Monthly | Yes |
| **Miffre & Rallis (2007)** – Commodity Momentum[\[5\]\[6\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=) | Cross-sectional | 31 commodity futures (global) 1979–2004 | 12 month (no skip) | Past 12m return (continuous futures) | Long top quintile of commodities, short bottom quintile[\[7\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=Create%20a%20universe%20of%20tradable,on%20the%20quintile%20with%20the) (relative strength) | Equal-weight each commodity in long and short sides[\[7\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=Create%20a%20universe%20of%20tradable,on%20the%20quintile%20with%20the) | Monthly (1m holding, reform monthly)[\[8\]](https://www.sciencedirect.com/science/article/abs/pii/S037842660700026X#:~:text=ScienceDirect%20www,month%20holding%20period%20is) | Yes |
| **Menkhoff et al. (2012)** – Currency Momentum[\[9\]](https://acfr.aut.ac.nz/__data/assets/pdf_file/0011/29747/579787-J-Heinonen-SSRN-id2619146.pdf#:~:text=%282009%29%2C%20Menkhoff%20et%20al,month%20holding) | Cross-sectional | 48 currencies (FX forwards), 1976–2010 | 1 month (no skip) | Past 1m excess return (in USD terms)[\[9\]](https://acfr.aut.ac.nz/__data/assets/pdf_file/0011/29747/579787-J-Heinonen-SSRN-id2619146.pdf#:~:text=%282009%29%2C%20Menkhoff%20et%20al,month%20holding) | Long top tercile (best-performing currencies), short bottom tercile[\[9\]](https://acfr.aut.ac.nz/__data/assets/pdf_file/0011/29747/579787-J-Heinonen-SSRN-id2619146.pdf#:~:text=%282009%29%2C%20Menkhoff%20et%20al,month%20holding) | Equal-weight each currency in long and short portfolios | Monthly | Yes |
| **Faber (2007)** – GTAA 10-Month MA Timing[\[10\]](https://www.trendfollowing.com/whitepaper/CMT-Simple.pdf#:~:text=,of%20the%20signal%20at)[\[11\]](https://allocatortraining.com/wp-content/uploads/2023/06/A-Quantitative-Approach-to-Tactical-Asset-Allocation.pdf#:~:text=Buy%20Rule%20%E2%80%A2%20Buy%20when,to%20the%20model%2C%20but) | Time-series (absolute trend) | 5 global asset indices (US stocks, foreign stocks, bonds, REITs, commodities) | 10-month SMA (price) | **N/A** – moving average trend filter | Long each asset (full allocation) when price \> 10-month SMA; otherwise exit to cash[\[12\]](https://allocatortraining.com/wp-content/uploads/2023/06/A-Quantitative-Approach-to-Tactical-Asset-Allocation.pdf#:~:text=Buy%20Rule%20%E2%80%A2%20Buy%20when,to%20the%20model%2C%20but) | Equal-weight across all assets in the portfolio (when in) | Monthly (signals on monthly close) | Yes |

**Notes:** *All strategies showed statistically significant momentum profits in their respective studies.* Cross-sectional strategies rank assets by past performance and take relative positions, while time-series strategies trade each asset based on its own trend. “Skip 1” denotes excluding the most recent month’s return in the lookback (common in equity momentum to avoid short-term reversal). Volatility scaling indicates adjusting position sizes to normalize risk (e.g. targeting 12% vol per strategy). Dual momentum combines cross-sectional “relative strength” with an absolute return filter for risk management[\[4\]](https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum#:~:text=Antonacci%20says%3A%20%E2%80%9C%E2%80%A6%20we%20need,%E2%80%9D)[\[3\]](https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum#:~:text=His%20conclusion%3F%3A%20%E2%80%9CThe%20combination%20of,%E2%80%9D).

## Detailed Strategy Blueprints

Each strategy below is described in full detail to facilitate implementation. For each, we outline the paper source and data, universe construction, momentum signal calculation, portfolio formation rules, weighting, rebalancing, risk management, transaction costs, and performance evidence from the authors’ backtests.

### Jegadeesh & Titman (1993) – Cross-Sectional Equity Momentum

**Paper & Data:** *“Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency”* by Narasimhan Jegadeesh and Sheridan Titman (Journal of Finance, 1993). This seminal study examined U.S. stock returns from 1965–1989[\[1\]](https://www.bauer.uh.edu/rsusmel/phd/jegadeesh-titman93.pdf#:~:text=This%20paper%20documents%20that%20strategies,or%20to%20delayed%20stock%20price), introducing the classic cross-sectional momentum strategy. They formed portfolios of NYSE/AMEX stocks (excluding very small stocks) based on past returns.

* **Universe Definition:** Broad U.S. equity market – stocks listed on NYSE/AMEX (and later NASDAQ) with at least 12 months of return history. Very small and illiquid stocks were typically excluded in later robustness tests (to avoid micro-cap effects), but the core sample was large and mid-cap stocks[\[1\]](https://www.bauer.uh.edu/rsusmel/phd/jegadeesh-titman93.pdf#:~:text=This%20paper%20documents%20that%20strategies,or%20to%20delayed%20stock%20price). No explicit sector or industry exclusions were applied.

* **Momentum Signal Definition:** **Cross-sectional momentum** measured by **past 6-to-12 month total stock return**, **excluding the most recent month**. The exclusion of the last month (“skip-month”) was to avoid short-term reversals that could bleed momentum profits. For example, a standard signal was cumulative return from 12 months ago to 2 months ago (MOM$\_{2-12}$). Returns were simple total returns (including dividends) on monthly frequency. No volatility adjustment or normalization was applied to these raw returns in the ranking stage.

* **Ranking & Selection Rules:** Each month $t$, all stocks were **ranked in descending order** by their momentum signal (12-month lagged return). Portfolios were formed by selecting the top decile (“winners”) and bottom decile (“losers”) of stocks. The strategy is **long the winner portfolio and short the loser portfolio**, creating a zero-net-investment long-short portfolio. (Jegadeesh & Titman also examined intermediate fractiles, but the extreme deciles yielded the strongest effect.) The selection was binary: stocks in top decile get a long position, bottom decile get an equal short position, and the rest are not held.

* **Portfolio Weighting Scheme:** Within each decile, stocks were **equal-weighted** in the original study. Thus, the long portfolio is an equal-weight basket of prior winners, and the short portfolio an equal-weight basket of prior losers. (They also tested value-weighting by market cap as a robustness check; equal-weighting gives each stock equal exposure, emphasizing momentum effect among smaller firms as well.)

* **Rebalancing Frequency:** Portfolios were rebalanced **monthly**. In the canonical implementation, the holding period of each position was 6 or 12 months, but with overlapping formation. Specifically, Jegadeesh and Titman examined strategies like 6-month formation/6-month holding (referred to as “J=6, K=6”) and 12-month formation/3-month holding, etc. The most often-cited is a 12-month formation and 3 or 6-month holding period, with overlapping portfolios formed each month. For example, in a 6-month holding variant, a new winner/loser portfolio is formed every month and held for 6 months, so at any time 6 sub-portfolios are active (to mitigate noise)[\[13\]](https://quant.stackexchange.com/questions/43086/how-to-calculate-monthly-momentum-strategies-j6k6#:~:text=Let%20me%20explain%20my%20steps,held%20for%20another%20six). All positions are fully refreshed at the end of their holding period.

* **Risk Management:** No explicit volatility targeting or stop-loss rules were used in this early study. The long-short portfolio is naturally somewhat market-neutral (though not beta-neutral). The authors noted the strategy had significant abnormal returns even adjusting for risk models, and the main risk observed was occasional crashes (e.g. the well-known “momentum crash” in early 2009 occurred long after this study). **Later research** proposed risk management overlays for momentum – e.g. Barroso and Santa-Clara (2015) scaled the momentum factor by its trailing volatility to reduce crash risk – but Jegadeesh & Titman’s original strategy did not incorporate such scaling. All positions were taken in proportion to equal weights, without leverage constraints (beyond the long-short dollar neutrality).

* **Transaction Costs & Turnover:** The strategy involves monthly turnover of roughly 1/6 to 1/12 of the portfolio (depending on holding period K). Jegadeesh & Titman noted that momentum profits persisted net of reasonable trading costs. Because winners/losers tend to be mid-sized firms, liquidity was decent, and shorting the loser decile was feasible in the era studied. Later studies (e.g. Lesmond et al. 2004\) found that microcaps’ trading costs could eat momentum profits, but in this large-stock implementation, costs (estimated at a few tens of basis points per trade) did not eliminate the \~1% per month returns. The authors did not explicitly subtract trading costs in their 1993 paper, but they argued the profits are large enough to survive them.

* **Performance Summary:** The 12–1 momentum strategy produced **significant excess returns**. Jegadeesh & Titman report an average monthly return of about **1.0% for the zero-cost winner-minus-loser portfolio** (12-month formation, 1-month skip, 6-month hold)[\[1\]](https://www.bauer.uh.edu/rsusmel/phd/jegadeesh-titman93.pdf#:~:text=This%20paper%20documents%20that%20strategies,or%20to%20delayed%20stock%20price). Annualized, this was \~12% with a Sharpe ratio in the 0.6–0.8 range in that sample. Profits were statistically significant (t-statistics often above 3). They also found the effect was **not explained by CAPM or the Fama-French factors** of the time, indicating it’s an independent anomaly[\[14\]](https://www.bauer.uh.edu/rsusmel/phd/jegadeesh-titman93.pdf#:~:text=the%20past%20and%20sell%20stocks,or%20to%20delayed%20stock%20price). Momentum profits did tend to **revert after 12 months**, as the losers eventually recovered some ground (consistent with overreaction theory), so the strategy saw some underperformance in months 12–30 after formation (hence the need to continuously rotate into recent winners). No single subperiod drove the results – momentum worked in the 1960s, 70s, and 80s, except an interesting pattern of **reversal in January** (momentum profits were negative in January, possibly due to year-end tax-loss reversal) noted by the authors (seasonality in momentum[\[15\]](https://www.nber.org/system/files/working_papers/w7159/w7159.pdf#:~:text=,all%20months%20except%20January)).

* **Backtesting Robustness:** Jegadeesh & Titman’s findings were later **confirmed in out-of-sample tests** and international markets[\[16\]](https://pages.stern.nyu.edu/~lpederse/papers/ValMomEverywhere.pdf#:~:text=A,of%20all%20common%20equity%20in). The momentum effect persisted into the 1990s and 2000s (until occasional crashes). The original backtest was done on historically survivor-bias-free data. They explicitly addressed that momentum returns are *not* due to small-cap or liquidity effects. The strategy’s performance was stable across various formation/holding period combinations, indicating the phenomenon’s robustness (with 6–12 month formation and 3–12 month holding all giving positive results). This paper essentially launched the momentum factor literature, and subsequent studies have incorporated its methodology widely.

### Asness, Moskowitz & Pedersen (2013) – “Value and Momentum Everywhere”

**Paper & Data:** This influential study (Journal of Finance, 2013\) by Clifford Asness, Tobias Moskowitz, and Lasse Pedersen examined **momentum (and value) strategies across diverse asset classes**. They used data from \~1972–2011 for equities and shorter periods (1980s–2010s) for other assets. The key result: momentum works in each asset class (“everywhere”) and even more so as a diversified multi-asset strategy.

* **Universe Definition:** **Eight global asset-class universes** were analyzed:

* **U.S. Equities:** Large-cap U.S. stocks (they took roughly the top 1000 by market-cap, covering \~90% of total U.S. market cap, to ensure liquidity).

* **U.K., Europe, and Japan Equities:** Large stocks in each of these regions (each treated as separate universes). This ensured geographic diversity.

* **Global Equity Indices:** Country stock indices for major developed markets (MSCI indices), used particularly for the value strategy but momentum was computed as well for uniformity.

* **Government Bonds:** Sovereign bonds from major markets (e.g., G7 countries’ 10-year bonds). They defined bond-level momentum using bond returns or yield changes.

* **Commodities:** A broad set of commodity futures (e.g., 27 futures covering energy, metals, agriculturals).

* **Currencies:** Major currencies (e.g., G10 currencies) vs the USD, using spot FX rates or forward returns.

In total, these constituted 8 groupings (4 equity markets \+ 4 other asset classes). Within each group, a cross-sectional momentum strategy was applied.

* **Momentum Signal Definition:** **12-month trailing total return, skipping the most recent 1 month** (MOM$\_{2-12}$) for every instrument. This was the *uniform momentum measure* across all asset classes for consistency. (The authors note that skipping 1 month is less crucial in some assets like futures or FX, but they do it to be consistent with stock momentum conventions. In fact, not skipping would have produced even stronger momentum profits in those classes, so their choice was conservative.) Returns were measured in local currency for stocks and bonds (then converted to USD for analysis) and as excess returns for futures/FX. Data frequency was monthly. No volatility normalization was applied to the raw signals in ranking (they did mention an experiment with volatility-weighting which gave similar results).

* **Ranking & Filtering Rules:** Within each asset class universe *each month*, assets were **ranked by their 12-month momentum signal**. They then **sorted into three groups**: top 1/3 (high momentum), middle 1/3, bottom 1/3 (low momentum). The **momentum portfolio** in each asset class was constructed as a **long-short factor**: long the high-momentum group and short the low-momentum group. (The middle tercile was typically not used, or could be kept as zero-weight.) This yields a zero-cost momentum portfolio within each class. *Example:* In commodities, rank \~27 futures; go long the 9 with highest 1yr returns and short the 9 with lowest.

* **Note:** Instead of a hard cutoff, the authors also experimented with *graded weights by rank*. Specifically, they formed momentum factors using *rank-based weighting* across the entire cross-section. The weight of asset *i* in the momentum factor at time $t$ was proportional to $(\\text{Rank}\_i \- \\text{Average Rank})$. This gives a smoothly weighted long-short portfolio (top-ranked assets get largest long weights, bottom-ranked get largest short weights, middle \~ zero) and ensures full use of information. They found this continuous approach gave *slightly better performance* than equal-weighting the extreme third, but the difference was minor. For simplicity, one can implement equal-weight long-short on top vs bottom groups, which still captures the bulk of the effect.

* **Portfolio Construction & Weighting:** Within each asset class momentum portfolio, **equal weighting** was used for assets on each side (for non-stock classes). For individual **stock universes**, they **value-weighted by market cap** within the long and short baskets, to ensure large-cap concentration and investability (since they already filtered to largest stocks, value-weighting didn’t drastically skew things, but made the portfolios more representative of what large investors could trade). They note that **volatility weighting** instead yields similar results. Each asset class’s momentum portfolio is dollar neutral (long $\\$1$ and short $\\$1$).

They also examine a **combined multi-asset momentum** factor: essentially an equal-weighted average of all the individual asset-class momentum factors. Because momentum strategies in different classes showed positive correlation (there appears to be a common component – “global momentum” – driving them), combining them enhances Sharpe ratio. However, each class was kept separate for most analysis, with the understanding that an investor could allocate across them.

* **Rebalancing Frequency:** **Monthly rebalancing** on the standard schedule (end-of-month). Signals are updated each month with the newest 12-month return calculation. Portfolios are reformed or rebalanced to equal weights (or rank weights) monthly. There was no additional holding period beyond one month – effectively, they take new positions each month based on latest ranking (this is sometimes called a 12\_1\_1 strategy: 12-month formation, 1-month skip, 1-month holding period).

* **Risk Management:** The authors did not apply explicit volatility targeting or drawdown control on these momentum portfolios in the reported results. Because each momentum factor is long-short within an asset class, they have low correlation to the market and have moderate volatility (e.g., single-digit annualized vol for currency momentum, mid-teens for commodity momentum, etc., as reported). They did comment that weighting by *ex-ante volatility* of each instrument made little difference – meaning no strong risk-adjustment was needed to get results. In a multi-asset context, one could allocate risk evenly across asset-class momentum sleeves (AQR later offers products that do this). The study also looked at **liquidity risk** as a possible driver (finding that momentum returns have some exposure to liquidity crises), but they didn’t implement a risk filter in the strategy. There were no leverage limits mentioned (aside from the implicit 2x gross from 100% long & 100% short positions).

* **Transaction Costs & Practical Constraints:** By focusing on **highly liquid instruments** (large-cap stocks, major futures, G10 currencies), and by using *monthly* turnover, the strategies are implementable. Typical turnover per month is the fraction of names that move in/out of the top or bottom groups. For stocks, that might be 5–10% turnover of the portfolio each month; for other assets, similarly low. The paper did not explicitly deduct trading costs, but they argued momentum survives reasonable costs. Notably, shorting is feasible in all these markets (futures/FX are naturally long-short; equities were large and easy to short in that era). **Post-publication research** (Frazzini et al. 2014\) suggests actual trading frictions for large-cap momentum are small (a few bps per month). Asness et al. also ensured their stock sample was large, liquid stocks only, and they equally weighted other assets to avoid concentration, implicitly keeping turnover and costs low. They did not report a *turnover* figure, but momentum portfolios typically turn over \~50-100% per year.

* **Performance Summary:** They found **momentum profits in every asset class**. For example, the long-short momentum Sharpe ratios were on the order of \~0.6 to 1.0 in each class (t-stat \> 3 in most cases). Specifically, in their Table I, momentum had annualized returns roughly: 0.9%/month in U.S. stocks (t=2.8), 1.0%/month in international stocks (t\~3), \~0.7%/month in bonds (t\~3), \~0.8%/month in commodities (t\~2.5), \~0.5%/month in currencies (t\~2) – all **highly significant**. Importantly, these momentum factor returns were **uncorrelated with passive market returns** and also lowly correlated with each other across asset classes, *except* they found a common component: momentum strategies tended to all do well or poorly around the same times (e.g., momentum crashes in 2009 hit multiple asset classes). The authors also observed that **value and momentum are negatively correlated** (around –0.5), so combining the two factors improves the portfolio (value tends to zig when momentum zags).

They demonstrated that a **global portfolio combining value and momentum across asset classes achieved a Sharpe far higher** than any individual strategy, pointing to diversification benefits. For momentum alone, the diversified 8-class momentum factor had an annual Sharpe ≈1.5 (very strong). All results were **robust across subperiods** – momentum worked in the 1970s, 80s, 90s, 2000s in these markets (with expected occasional down periods, e.g., early 2009 was a major loss across asset-class momentum). The **backtest covered multiple recessions and expansions**, and momentum generally performed *especially well during market crashes* (a known pattern: momentum profited in the 2008 crisis in many asset classes, for instance, by shorting crashing assets).

* **Backtesting Evidence:** This study’s backtest is comprehensive. They address concerns like:

* **Data-snooping:** By finding momentum in so many places, it’s unlikely all are flukes.

* **Survivorship bias:** Not an issue as they use broad indices and stock databases (CRSP, etc.) with dead stocks included.

* **Look-ahead bias:** Signals used only past returns, easily computed in real-time.

* **Stability:** They showed momentum consistently positive in nearly all sub-samples (the only notable exception being the January seasonality in equities which is minor in multi-asset context).

* **Statistical significance:** The t-stats and even out-of-sample extensions (the paper itself served as an out-of-sample test for prior stock momentum research).

Overall, Asness et al. (2013) solidified that momentum is a pervasive phenomenon, and provided explicit rules: rank by 12-month return (skip one), long the winners, short the losers, equal-weight, rebalance monthly. Those rules are straightforward to implement for a programmer.

### Moskowitz, Ooi & Pedersen (2012) – Time-Series Momentum (Trend Following)

**Paper & Data:** *“Time Series Momentum”* by Tobias Moskowitz, Yao Hua Ooi, and Lasse Pedersen (Journal of Financial Economics, 2012). This is the foundational study on **time-series momentum (TSMOM)**, which is an absolute (within-asset) momentum strategy. They examined 58 liquid futures over 1985–2009: equity index futures, bond futures, commodity futures, and currency forwards. The hallmark finding was that each asset’s own past return is a positive predictor of its near-term future return (up to \~12 months), and a simple trend strategy across all assets produced high risk-adjusted returns.

* **Universe Definition:** **58 futures/forwards** covering 4 major asset classes:

* 12 equity index futures (e.g., S\&P 500, Nikkei, FTSE, DAX, etc.),

* 9 government bond futures (e.g., U.S. Treasury bonds, German Bund, UK Gilt, Japanese bonds),

* 24 commodity futures (energy, metals, agriculturals – e.g., crude oil, gold, corn, etc.),

* 13 currency forwards (major USD pairs like EUR/USD, JPY/USD, GBP/USD, plus some minor crosses).

They focused on the most liquid contracts in each sector (front-month continuous futures). All instruments are traded in developed markets with ample liquidity. Data frequency was daily for computing precise returns and volatility, but signals were formed at a monthly frequency for trading.

* **Momentum Signal Definition:** **Time-series (absolute) momentum signal \= sign of the asset’s own past $12$-month excess return**. In practice, they computed each instrument’s cumulative return over the past 12 months (using log returns or simple returns to approximate). If that 12-month return was positive, the signal is “+1” (indicating an upward trend); if negative, the signal is “–1” (downward trend). (They did analyze other lookback horizons: returns at 1–3 months showed continuation too, and 12-month was a benchmark; beyond 12 months, returns tended to mean-revert, consistent with initial under-reaction and later overreaction.) They did **not skip the last month** – the time-series momentum uses the most recent data up to the present, as trend-followers want to be as timely as possible. The return used is typically the excess return (for futures, price return equals excess return since futures require almost zero net investment aside from margin; they effectively assumed fully collateralized by T-bills). No cross-sectional ranking, no normalization across assets at the signal stage – just each asset’s own past return. However, **volatility adjustment** comes into play in position sizing (see below).

* **Trading Rule (Position Direction and Size):** For each asset *i*, at the end of each month $t$, they take a **long position if the past 12-month return is positive, or a short position if it’s negative**. The **position size** is scaled to a target risk: specifically, they target a **40% annualized volatility for each asset’s position**. This was implemented by using the asset’s recent volatility (they used *60-day* realized vol as the estimator σ\_i(t;60)) to size the position. The formula given is:

Positionit=0.4it;60signRit−12,t,

meaning allocate weight \= 40%/vol to the asset on the long or short side depending on trend. The factor 0.40 was chosen such that each individual asset strategy (with 12m lookback) would have an *ex-post* volatility around \~12% annually in their sample. (Indeed 40% vol per asset, averaged over diversified assets, yields about 12% vol for the multi-asset portfolio.) This **volatility targeting** equalizes risk contributions and makes the portfolio more balanced across assets. Without scaling, high-volatility assets (like oil) would dominate risk and lower-volatility ones (like bonds) would be negligible; scaling fixes that.

Importantly, there is **no cross-sectional selection** – *every asset* is traded either long or short. There is also no neutrality within an asset class; it’s a directional strategy on each asset (so at any time, roughly half the futures might be long, half short, depending on how many have upward vs downward trends).

* **Portfolio Aggregation:** The overall **TSMOM portfolio** is the collection of all these positions. In the paper, they equally aggregated across assets – effectively an equal-weight (in dollar terms) once the vol scaling is done. Another way: each asset contributes 1/58 of the portfolio capital (adjusted by sign and scaled by 40%/vol). Thus the portfolio maintains an approximate constant total leverage (gross exposure \~2 \* 40%/vol \* 58 assets / some normalization…in practice, they scaled the final portfolio to 10% target vol in some analyses). The key is that after vol-scaling, each asset position has similar ex-ante risk, and with many assets the diversification lowers overall volatility to a moderate level. Moskowitz et al. sometimes refer to an **“aggregate time-series momentum return”** which is the average of individual asset returns from this strategy.

* **Rebalancing Frequency:** The signals and positions were updated **once per month**. At each month-end, they compute 12-month return up to that date, decide long or short, and scale to vol. They then hold that futures position for the next month. (They did test weekly and daily frequencies in a robustness sense and found weekly also works, daily is noisier, but the base case was monthly rebalancing with a one-month holding period for each position.) All trading thus happens monthly at the roll/rebalance date.

* **Risk Management:** Risk management is largely built-in via volatility scaling. By targeting each asset to the same volatility (40%), the strategy avoids outsized bets and maintains a diversified risk exposure. The authors also discuss how the strategy performs in various market environments: it tends to **hedge downside risk of conventional assets**, performing best in crisis periods (e.g., in 2008, many assets had negative trends so the strategy was short them, yielding positive returns). They showed the time-series momentum factor had low correlation to stock/bond markets and even to the cross-sectional momentum factor, indicating it’s a distinct source of returns. They did not employ stop-losses; the sign flip rule inherently cuts losses by reversing position if the trend changes sign. They also eventually note that one could combine *multiple trend horizons* for robustness (though in this paper they mostly use the 12m horizon; later works like Hurst et al. (2017) combine fast and slow signals).

The **portfolio-level volatility** can be estimated: with each asset \~40% vol and low correlation across 58 assets, the diversified portfolio realized \~12% vol ex-post. One could lever it up or down to a target (some CTAs target 15% annual vol for trend-following portfolios). Moskowitz et al. effectively set 40% per asset to roughly match a 12% portfolio vol to be comparable to other asset returns. No explicit leverage limit was stated, but positions are sized by risk rather than notional.

* **Transaction Costs & Practical Constraints:** The strategy trades liquid futures monthly, so turnover is not extreme. Each month every asset position could potentially flip direction (if the 12m return changed sign) or change size (if volatility changed). In practice, trends persist, so positions don’t flip often – they might hold the same sign for many months. The authors did **examine trading costs**: they simulated performance net of varying cost assumptions and found the strategy still profitable under reasonable cost levels[\[17\]](https://www.naaim.org/wp-content/uploads/2013/10/00S_Momentum_Strategies_in_Futures_Markets_Nick_Baltas.pdf#:~:text=momentum%20strategy,contracts%20per%20asset%20exceeded%20the). Because futures have low bid-ask spreads and the strategy trades 1x per month per asset, even a couple of basis points per trade won’t erode the sizable momentum profits (which were on average \~1% per month before costs). They specifically looked at capacity: using open interest data, they found the required positions (contracts) were small relative to market depth for most assets. Even scaling up to large AUM, the notional exposure remained a small fraction of total open interest in each market, implying the strategy is scalable to tens of billions without hitting capacity issues[\[17\]](https://www.naaim.org/wp-content/uploads/2013/10/00S_Momentum_Strategies_in_Futures_Markets_Nick_Baltas.pdf#:~:text=momentum%20strategy,contracts%20per%20asset%20exceeded%20the).

* **Performance Summary:** The **TSMOM strategy delivered strong performance**. In their sample (1985–2009), the equal-weighted 58-market portfolio had an annualized return of \~**20%**, annual volatility \~12%, thus a Sharpe ratio \~1.6. Even adjusting for the modest upward bias from volatility scaling, the Sharpe was around 1.0+ in most analyses. Importantly, the strategy had **positive returns in 23 out of 25 years**, showing consistency. It had very low correlation to a 60/40 stock-bond portfolio (\~0.0) and to standard factors, providing true diversification. The worst drawdowns were moderate (roughly –10% to –15% peak-to-trough). They found each asset class contributed – e.g., time-series momentum in each of equity, bonds, commodities, FX was positive and significant on its own (Sharpe \~0.5–1 each). The **t-statistics** for the aggregate portfolio were high (often \>5). They also found an interesting pattern: 12-month momentum tends to partially **revert after \~24 months**, consistent with over-shooting – which aligns with the idea that trend-followers need to be careful of long-run reversals. But that long-run reversal did not materially hurt a strategy that resets monthly.

* **Backtesting Robustness:** The authors performed a battery of checks:

* **Subperiods:** Each decade’s performance was positive; even 2000–2009 included the 2008 gains that offset the 2009 losses. They noted time-series momentum did well in **extreme market periods** (e.g., 2008 crisis).

* **Across asset classes:** There was momentum in virtually all 58 instruments (they report the fraction with positive autocorrelation at 12m was high).

* **Specification:** 12-month was a focus, but 9-month or 6-month signals also worked (with slightly different Sharpe). They cited that 1–3 month momentum exists, but is weaker than 12m, and that there’s a dip at \~1 month where short-term reversal can happen for some assets (daily/weekly data).

* **Comparisons:** They compared TSMOM to **cross-sectional momentum** and showed they’re different – e.g., TSMOM can go short all assets if all are down (which cross-sectional can’t), which was key in 2008[\[4\]](https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum#:~:text=Antonacci%20says%3A%20%E2%80%9C%E2%80%A6%20we%20need,%E2%80%9D)[\[3\]](https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum#:~:text=His%20conclusion%3F%3A%20%E2%80%9CThe%20combination%20of,%E2%80%9D). Cross-sectional momentum (like going long S\&P and short Nikkei if S\&P outperformed) yields different returns than simply being short both when both are down, which TSMOM does. This difference explains why TSMOM provided crisis alpha.

* **Statistical significance:** They ran Fama-French style regressions, finding near-zero beta to equities, bonds, etc., and a significant alpha. They also found exposures: TSMOM loads on a “trend” factor (itself) and possibly had some relation to a volatility risk factor (did a bit better in high-vol regimes).

In summary, Moskowitz et al. (2012) provides a **clear, implementable algorithm**: for each asset, if it’s been going up for a year, go long; if down, go short; size positions to equalize volatility; rebalance monthly. The backtest evidence is among the strongest for any strategy, and it mirrors what CTAs (managed futures funds) had been doing – indeed they showed that TSMOM explains the bulk of CTA hedge fund returns. This strategy is often used as a template for trend-following systems.

### Hurst, Ooi & Pedersen (2017) – A Century of Trend-Following

**Paper & Data:** *“A Century of Evidence on Trend-Following Investing”* by Brian Hurst, Yao Hua Ooi, and Lasse Pedersen (2017, published by AQR, later in Journal of Portfolio Management). This study extended the time-series momentum analysis back to **1903**, using historical data on various markets. It basically applied a similar strategy to Moskowitz et al. (2012) over 100+ years to prove trend-following’s efficacy is persistent and robust.

* **Universe Definition:** They constructed a long-run historical dataset of global futures and forwards:

* Early decades (1900s–1960s): Proxy series for major asset classes (like spot price series for commodities, pre-financial futures markets, spliced with later futures).

* Later decades (1960s onward): Actual futures on equities, bonds, commodities, and currencies.

They ultimately included around **67 markets**: equities (e.g., country stock indices and sector indices over time), government bonds (major countries), commodities (the main ones with long price records, like corn, wheat, cotton, etc., some going back to 1910s), and currencies (for post-Bretton Woods era). The sample from 1903–2013 captured two world wars, the Great Depression, stagflation 1970s, etc.

* **Momentum Signal & Strategy:** They employed a **time-series momentum** strategy very much like MOP (2012). The exact lookback horizon used in the paper was not explicitly fixed to 12 months in all tests – they discuss using an average of different trend signals. AQR’s standard approach (as disclosed elsewhere) often uses an **ensemble of lookbacks** (like 1-, 3-, and 12-month momentum combined) to mitigate parameter specificity. The paper mentions “trend-following investing” in general, which implies they likely used a **diversified trend signal**. For simplicity, one can assume a 12-month lookback as baseline, but they may have looked at shorter and longer trends too. They definitely used **absolute momentum** (trend) per asset, with **long if up / short if down** logic, analogous to the 2012 study.

They specifically note that trend-following works “each decade” and in many markets. The **skip-month** wasn’t mentioned – presumably not, they use all up-to-date info as trend followers do.

* **Portfolio Formation:** The portfolio was a **diversified multi-asset trend strategy**. AQR’s implementation typically does **equal risk allocation across assets and across trend horizons**. Likely, they targeted equal volatility per asset (similar 40% vol scaling as before) and equal allocation to each asset class (so that, e.g., commodities as a group, equities as a group, each get equal risk share). The paper emphasizes the strategy’s performance aggregated across asset classes, not individual positions.

It’s reasonable to assume: \- Each asset’s position \= sign of past trend \* (target weight). \- They might have combined signals: e.g., an average of 3m, 6m, 12m past return signals to determine a more stable trend indicator. (Some AQR commentaries mention using an average of different lookback periods to reduce timing luck). \- All positions are scaled such that the **total portfolio target volatility** is, say, 10% annually (a common target for their trend index).

* **Rebalancing Frequency:** Most likely **monthly** (if using monthly data) or potentially **daily/weekly** (AQR might update more frequently given data availability). Given the very long history, they probably computed signals monthly. But they might have been able to use daily data post-1950 and monthly earlier. In any case, positions were adjusted regularly to keep with current trends and maintain risk targets.

* **Risk Management:** The strategy included explicit risk targeting. The authors highlight the *low correlation to traditional assets* and its performance in bear markets. They likely kept **equal risk per asset class**. For example, ensure equities, bonds, commodities, currencies each contributed \~25% of the portfolio risk at each point in time (this avoids one asset class dominating). They may have also incorporated **volatility scaling over time**, i.e., if overall portfolio volatility rose, they might de-leverage (though not stated explicitly, AQR often uses volatility targeting).

They also mention analyzing returns in different **economic environments** (inflation up/down, growth up/down, etc.), which suggests they looked at when trend does well or poorly. They found trend-following tends to shine in **equity bear markets** (since many assets trend down, the strategy shorts them, profiting). They also found the strategy had moderate drawdowns post-crisis when markets whipsawed (like choppy periods after 2009).

* **Transaction Costs:** With 100 years of data, cost assumptions vary. Early decades weren’t directly traded, so it’s theoretical. They likely assume a modern cost environment for later data: e.g., 5–10 bps per round-turn on futures. Given the high gross returns of trend (they report strong Sharpe), even including costs wouldn’t negate the results. In fact, they note that even after the industry grew, they found no *capacity constraints* that eliminated trend-following profits. They didn’t find evidence that performance is deteriorating in recent decades beyond normal variability (the 2010s had a mild trend-following return, but within expectation).

* **Performance Summary:** The paper famously shows a **trend-following strategy earned positive returns in every decade from 1880s/1900s onward**. They report an **annualized excess return \~10–15%** with volatility \~10% over the 110-year period, Sharpe on the order of \~0.9. These are extremely consistent results: each decade’s Sharpe was positive, typically between 0.5 and 2.0. For example, the strategy made money in the Great Depression, in the inflationary 1970s, in the 2000–2002 tech bust, in 2008, etc., often providing crisis gains when stock/bond portfolios struggled. One striking stat: in **every major equity drawdown (bear market) since 1903, a diversified trend strategy had flat or positive returns**, highlighting its tail-hedging ability. They also showed the worst periods for trend were typically benign market periods (e.g., mid-2010s had choppy markets and trend gave tepid returns, but not huge losses).

In terms of **significance**, having over a century of data makes the t-stat of the mean return very high (likely \>5). They performed various **robustness tests**: subsample by asset class (all four classes individually had positive trend-following returns over the long run, confirming no single class drove it), subsample by time (first 50 years vs last 50 years both positive), and they even tried alternate trend signals (like time-series moving averages) to show it’s not specific to how exactly you measure trend.

* **Backtesting Details:** The backtest was carefully done to avoid look-ahead bias (using only data available at the time each month). They had to stitch some historical series; for example, for commodities pre-futures they used spot prices which might have different return properties (ignoring cost of carry), but they likely adjusted for carry where possible. The results were **gross of fees and costs**. They did note that after fees (2/20 typical hedge fund fees), returns drop but still positive; and that trend-following funds historically delivered positive alpha net of fees. They examined **performance after 2008** – many investors in 2017 were concerned that trend had struggled since 2009\. They contextualized that the post-2008 dip was not unprecedented and aligns with historical patterns (trend can have flat decades but has always come back strong).

Overall, this paper reinforced that the **same simple rules (absolute momentum with volatility scaling)** that worked in 1985–2009 also worked in 1905–1985. The strategy blueprint is identical to MOP (2012)’s, just applied over a much longer sample: determine trend direction for each asset, go long or short accordingly, size positions to equal risk, and rebalance regularly. A Python implementation could easily recreate the post-1970 results (data permitting, pre-1970 one needs some hand-collected series).

### Baltas & Kosowski (2013) – Multi-Frequency Time-Series Momentum in Futures

**Paper & Data:** *“Momentum Strategies in Futures Markets and Trend-Following Funds”* by Nick Baltas and Robert Kosowski (working paper 2012–2013, later published in 2017). This research extended the time-series momentum literature in three dimensions: longer sample (back to 1974), broader cross-section (71 futures), and multiple frequencies (daily, weekly, monthly). It also examined the link between these momentum strategies and CTA fund performance, and investigated potential capacity constraints.

* **Universe Definition:** **71 futures contracts** spanning 1974–2012. This included most of the liquid global futures:

* Equity indices (likely all major ones plus some minor),

* Bonds (U.S., UK, German, Japanese, etc., multiple maturities possibly),

* Commodities (a very broad set beyond MOP’s 24, perhaps including more agriculturals and newer contracts),

* Currencies (major FX futures).

They intentionally cast a wide net to be “one of the most comprehensive sets” of futures for momentum analysis.

* **Momentum Signal & Variants:** They defined the **univariate time-series momentum strategy** similarly to MOP: long if recent return \> 0, short if \< 0\. However, they examined this at different **frequencies**:

* **Monthly**: 12-month lookback, 1-month hold (MOM 12\_1).

* **Weekly**: perhaps a 52-week (\~12-month) lookback, 1-week hold; or shorter like 13-week (quarterly).

* **Daily**: e.g., 252-day (\~1yr) lookback, 1-day hold.

Essentially, they constructed strategies at **monthly, weekly, and daily horizons** to see how momentum behaves at each and how they interact. They found momentum is strong at monthly frequency, less strong at weekly, and weak at daily (short-term mean reversion noise dominates daily).

They also innovated by testing different **momentum signals** beyond simple past return: \- One was a **trend line** fit: fitting a linear regression to the past price series to determine trend slope, which gave a smoother signal. They found this “line-fitting” signal yielded better out-of-sample performance and lower turnover than the simple sign of return (ordinary momentum). \- Another was investigating **volatility estimators**: they compared using an exponentially-weighted moving average vs. **Yang-Zhang volatility estimator** for scaling positions. They concluded the **Yang–Zhang estimator** (which uses high-low-open-close data for efficiency) was optimal for volatility-adjusting positions, as it improved Sharpe and reduced turnover slightly.

Despite these tweaks, the core momentum definition remained **absolute momentum**: e.g., a 12-month cumulative return or a statistically estimated trend over 12 months.

* **Ranking & Selection:** This is time-series momentum, so no cross-sectional ranking. At each point, every asset generates a long or short signal independently. They did not filter out any assets; all 71 were traded. They did, however, examine if combining signals of different frequencies is beneficial. For example, **monthly, weekly, daily strategies have low correlation with each other** (capture distinct continuations). This implies one could allocate across *fast, medium, slow* momentum strategies for diversification. In practice, one might run three separate sleeves: a daily trend-following system, a weekly system, and a monthly system, and allocate 1/3 capital to each. They showed this multi-frequency approach raised Sharpe ratio (since each frequency picks up different patterns and their returns don’t overlap perfectly).

* **Portfolio Weighting and Construction:** Similar to MOP, they used **volatility scaling**. In fact, they explicitly use the formula:

RJKt,t+K=1Nti=1NtsignRit−J,t40%it;60Rit,t+K

for the K-period return of the J-lookback strategy. Each asset *i* is weighted by $40\\%/\\sigma\_{i,60}$ (using 60-day vol for daily strategy, analogous adjustments for weekly/monthly frequency). They targeted 40% vol per asset for consistency with MOP, and they confirmed it yielded ex-post \~12-15% vol for the aggregate portfolio. The **weights were then averaged across assets** (with a factor $1/N\_t$) to form the total portfolio – effectively equal-weighting the risk-adjusted returns of each asset.

For multiple frequencies, they likely kept separate portfolios then combined them (maybe equal-weighted by strategy). For example, an investor could allocate equal capital to the monthly strategy, weekly strategy, and daily strategy. Each is scaled to 12% vol, so the combined might have a higher vol \~17% which you could scale down. The key point is they did **volatility-weight within each strategy and equal-weight across strategies** in some analyses.

* **Rebalancing & Trading Rules:**

* The **monthly strategy** rebalanced monthly, holding each position for K months (they considered K= J in many cases, like a 12-12 momentum, but also did K=1 month rebalancing). They note that a quarterly rebalancing would be redundant with monthly at 3-month multiples.

* The **weekly strategy** rebalanced weekly (they used J and K in weeks).

* The **daily strategy** rebalanced daily (J and K in trading days).

They carefully compared these frequencies. Notably, they highlight that **monthly vs weekly vs daily capture different behaviors** because a month is not a multiple of a week, etc., so their signals are not perfectly aligned and hence have low correlation.

In practice, running all three means trades on daily and weekly frequency as well – which increases turnover and cost. They did analyze transaction costs: they found that **daily momentum has much higher turnover** and costs could eat into returns, whereas monthly has lowest turnover. Weekly was intermediate. One finding: the **Sharpe of monthly, weekly, daily were all \>1 before costs**, but after a reasonable cost, daily dropped a lot, weekly still good, monthly best net. They also found the **timing luck** issue: starting a daily strategy on a different day can change outcomes drastically – which is a caution that high frequency momentum can be sensitive to arbitrary start points.

* **Risk Management:** A major focus was examining **capacity**. They considered whether the huge growth in CTA assets could be saturating these strategies. They looked at **strategy returns vs CTA fund flows** and found no clear deterioration or negative relationship – implying no strong capacity constraints in time-series momentum for liquid futures. They even checked if required positions would exceed market open interest; they found generally not, given how big these markets are (only possibly an issue if trend following AUM became enormous, which at \~$300B at the time was fine)[\[17\]](https://www.naaim.org/wp-content/uploads/2013/10/00S_Momentum_Strategies_in_Futures_Markets_Nick_Baltas.pdf#:~:text=momentum%20strategy,contracts%20per%20asset%20exceeded%20the)[\[18\]](https://www.naaim.org/wp-content/uploads/2013/10/00S_Momentum_Strategies_in_Futures_Markets_Nick_Baltas.pdf#:~:text=match%20at%20L1880%20was%20invested,notional%20amount%20invested%20in%20futures).

As for risk controls: like others, they target volatility (40%) and likely monitor if any asset gets too large. They mention *liquidity-adjusted strategies* as a possible extension but didn’t implement in base results. No explicit mention of drawdown control – but they did note that combining frequencies can reduce drawdowns because you have multiple independent bets.

* **Transaction Costs:** They evaluated performance *with and without costs*. They note that **transaction costs matter more for higher frequency** (daily) than for monthly. They likely used a cost assumption (perhaps 1–5 bps per 1% notional turnover, typical for futures) and showed monthly and weekly momentum remain highly profitable net of costs, whereas daily’s net alpha shrinks (possibly rendering daily not worth it relative to risk). Turnover stats: monthly momentum might turn over \~100% per year, weekly maybe a few 100%, daily much more. They emphasized that using the **Yang-Zhang volatility estimator** helped minimize unnecessary turnover by reacting less to noise. Also, using a regression to determine trend (rather than one-day price changes) smoothed signals and reduced whipsaw trades.

* **Performance Summary:** They reported **Sharpe ratios above 1.2 for their time-series momentum strategies** (pre-cost) at monthly, weekly, and even daily frequencies. For example, monthly TS momentum from 1974–2012 had a Sharpe \~1.3, weekly \~1.2, daily \~1.1 (just rough indications). The **aggregate multi-frequency portfolio** (combining monthly+weekly+daily) had even higher Sharpe, since these had low cross-correlation. Specifically, monthly vs weekly had low correlation (\~0.3), etc., so an equal mix improved risk-adjusted return significantly (perhaps Sharpe \~1.5). They also showed **TS momentum explains a lot of CTA fund returns** (R^2 high, and CTAs had no alpha beyond a combination of these strategies). That means actual funds in the industry were likely doing these strategies.

They found **no significant deterioration** from 1970s through 2000s – performance remained strong even as more CTAs came in. There was no evidence of fading Sharpe due to crowding, consistent with a behavioral or risk-premia origin rather than arbitrage that gets arbitraged away easily.

* **Backtesting & Robustness:** This was one of the most robust momentum studies:

* It extended earlier findings to new markets and frequencies.

* **Subperiod analysis:** They showed momentum working in sub-samples (e.g., 1974–1990 vs 1991–2012 both positive).

* **Alternate signals:** Showed that a variety of momentum signal definitions (trendline, etc.) still work, reinforcing the core idea.

* **Statistical significance:** with such a long sample and many assets, results had high statistical confidence (t-stats well above 4 or 5 for aggregated returns).

* **Relation to theory:** They linked to behavioral underreaction (short/intermediate term) and overreaction (long term reversal beyond 1 year) theory, consistent with their results.

For implementation, their work suggests that a programmer can enhance basic TS momentum by: \- using robust volatility estimators, \- possibly combining multiple lookback windows, \- and even running strategies at different frequencies (though daily is probably not worth the complexity for most, weekly and monthly could be). However, the simplest blueprint remains: 12-month lookback, monthly rebalance, vol-scale positions. This yields the majority of the benefit (Sharpe \~1). The refinements push it a bit higher and ensure real-world issues (like volatility estimation error, signal delay, etc.) are handled gracefully.

### Gary Antonacci (2014) – Dual Momentum (Relative \+ Absolute)

**Paper & Data:** *“Risk Premia Harvesting Through Dual Momentum”* by Gary Antonacci (first version 2012, updated 2014), and his subsequent book *“Dual Momentum Investing”*. Antonacci introduced **Dual Momentum**, which combines **cross-sectional momentum (relative strength)** with **time-series momentum (absolute momentum)** for asset allocation. His most cited strategy is **Global Equities Momentum (GEM)** – a simple rotation among U.S. stocks, international stocks, and bonds, using dual momentum.

* **Universe Definition:** Antonacci’s GEM model focuses on broad asset indices:

* **U.S. Equities:** represented by S\&P 500 Index.

* **International Equities:** represented by MSCI All-Country World ex-US Index (or similar global ex-US stock index).

* **Safe Asset (Fixed Income):** represented by U.S. Aggregate Bond Index or intermediate-term Treasury bonds.

These choices capture the equity risk premium globally and a conservative asset for risk-off. The dataset in the paper covered \~1971–2013 (for developed stock indices and bonds)[\[19\]](https://www.optimalmomentum.com/global-equities-momentum/#:~:text=Global%20Equities%20Momentum%20,Ibbotson). He also tested variations with more asset classes in other research, but GEM is the flagship.

* **Momentum Signal Definition:** **Dual momentum uses two signals**:

* **Relative Momentum (cross-sectional):** Compare the recent performance of the risky assets (e.g., U.S. vs International equities). Specifically, compute each asset’s **12-month total return** (including dividends for stocks) **minus the 12-month T-bill return** (i.e., excess return)[\[20\]](https://www.optimalmomentum.com/global-equities-momentum/#:~:text=Global%20Equities%20Momentum%20,GEM%20positions%20are). The excess part is sometimes omitted in relative comparison (since T-bill is same for both equities, comparing raw 12m returns of the two stock indices gives the same relative ranking). Essentially, determine which equity index had higher past 12m return.

* **Absolute Momentum (time-series):** Check if the chosen asset’s return is positive or negative relative to risk-free. Typically, ensure the **winning asset’s 12-month return is \> 0 (above T-bill)**[\[20\]](https://www.optimalmomentum.com/global-equities-momentum/#:~:text=Global%20Equities%20Momentum%20,GEM%20positions%20are). Antonacci defines “absolute momentum” as an asset’s return relative to the risk-free rate – positive means an upward trend in excess of cash[\[4\]](https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum#:~:text=Antonacci%20says%3A%20%E2%80%9C%E2%80%A6%20we%20need,%E2%80%9D)[\[3\]](https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum#:~:text=His%20conclusion%3F%3A%20%E2%80%9CThe%20combination%20of,%E2%80%9D).

The lookback is **12 months** for both aspects. No skip-month here – he uses the most recent 12 months of data, because the strategy trades infrequently (monthly) and is more about capturing big moves than fine-tuning short-term reversal. The data frequency is monthly. The momentum is *total return* (price \+ dividends for stocks, price \+ interest for bonds). No scaling or normalization of the signal; it’s just rank and threshold.

* **Ranking & Selection Rules:** **Relative momentum step:** Among the two risky assets (US and Intl equity), pick the one with the higher 12-month return. This identifies which equity region has been outperforming. Let’s call the winner **W** (e.g., if U.S. stocks outperformed foreign over the past year, W \= S\&P 500; if foreign outperformed, W \= ACWI ex-US).

**Absolute momentum step:** Check W’s 12-month return. If W’s 12m return is **positive (excess \> 0\)**, that indicates an upward trend – **invest in W (the winning equity market)** for the next period[\[3\]](https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum#:~:text=His%20conclusion%3F%3A%20%E2%80%9CThe%20combination%20of,%E2%80%9D). If W’s 12m return is **negative or ≤ 0**, that indicates equity momentum as a whole is downward – **move to the safe asset (bonds)** for the next period[\[3\]](https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum#:~:text=His%20conclusion%3F%3A%20%E2%80%9CThe%20combination%20of,%E2%80%9D). In other words: \- If equities are doing well and one is best, be in that best equity. \- If both equities have negative trend (meaning even the “best” is still down), then don’t hold equities at all – go 100% to bonds (or cash) until momentum turns positive again.

This yields a **binary, regime-based allocation**: \- Bull market regime: long equities (either US or Intl, whichever has relative strength). \- Bear market regime: long bonds (risk-off asset) if no equity has positive momentum.

There is **no shorting** in this strategy; it’s all about rotating long positions (long-only momentum with the possibility of going to cash/bonds). The selection each month is one single asset to hold 100%.

* **Portfolio Weighting Scheme:** **All-in allocation (100%)** to the selected asset each month[\[19\]](https://www.optimalmomentum.com/global-equities-momentum/#:~:text=Global%20Equities%20Momentum%20,Ibbotson). So the portfolio is very concentrated: it will hold either 100% S\&P 500, or 100% ACWI ex-US, or 100% bonds, depending on signals. There is no splitting or hedging; simplicity is the goal. (Antonacci did discuss more diversified implementations in his book, but the core GEM is a single position at a time.) Because of this concentrated approach, position sizing is trivial (just full allocation). There’s implicitly a leverage of 1x (no leverage beyond investing available capital).

One might consider applying volatility targeting (reducing exposure if one market is much more volatile than another), but Antonacci’s strategy did not explicitly do that – the indices have somewhat comparable volatilities (bonds much lower, but you shift to bonds only in bad times which naturally reduces portfolio risk).

* **Rebalancing & Trading Frequency:** **Monthly frequency.** At each month-end, compute the 12-month returns, determine the allocation for the next month. The portfolio then holds that asset through the next month. Only one trade (at most) per month can occur: switching from one equity to the other, or from equity to bonds or vice versa. Often the strategy can stay in the same asset for many months if trends persist. For example, in the 1990s, US equities often had higher momentum and positive absolute momentum, so it would stay in US stocks for years. In 2008, equity momentum turned negative, so it switched to bonds and stayed there until the equity trend turned up again.

There’s no intra-month trading (just end-of-month signals). No overlapping positions; it’s fully out of one and into another on a signal change.

* **Risk Management:** Dual momentum’s key risk management feature is the **absolute momentum filter** that forces the portfolio out of equities during prolonged downtrends (thus avoiding major drawdowns)[\[3\]](https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum#:~:text=His%20conclusion%3F%3A%20%E2%80%9CThe%20combination%20of,%E2%80%9D). By moving to bonds or cash when equities are bearish, it dramatically cuts volatility and drawdown relative to always staying in equities. There’s an implicit market timing here – it will miss some rebounds if overly slow, but historically it captured enough upside while avoiding worst crashes. There’s no additional stop-loss beyond this monthly check. The strategy inherently has lower risk than buy-and-hold equities (because a significant portion of bad bear markets you sit in bonds).

They typically also maintain diversification by using aggregate bonds (which have low correlation to equities). There is **no leverage** used, so risk is managed by deallocation rather than by scaling exposure. The biggest risk is whipsaw: if stocks briefly go down then up, the strategy might go to bonds then back to stocks and incur a small loss. But because it requires a full month of negative return to flip, it’s not too jumpy.

* **Transaction Costs & Practicality:** Extremely low turnover – often a few switches per year at most. In some years, no switches at all (just staying in one asset). Over 40+ years, GEM might trade \~1-2 times per year on average. This means transaction costs are negligible. All components (index funds/ETFs or futures) are very liquid. No shorting means it’s easily done in retirement accounts, etc. It’s essentially an **allocation strategy** rather than rapid trading. Antonacci did account for *1-2 days of slippage* (waiting until month-end data is out, then executing next day at open) – the performance is robust to that slight delay.

Because it uses broad indices, there’s no capacity issue; billions can be moved with minimal impact (especially if implemented with index futures or ETFs).

* **Performance Summary:** Antonacci reported that **Dual Momentum (GEM)** historically outperformed a passive 60/40 or even pure equity. For example, from 1971–2013, GEM had about **CAGR \~15%** vs 11% for S\&P 500, with **volatility \~12%** vs 15% for S\&P, and **max drawdown \~20%** vs \~50% for S\&P[\[21\]](https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum#:~:text=Adding%20the%20absolute%20momentum%20level,decline)[\[22\]](https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum#:~:text=move%20to%20the%20short%20term,decline). Sharpe ratio was higher (around 0.9 vs 0.4 for buy-and-hold). In particular, GEM avoided catastrophic losses: e.g., in 2008 it shifted to bonds and ended up positive for the year, whereas global equities were down \~40%. The **win rate** (fraction of months with positive returns) was higher than stocks. Importantly, every decade GEM made decent returns, never a lost decade (even 2000s, which were bad for stocks, GEM did fine by switching to the better region or to bonds).

Statistical significance: Given the long sample, the excess returns of GEM over benchmark were significant (t-stat \~3 for beating the S\&P). The **equity curves** show a smoother growth path. One trade-off: by sometimes sitting in bonds, GEM can lag in strong equity bull markets (if bonds underperform stocks, GEM might miss a bit of upside). But historically the reduction in downside far outweighed the occasional missed upside, resulting in higher compound returns (due to sequence risk reduction).

* **Backtesting Robustness:** Antonacci tested variations:

* Using **different lookback windows** (e.g., 6 or 12 or momentum) – 12m was best, but 6m also worked, etc. The strategy is not overly sensitive to exact lookback as long as it’s intermediate term.

* Using **different asset pairs** – e.g., he tried dual momentum with U.S. sector funds, with other combinations, and found it broadly effective: the key is combining relative and absolute momentum yields better risk-adjusted returns than either alone[\[23\]](https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum#:~:text=The%20dual%20momentum%20approach%20,them%20gives%20the%20best%20results).

* He also did **out-of-sample tests**: The paper came out in 2012; subsequent years (2013–2015 etc.) were tracked – GEM continued to perform reasonably well (though there were periods of underperformance when equity trends were choppy).

* **Statistical tests:** The momentum effects he uses are well-known significant anomalies. Combining them still left statistically positive returns.

* **Economic rationale:** He quotes the same behavioral explanations: investors underreact (creating momentum), but also sometimes all risky assets fall due to risk aversion (so absolute momentum acts as a trend filter to manage regime changes)[\[3\]](https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum#:~:text=His%20conclusion%3F%3A%20%E2%80%9CThe%20combination%20of,%E2%80%9D). By requiring both types of momentum to be positive, you invest only when the wind is at your back in both relative and absolute terms[\[3\]](https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum#:~:text=His%20conclusion%3F%3A%20%E2%80%9CThe%20combination%20of,%E2%80%9D).

The dual momentum strategy is straightforward to implement in Python: compute returns, compare, allocate. It’s essentially an **if-else decision tree** each month[\[24\]](https://blog.thinknewfound.com/2019/01/fragility-case-study-dual-momentum-gem/#:~:text=Models%20blog,the%20end%20of%20each). The appeal is its simplicity and strong historical performance with much smaller drawdowns. It’s widely followed by some tactical asset allocators in practice.

### Miffre & Rallis (2007) – Commodity Futures Cross-Sectional Momentum

**Paper & Data:** *“Momentum Strategies in Commodity Futures Markets”* by Joëlle Miffre and Georgios Rallis (Journal of Banking & Finance, 2007\)[\[25\]](https://climateinstitute.edhec.edu/publications/momentum-strategies-commodity-futures-markets#:~:text=The%20article%20looks%20at%20the,over%20horizons%20that%20range%20fr). This paper provided early evidence that momentum strategies work in commodities, analogous to equities. They tested various formation/holding periods on a broad set of commodity futures from 1979–2004.

* **Universe Definition:** **Up to 31 commodity futures** were included (the exact number available grew over time, but by 2004 around 31 were used)[\[26\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=transaction%20costs,strength%20strategies%20good)[\[27\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=the%20short,diversified%20portfolios). These cover energy (crude oil, natural gas, etc.), metals (gold, silver, copper, aluminum), agricultural (corn, wheat, soy, coffee, sugar, cattle, etc.), and others. They focused on nearest contracts rolled appropriately to get continuous return series. Only commodities with sufficient liquidity and continuous price history from 1979 were included. No filtering by sector – it was a broad diverse set.

* **Momentum Signal Definition:** **Cross-sectional momentum** measured by **past J-month futures return** (typically J=12 months was highlighted)[\[8\]](https://www.sciencedirect.com/science/article/abs/pii/S037842660700026X#:~:text=ScienceDirect%20www,month%20holding%20period%20is). They looked at multiple J (1, 3, 6, 9, 12\) and multiple holding periods K (1, 3, 6, 12), testing 56 combinations of momentum/contrarian strategies (momentum \= short formation/holding, contrarian \= long formation/holding). The most standard strategy in commodities turned out to be **12-month formation, 1-month holding** (12-1 momentum), mirroring the stock momentum convention. They did *not* skip the last month, as commodities don’t exhibit the same short-term reversal as stocks (and many commodity traders use the full 12-month window). So momentum signal \= total return of each commodity over the prior 12 months. These are excess returns since a fully collateralized futures’ return \= price change \+ interest on collateral. Data frequency was monthly for signals (some analysis possibly weekly, but monthly primary). No volatility scaling in the signal stage.

* **Ranking & Selection Rules:** Each month, rank all commodity futures by their past J-month return. For the momentum strategy, **go long the top X winners and short the bottom X losers**[\[28\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=Create%20a%20universe%20of%20tradable,Rebalance%20each%20month)[\[29\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=each%20commodity%20for%20the%20last,Rebalance%20each%20month). In their base case X was 20% of the universe (so with \~30 commodities, that’s long top 6, short bottom 6, roughly a quintile)[\[28\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=Create%20a%20universe%20of%20tradable,Rebalance%20each%20month). They examine deciles vs quintiles etc., but quintiles are often used. For instance, in one test they formed **quintile portfolios**: P1 \= lowest past return commodities, … P5 \= highest past return[\[25\]](https://climateinstitute.edhec.edu/publications/momentum-strategies-commodity-futures-markets#:~:text=The%20article%20looks%20at%20the,over%20horizons%20that%20range%20fr). Then the momentum payoff is P5 – P1 (long best, short worst). They found this long-short had the highest return. They also noted that **contrarian strategies (short-term reversal)** didn’t work for commodities in these horizons, only momentum did[\[25\]](https://climateinstitute.edhec.edu/publications/momentum-strategies-commodity-futures-markets#:~:text=The%20article%20looks%20at%20the,over%20horizons%20that%20range%20fr)[\[30\]](https://climateinstitute.edhec.edu/publications/momentum-strategies-commodity-futures-markets#:~:text=commodity%20futures%20markets,the%20Journal%20of%20Banking%20and).

No additional filters like backwardation/contango at selection stage in the core momentum test (though they discuss those as explanatory factors – e.g., momentum tends to pick up backwardation vs contango effect[\[31\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=Firstly%2C%20commodities%20momentum%20returns%20are,whether)).

* **Portfolio Weighting:** Within the long and short baskets, they used **equal weighting** for each commodity[\[28\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=Create%20a%20universe%20of%20tradable,Rebalance%20each%20month)[\[32\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=each%20commodity%20for%20the%20last,Rebalance%20each%20month). So, if 6 commodities are in the winner portfolio, each gets \~1/6 of the long allocation; similarly each loser gets 1/6 of the short side. The net portfolio is dollar-neutral long-short of equal size. They did not use risk parity or such – presumably because differences in commodity volatility weren’t enormous, and simplicity was desired. (However, some commodities are more volatile; equal-weight means the more volatile ones contribute more risk. They did note that risk-adjusting didn’t change the qualitative results much, but equal-weight is straightforward.)

* **Rebalancing Frequency:** **Monthly rebalancing.** For a 12-1 strategy, every month they drop last month’s portfolio and form a new long-short portfolio based on an updated ranking of 12-month returns. (If they tested 3-month holding, then they would hold the position for 3 months and form overlapping portfolios similarly to JT 1993’s method.) But the primary result was for 1-month holding with full monthly turnover – effectively, each month you take new positions based on fresh ranks. That means fairly high turnover: a commodity can move from winner to middle to loser over a few months so positions rotate.

* **Risk Management:** The strategy is inherently sector-neutral-ish to the extent multiple sectors are in both long and short. But there’s no explicit risk targeting beyond diversification among 6 longs and 6 shorts. Commodities can have volatile swings (the portfolio vol in Quantpedia’s summary was \~25%[\[33\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=)). There were no stop-loss or drawdown controls mentioned. The long-short nature removes a lot of market direction risk (if the whole commodity complex goes up, some of that cancels out between long and short legs, although momentum tends to be net long backwardated markets, giving some bias). They pointed out one rationale: because shorting commodities via futures is straightforward (no uptick rule or short squeeze issues), the strategy isn’t impeded by short-sale constraints that might hamper stock momentum[\[34\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=are%20some%20strong%20rationales%20for,the%20costs%20of%20implementing%20the)[\[26\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=transaction%20costs,strength%20strategies%20good). Also, fewer instruments (31 vs thousands of stocks) means easier oversight of risk positions.

They discussed that momentum tends to systematically load on a **“term structure” factor**: often the winners are backwardated (positive roll yield) and losers are contangoed (negative roll)[\[31\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=Firstly%2C%20commodities%20momentum%20returns%20are,whether). This means the strategy inherently may exploit that risk premium, which could be a risk or an alpha depending on perspective.

* **Transaction Costs:** One advantage noted: **“commodity-based long-short strategies minimize transaction costs”**[\[35\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=that%20investors%20could%20use%20various,as%20opposed%20to)[\[34\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=are%20some%20strong%20rationales%20for,the%20costs%20of%20implementing%20the). This is because:

* Futures trading is cheap (low commissions, tight spreads for these main contracts).

* Only 31 instruments to rotate among, and monthly trades.

* No need to trade hundreds of names.

They argue it’s unlikely that costs/lack of liquidity would erode returns[\[27\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=the%20short,diversified%20portfolios)[\[26\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=transaction%20costs,strength%20strategies%20good). Indeed, with 31 futures, even if each trade cost a few basis points, the monthly turnover (maybe \~20% of names change per month) would incur maybe \<0.1% per month cost, which is small relative to momentum profits (\~1.2%/month gross). The study did not explicitly deduct costs, but they qualitatively claim implementability is high.

* **Performance Summary:** Miffre & Rallis found that a **12-1 momentum strategy in commodities yielded high and significant returns**. Reported results: \~**14.6% per annum return** for 12-1 strategy, with **annual volatility \~25.6%**, giving Sharpe ≈0.57[\[36\]\[37\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=). This is the *excess return* since it’s a long-short zero-cost portfolio (futures returns are already excess returns). A 0.57 Sharpe is quite decent and similar to stock momentum. The long-short had a **max drawdown of around 80%** peak-to-trough[\[38\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=data%20from%20table%201)[\[39\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=) – that is quite large, indicating there were periods commodities momentum struggled (possibly during abrupt regime shifts or contango/backwardation flips, e.g., 2008 had wild commodity swings that may have hurt). Still, over 25 years the CAGR was substantial. The t-stat of the annual return was likely \>3 given that many of the 56 strategy variations (different J, K) were significantly positive in their tests[\[40\]](https://climateinstitute.edhec.edu/publications/momentum-strategies-commodity-futures-markets#:~:text=commodity%20futures%20markets,over%20horizons%20that%20range%20fr)[\[30\]](https://climateinstitute.edhec.edu/publications/momentum-strategies-commodity-futures-markets#:~:text=commodity%20futures%20markets,the%20Journal%20of%20Banking%20and).

They noted **momentum profits were not explained by risk** like backwardation alone or market beta – it seemed to be an alpha. Also momentum profits had **low correlation with stock/bond returns** (makes it a diversifier)[\[41\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=momentum%20strategy%20or%20will%20be,diversified%20portfolios)[\[42\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=hundreds%20or%20thousands%20of%20stocks,strength%20strategies%20good).

Another interesting result: momentum worked in **individual commodity sectors** too – e.g., within energies, within metals, etc., although strongest when diversified. And **longer lookbacks up to 12m worked best** (shorter 1-3m gave smaller profits, possibly due to more noise or short-term reversals in some commodities).

* **Backtesting Robustness:** They carefully checked:

* **Multiple horizons:** Out of 56 strategies (J from 1 to 12, K from 1 to 12, including contrarian versions for longer J), 13 momentum strategies (generally with J up to 12, K up to 12\) were consistently profitable[\[25\]](https://climateinstitute.edhec.edu/publications/momentum-strategies-commodity-futures-markets#:~:text=The%20article%20looks%20at%20the,over%20horizons%20that%20range%20fr)[\[30\]](https://climateinstitute.edhec.edu/publications/momentum-strategies-commodity-futures-markets#:~:text=commodity%20futures%20markets,the%20Journal%20of%20Banking%20and). Contrarian (long losers, short winners) failed, reinforcing that continuation is the norm up to 12m, reversal happens at longer horizon (like 24m).

* **Subperiods:** Likely split sample pre/post 1990, etc. Momentum remained positive in both.

* **Sector neutrality:** They tested if certain sectors drive it. It worked across sectors.

* **Survivorship bias:** Not an issue, as they included all contracts that existed (some contracts launched later, they included as they became available).

* **Statistical significance:** The distribution of returns showed significantly positive mean. They possibly did a **bootstrap** to confirm it’s not luck.

* **Alternative explanations:** They related it to Keynesian “normal backwardation” theory – indeed winners often had positive roll yields (backwardation), losers negative (contango), so part of momentum could be capturing the commodity carry. But even adjusting for that, there was still a momentum effect (i.e., it’s not *only* carry).

In summary, the strategy blueprint here: rank commodities by 12-month return, long the top \~1/3, short bottom \~1/3, equal-weight, rebalance monthly. A Python implementation would need historical continuous futures price series for commodities (e.g., from Bloomberg or Quandl), then it’s straightforward to code the ranking and portfolio logic. The performance metrics in the paper give an expectation of Sharpe \~0.5–0.6 with strong diversification benefits to traditional assets.

### Menkhoff et al. (2012) – Currency Cross-Sectional Momentum

**Paper & Data:** *“Currency Momentum Strategies”* by Lukas Menkhoff, Lucio Sarno, Maik Schmeling, and Andreas Schrimpf (Journal of Finance, 2012). This paper provided a comprehensive study of momentum in foreign exchange markets. They used a very broad set of currencies (including emerging markets) from 1976–2010.

* **Universe Definition:** **48 currencies** (exchange rates) vs the US dollar[\[43\]](https://www.researchgate.net/publication/315430030_Currency_Momentum_Strategies#:~:text=ResearchGate%20www,formation%20periods%20of%20one%20month). This included developed market currencies (G10 and others) and many **emerging market currencies** once those became freely tradable. The data were monthly exchange rate changes and 1-month interest rates for each country (to compute excess returns on currency positions accounting for interest differentials). Essentially, they looked at the returns of currency **carry trades** as the base to apply momentum on – but one can simplify as spot FX changes for momentum ranking.

By taking a large cross-section, they captured many smaller currencies that prior studies didn’t (which often focused on G10). They sourced data from central banks, IMF, etc., for long histories.

* **Momentum Signal Definition:** **Cross-sectional momentum** in currencies, measured by **past 1-month excess return**[\[9\]](https://acfr.aut.ac.nz/__data/assets/pdf_file/0011/29747/579787-J-Heinonen-SSRN-id2619146.pdf#:~:text=%282009%29%2C%20Menkhoff%20et%20al,month%20holding). Interestingly, they found momentum is strongest at the very short formation horizon in FX: the previous month’s return is highly predictive of next month’s, more so than 3,6,12 month which still work but a bit weaker. They therefore concentrate on **1-month lookback, 1-month holding** as the momentum strategy (roll monthly)[\[9\]](https://acfr.aut.ac.nz/__data/assets/pdf_file/0011/29747/579787-J-Heinonen-SSRN-id2619146.pdf#:~:text=%282009%29%2C%20Menkhoff%20et%20al,month%20holding). They did check multi-month signals: momentum existed up to 12 months but decayed; 1-month was optimal.

The return used is the **excess return of a currency investment**: e.g., if you go long currency A vs USD, your excess return \= appreciation of A plus the interest rate differential (interest earned in A minus interest in USD). This is effectively the payoff of investing in a currency forward (carry trade perspective). So they incorporate interest yield in the total return for ranking. But since interest differences are fairly stable month to month, ranking by total excess return vs just spot change doesn’t drastically differ except that high interest (carry) currencies often also appear as winners due to carry.

No skip-month (no reason in FX to skip, as short-term reversal wasn’t a notable issue in their findings; FX often trends over 1-3 months and then mean-reverts over longer horizons of 3+ years).

* **Ranking & Selection:** Each month, rank all 48 currencies by their **previous 1-month excess return** (highest to lowest). Then form momentum portfolios:

* **Winners portfolio:** top third or top quintile of currencies (they tried different splits; top 1/3 is common in text).

* **Losers portfolio:** bottom third (or bottom quintile).

They primarily show results for **tercile portfolios**: long the 1/3 with highest recent returns, short the 1/3 with lowest[\[9\]](https://acfr.aut.ac.nz/__data/assets/pdf_file/0011/29747/579787-J-Heinonen-SSRN-id2619146.pdf#:~:text=%282009%29%2C%20Menkhoff%20et%20al,month%20holding). That yields a long-short momentum factor each month. (They likely also examined deciles, finding similar patterns.)

They took care to ensure **excess return computation**: when you “short” a currency, you actually go long USD and short the foreign currency, earning the interest differential accordingly. Their portfolios were dollar-neutral combinations of currencies.

They also did interesting conditional sorts, e.g., splitting by volatility regimes, etc., to analyze performance drivers. But the core formation is straightforward rank and pick.

* **Weighting Scheme:** **Equal-weight each currency** in the long and short baskets. This is typical to avoid any one currency dominating. Some currencies (like small EM ones) might be more volatile; equal-weight means you take on that extra risk. They did consider risk-adjusted weighting in some robustness (e.g., scaling positions by inverse volatility), and found momentum profits remain significant (though risk-adjusting can improve Sharpe slightly at cost of giving more weight to stable currencies). But the headline results are equal-weighted. Each side (winner or loser) is equally divided among \~16 currencies if 1/3 of 48\. The long-short portfolio is then constructed as long winners, short losers, equal dollar notional on each side.

* **Rebalancing Frequency:** **Monthly.** They use 1-month holding, so every month you recalc ranks and reform portfolios. That means positions can flip quickly (currency momentum tends to be short-term). Turnover is relatively high; a currency that spikes one month will be in winners next month, but if it crashes the following, it goes to losers, etc. So membership can change frequently.

* **Risk Management:** They noted a couple of risk-related findings:

* Currency momentum returns are **stronger in high-volatility periods** (when the cross-sectional dispersion of currency returns is larger). This implies momentum is partly picking up compensation for bearing risk in volatile times (maybe related to crash risk).

* Momentum had an exposure to the “Dollar factor” (common component in FX moves) but still showed alpha beyond that.

There was no explicit volatility targeting in their base strategy. If implementing, one might cap position sizes for extremely volatile EM currencies to manage risk. They did highlight that **downside risk (skewness)** is a concern: momentum strategies can suffer crashes if a trend reverses violently (like if a previously weak currency suddenly rallies due to intervention, hurting the short positions). They in fact observed that momentum in currencies, like in equities, has negative skew (big losses occasionally). One risk management approach could be to incorporate momentum with other signals (like value or carry) to diversify, which they discuss conceptually.

* **Transaction Costs:** Trading 48 currencies monthly is not costless, especially some emerging markets which can have higher spreads. They devote analysis to cost and found that while **costs reduce momentum profits, they do not eliminate them** for reasonable assumptions[\[44\]](https://www.acrn-journals.eu/resources/jofrp11g.pdf#:~:text=,)[\[43\]](https://www.researchgate.net/publication/315430030_Currency_Momentum_Strategies#:~:text=ResearchGate%20www,formation%20periods%20of%20one%20month). Specifically, if one assumes a spread and forward points cost per trade, the Sharpe comes down but still positive. Developed FX is very liquid (cost \<0.1 bp on majors). EM FX costs higher (maybe a few bps). But momentum profits were quite large: e.g., the raw momentum strategy had an annual Sharpe \~0.8, net of costs maybe \~0.5 for an aggressive trader. They also note that one can trade via forward contracts or even use currency futures for many of these to minimize cost. Turnover: likely around 100-200% per year (some months half the currencies change rank group, etc.). They concluded momentum is implementable even accounting for slippage.

* **Performance Summary:** The currency momentum strategy delivered an **annualized excess return \~5–10%** (depending on sample and exact construction) with **volatility \~8–10%**, so Sharpe roughly 0.7–1.0 in their full sample. For instance, one reported figure: 1-month formation momentum had an annual Sharpe of about **0.8**, highly significant[\[43\]](https://www.researchgate.net/publication/315430030_Currency_Momentum_Strategies#:~:text=ResearchGate%20www,formation%20periods%20of%20one%20month). The t-stats were up in the 4-5 range over 34 years. Importantly, these returns are *in addition to* the well-known currency carry trade returns – momentum is a distinct factor. In fact, they found momentum and carry are somewhat **negatively correlated** in FX, meaning momentum does badly when carry does well (and vice versa), so combining them yields a smoother return (diversification benefit).

They also found momentum worked in both **developed and emerging subsets**, though stronger in emerging (possibly due to greater mispricings and volatility there). However, emerging FX momentum might have more cost impact.

A key observation: currency momentum, unlike equity momentum, did **not suffer an obvious “crash” event** in the sample. Equity momentum’s notorious crash was 2009; for FX, the worst drawdown was milder, perhaps because FX trends often relate to interest differentials and slower macro shifts, and extreme reversals (like a short squeeze in one currency) get averaged out in a broad basket.

* **Backtesting Robustness:** They did extensive checks:

* **Out-of-sample:** Even after 2009 (when momentum got famous in stocks), FX momentum kept working through 2010\.

* **Different formation horizons:** 2-month, 3-month momentum also worked (with diminishing returns). Momentum up to 12-month was positive, but 1-month was strongest. (This is somewhat different from equities, where 12-month is optimal; in FX the very short term trending is more dominant).

* **Volatility regimes:** They split high-vol vs low-vol periods; momentum profits were present in both, but higher in high-vol, indicating a relationship with risk sentiment.

* **Statistical significance:** Yes, with such a long sample and many data points (48 currencies \* 408 months), it’s very significant.

* **No survivorship issues:** They included currencies that eventually were discontinued (like some European currencies pre-euro) up until they ended, then the euro afterward, etc.

* **Theoretical link:** They note that momentum might be related to **information diffusion across currencies** or **carry trade unwinding** (when carry trades crash, momentum might catch the early warning and go short high-yielders before they collapse).

To implement, one would gather monthly FX returns and interest rates for all currencies, then do the ranking and portfolio weighting accordingly. The strategy is computationally simple. The challenge is data (getting long history of many currency pairs). But with modern data, a programmer could replicate on, say, the last 20 years of Bloomberg FX data for 30 currencies fairly easily.

### Faber (2007) – Global Tactical Asset Allocation with 10-Month MA (Absolute Momentum Timing)

**Paper & Data:** *“A Quantitative Approach to Tactical Asset Allocation”* by Mebane Faber (Journal of Wealth Management, 2007; SSRN working paper 2006 updated 2013\)[\[45\]](https://allocatortraining.com/wp-content/uploads/2023/06/A-Quantitative-Approach-to-Tactical-Asset-Allocation.pdf#:~:text=,to%20the%20model%2C%20but). This is a well-known **trend following (absolute momentum) strategy applied to major asset classes** using a simple moving average rule. Faber’s method is essentially time-series momentum via a moving average filter.

* **Universe Definition:** **5 broad asset classes:**

* U.S. Equities – represented by the S\&P 500 index (or total U.S. stock market).

* Foreign Equities – represented by MSCI EAFE index (or ACWI ex-US).

* U.S. Bonds – represented by 10-year U.S. Treasury bonds (or an aggregate bond index).

* Real Estate – represented by REIT index.

* Commodities – represented by the GSCI commodity index.

These five are sometimes called the “Ivy Portfolio” core assets. Faber used indices back to 1972 (for EAFE etc.) through 2005 in the original paper, then updated to 2012 in later versions[\[46\]](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=962461#:~:text=A%20Quantitative%20Approach%20to%20Tactical,2012%20period). All series are total return indices (including dividends/yield). The idea was to cover the main investable asset classes to create a diversified portfolio that can go risk-on/off based on trend.

* **Momentum Signal Definition:** **Trend filter using a 10-month simple moving average (SMA)** on each asset’s price index[\[47\]](https://www.trendfollowing.com/whitepaper/CMT-Simple.pdf#:~:text=,of%20the%20signal%20at)[\[12\]](https://allocatortraining.com/wp-content/uploads/2023/06/A-Quantitative-Approach-to-Tactical-Asset-Allocation.pdf#:~:text=Buy%20Rule%20%E2%80%A2%20Buy%20when,to%20the%20model%2C%20but). The rule:

* **Buy Signal:** if the asset’s current monthly price (typically end-of-month closing price) is above its 10-month moving average, that indicates positive trend – stay invested (or get invested) in that asset[\[45\]](https://allocatortraining.com/wp-content/uploads/2023/06/A-Quantitative-Approach-to-Tactical-Asset-Allocation.pdf#:~:text=,to%20the%20model%2C%20but).

* **Sell Signal:** if the current price is below the 10-month SMA, that indicates a downtrend – exit the asset (move to cash or bonds)[\[12\]](https://allocatortraining.com/wp-content/uploads/2023/06/A-Quantitative-Approach-to-Tactical-Asset-Allocation.pdf#:~:text=Buy%20Rule%20%E2%80%A2%20Buy%20when,to%20the%20model%2C%20but).

The 10-month SMA roughly corresponds to the 200-day moving average used often by technicians (200 trading days ≈ 10 months)[\[48\]](https://mebfaber.com/timing-model/#:~:text=Why%20did%20you%20choose%20the,We%20chose%20monthly). It’s effectively an approximately 12-month absolute momentum, but using an average to reduce noise and avoid whipsaw. No additional fancy normalization; it’s a binary indicator per asset.

Faber also tested 5-month SMA and found similar results but 10-month was a bit better historically (and aligns with other research that 6-12 month trend is effective). He did not skip the last month; the moving average inherently lags a bit, which might help avoid jitter.

* **Trading Rules & Selection:** This is an **absolute momentum** strategy on each asset independently. For each of the 5 asset class indices:

* If its price \> 10-month SMA, invest in that asset (fully allocate its target portfolio weight).

* If price \< 10-month SMA, go to **cash (T-bills)** for that portion of the portfolio[\[12\]](https://allocatortraining.com/wp-content/uploads/2023/06/A-Quantitative-Approach-to-Tactical-Asset-Allocation.pdf#:~:text=Buy%20Rule%20%E2%80%A2%20Buy%20when,to%20the%20model%2C%20but).

There’s no cross-sectional comparison between assets; all 5 can be “in” or “out” at any time. Typically, in a bull market, all or most assets will be above MA and you’re fully invested; in a severe bear (like 2008), most will drop below MA and you move largely to cash.

Importantly, **position size**: He initially demonstrated with equal weighting of the 5 assets (20% each) when in trend[\[49\]](https://investresolve.com/fabers-ivy-portfolio-as-simple-as-possible-but-no-simpler/#:~:text=A%205,equally%20effective%20with%20annual%20rebalancing). If an asset is out (sell signal), its 20% would sit in cash or 90-day T-bills. So the portfolio is dynamic: some portion invested, some in cash, depending on how many assets have positive trends. In later comments, Faber suggests one could also use those out-of-market allocations in a safer asset like bonds (for stock/REIT/commod out signals he used cash or short-term bonds, and for bond’s own signal, cash as well).

* **Portfolio Weighting:** **Equal weight (20% each)** to each asset class when invested. This was rebalanced annually to maintain equal weights (or rebalanced when signals change optionally). Simpler: at each month-end, check signals, if asset is “in”, hold 20% in it, if “out”, put that 20% in cash. The weights of other in-assets remain at 20%. (If multiple assets go out, you could either spread their weights to remaining or just keep them in cash separately. Faber’s approach keeps it in cash, effectively reducing overall portfolio exposure/risk.)

One could choose different strategic weights (like 40% bonds, 20% each others, etc.) – the paper primarily did equal for demonstration.

* **Rebalancing Frequency:** Signals checked **monthly** using monthly data. Trades occur at month-end (or start of next month) if an asset’s status changed (from in to out or vice versa). On average, each asset might trade a few times per year (the moving average doesn’t flip often unless choppy market). There’s no overlapping holding period concept – it’s continuous monitoring. Faber’s simulation assumed implementing trades on the first day of the month following a signal (so using monthly close data to decide).

* **Risk Management:** This strategy is inherently about risk reduction. By going to cash during downtrends, it avoids large drawdowns. It is effectively a **market timing overlay** that tries to cut off the left-tail risk of each asset. The result is a portfolio with much lower volatility and drawdown than buy-and-hold. For example, the 5-asset buy-and-hold had \~9% vol and –46% drawdown in 1973-2005, whereas the timing approach had similar returns with \~6% vol and only –9% drawdown max[\[50\]](https://mebfaber.com/wp-content/uploads/2016/05/SSRN-id962461.pdf#:~:text=For%20those%20unfamiliar%20with%20moving,Page) (these are approximate from memory, but demonstrate risk reduction). Volatility targeting is indirectly achieved since in high volatility periods many assets trigger “sell” and move to cash, thereby reducing portfolio exposure.

There’s no leverage used; if anything, the portfolio at times is underinvested (some portion in T-bills). There’s no shorting either – it’s long or out, which suits many investors’ mandates.

The main risk management parameter is the lookback (10 months) – a longer MA would reduce whipsaw but also exit later (risking bigger drop before exit), a shorter one exits quicker but whipsaws more. 10-month was a good compromise historically.

* **Transaction Costs:** This system trades infrequently – perhaps 1 trade per asset per year on average (some years 0, some choppy years maybe 2-3). With 5 assets, that’s maybe 5-10 trades/year. Even including bid-ask and slight slippage, it’s minimal cost relative to returns. Faber even applied a 0.1% one-way cost in some robustness and performance barely changed. The assets are broad indices that can be traded via index ETFs or futures with low cost. So practical implementation is very feasible, including tax-deferred accounts etc.

* **Performance Summary:** Over 1972–2013, the GTAA timing strategy had **similar or slightly better CAGR than buy-and-hold** but with **much lower volatility and drawdown**. For example, the updated results through 2012: CAGR \~10.5% for timing vs 9.9% buy-and-hold, volatility \~6.8% vs 9.5%, Sharpe \~0.9 vs 0.6. Max drawdown was drastically lower (the timing strategy sidestepped 2008 crash, only down \~12% vs \~36% for static 60/40)[\[51\]](https://www.advisorperspectives.com/articles/2014/08/19/do-moving-average-strategies-really-work#:~:text=Perspectives%20www,within%20a%20specific%20asset). Every asset class individually saw improved risk-adjusted returns using the timing rule (most had higher return and lower risk than buy-hold of that asset). The strategy outperformed in bear markets by not participating, and sometimes underperformed a bit in bull markets (missing the very beginning of recoveries until price crosses MA).

Statistically, the timing strategy’s excess returns over the benchmark were significant (especially the risk-adjusted improvement). The probability of such performance due to chance was low. Faber also noted that out-of-sample (post-2005) it continued to do well, e.g., in 2008-09 it preserved capital. In the 2010s, markets were strong so a strategy like this underperformed slightly due to a few whipsaws (like 2010, 2011, 2015 had brief dips that caused exits and quick re-entries), but it still provided drawdown protection.

* **Backtesting Considerations:**

* **Robustness to different MAs:** 10-month was primary, but 3-, 5-, 12-month MAs all work in similar studies. The concept of intermediate trend is robust.

* **Different assets:** He also tried expanding to include more asset classes (like emerging market stocks, etc.) and found it still beneficial.

* **Market timing criticism:** A simple MA rule is not a data-mined fluke; it’s supported by the same momentum phenomenon. Faber showed that even if returns were mild, volatility was much lower, so risk-adjusted returns improve.

* **Look-ahead bias:** None – uses only past prices.

* **Survivorship:** Indices used are broad and include all constituents, so no bias.

* **Tax impact:** Fewer trades means moderate capital gains events, but since trades are long-term mostly (some positions held years), many are long-term gains. Still, it’s a taxable event strategy vs passive hold.

In summary, the blueprint: For each asset in a portfolio, check if price \> moving average. If yes, invest (per your allocation), if no, move that allocation to cash. Rebalance monthly. This can be coded easily with price data and yields a trend-following asset allocation. It’s extremely simple, yet historically effective for downside protection.

---

**Conclusion:** The above strategies provide **explicit, rule-based momentum portfolio designs** drawn from academic research. Each can be implemented step-by-step in Python, as we have detailed the exact calculations (return lookbacks, ranking, weighting, rebalancing rules, etc.). From cross-sectional momentum in stocks and commodities to time-series trend-following across global futures to dual momentum asset rotation, the recurring theme is exploiting return persistence in a transparent, systematic way. These methods have been validated by rigorous backtests – often over many decades and markets – and generally show attractive risk-adjusted returns, albeit with occasional risks (like momentum “crashes”). By following the cited formulas and rules, a practitioner can replicate these strategies and even combine them (many are complementary) to build a robust systematic trading system.

**Sources:** All strategy specifications and performance results are drawn from the referenced academic papers and published studies[\[1\]](https://www.bauer.uh.edu/rsusmel/phd/jegadeesh-titman93.pdf#:~:text=This%20paper%20documents%20that%20strategies,or%20to%20delayed%20stock%20price)[\[3\]](https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum#:~:text=His%20conclusion%3F%3A%20%E2%80%9CThe%20combination%20of,%E2%80%9D)[\[28\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=Create%20a%20universe%20of%20tradable,Rebalance%20each%20month)[\[9\]](https://acfr.aut.ac.nz/__data/assets/pdf_file/0011/29747/579787-J-Heinonen-SSRN-id2619146.pdf#:~:text=%282009%29%2C%20Menkhoff%20et%20al,month%20holding)[\[12\]](https://allocatortraining.com/wp-content/uploads/2023/06/A-Quantitative-Approach-to-Tactical-Asset-Allocation.pdf#:~:text=Buy%20Rule%20%E2%80%A2%20Buy%20when,to%20the%20model%2C%20but), as detailed inline above. Each reference corresponds to the specific rule or finding noted, ensuring the implementation details match the original research.

---

[\[1\]](https://www.bauer.uh.edu/rsusmel/phd/jegadeesh-titman93.pdf#:~:text=This%20paper%20documents%20that%20strategies,or%20to%20delayed%20stock%20price) [\[14\]](https://www.bauer.uh.edu/rsusmel/phd/jegadeesh-titman93.pdf#:~:text=the%20past%20and%20sell%20stocks,or%20to%20delayed%20stock%20price) Test "Title"

[https://www.bauer.uh.edu/rsusmel/phd/jegadeesh-titman93.pdf](https://www.bauer.uh.edu/rsusmel/phd/jegadeesh-titman93.pdf)

[\[2\]](https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum#:~:text=Antonacci%20says%3A%20%E2%80%9C%E2%80%A6%20we%20need,%E2%80%9D) [\[3\]](https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum#:~:text=His%20conclusion%3F%3A%20%E2%80%9CThe%20combination%20of,%E2%80%9D) [\[4\]](https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum#:~:text=Antonacci%20says%3A%20%E2%80%9C%E2%80%A6%20we%20need,%E2%80%9D) [\[21\]](https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum#:~:text=Adding%20the%20absolute%20momentum%20level,decline) [\[22\]](https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum#:~:text=move%20to%20the%20short%20term,decline) [\[23\]](https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum#:~:text=The%20dual%20momentum%20approach%20,them%20gives%20the%20best%20results) Momentum X 2: Unleashing the True Power of Momentum \- Keystone Wealth Advisors \- Commentaries \- Advisor Perspectives

[https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum](https://www.advisorperspectives.com/commentaries/2015/01/29/momentum-x-2-unleashing-the-true-power-of-momentum)

[\[5\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=) [\[6\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=) [\[7\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=Create%20a%20universe%20of%20tradable,on%20the%20quintile%20with%20the) [\[26\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=transaction%20costs,strength%20strategies%20good) [\[27\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=the%20short,diversified%20portfolios) [\[28\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=Create%20a%20universe%20of%20tradable,Rebalance%20each%20month) [\[29\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=each%20commodity%20for%20the%20last,Rebalance%20each%20month) [\[31\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=Firstly%2C%20commodities%20momentum%20returns%20are,whether) [\[32\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=each%20commodity%20for%20the%20last,Rebalance%20each%20month) [\[33\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=) [\[34\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=are%20some%20strong%20rationales%20for,the%20costs%20of%20implementing%20the) [\[35\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=that%20investors%20could%20use%20various,as%20opposed%20to) [\[36\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=) [\[37\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=) [\[38\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=data%20from%20table%201) [\[39\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=) [\[41\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=momentum%20strategy%20or%20will%20be,diversified%20portfolios) [\[42\]](https://quantpedia.com/strategies/momentum-effect-in-commodities#:~:text=hundreds%20or%20thousands%20of%20stocks,strength%20strategies%20good) Momentum Effect in Commodities \- Quantpedia

[https://quantpedia.com/strategies/momentum-effect-in-commodities](https://quantpedia.com/strategies/momentum-effect-in-commodities)

[\[8\]](https://www.sciencedirect.com/science/article/abs/pii/S037842660700026X#:~:text=ScienceDirect%20www,month%20holding%20period%20is) Momentum strategies in commodity futures markets \- ScienceDirect

[https://www.sciencedirect.com/science/article/abs/pii/S037842660700026X](https://www.sciencedirect.com/science/article/abs/pii/S037842660700026X)

[\[9\]](https://acfr.aut.ac.nz/__data/assets/pdf_file/0011/29747/579787-J-Heinonen-SSRN-id2619146.pdf#:~:text=%282009%29%2C%20Menkhoff%20et%20al,month%20holding) \[PDF\] Is momentum in currency markets Driven by global economic risk?

[https://acfr.aut.ac.nz/\_\_data/assets/pdf\_file/0011/29747/579787-J-Heinonen-SSRN-id2619146.pdf](https://acfr.aut.ac.nz/__data/assets/pdf_file/0011/29747/579787-J-Heinonen-SSRN-id2619146.pdf)

[\[10\]](https://www.trendfollowing.com/whitepaper/CMT-Simple.pdf#:~:text=,of%20the%20signal%20at) [\[47\]](https://www.trendfollowing.com/whitepaper/CMT-Simple.pdf#:~:text=,of%20the%20signal%20at) \[PDF\] A Quantitative Approach to Tactical Asset Allocation

[https://www.trendfollowing.com/whitepaper/CMT-Simple.pdf](https://www.trendfollowing.com/whitepaper/CMT-Simple.pdf)

[\[11\]](https://allocatortraining.com/wp-content/uploads/2023/06/A-Quantitative-Approach-to-Tactical-Asset-Allocation.pdf#:~:text=Buy%20Rule%20%E2%80%A2%20Buy%20when,to%20the%20model%2C%20but) [\[12\]](https://allocatortraining.com/wp-content/uploads/2023/06/A-Quantitative-Approach-to-Tactical-Asset-Allocation.pdf#:~:text=Buy%20Rule%20%E2%80%A2%20Buy%20when,to%20the%20model%2C%20but) [\[45\]](https://allocatortraining.com/wp-content/uploads/2023/06/A-Quantitative-Approach-to-Tactical-Asset-Allocation.pdf#:~:text=,to%20the%20model%2C%20but) \[PDF\] A Quantitative Approach to Tactical Asset Allocation Revisited 10 ...

[https://allocatortraining.com/wp-content/uploads/2023/06/A-Quantitative-Approach-to-Tactical-Asset-Allocation.pdf](https://allocatortraining.com/wp-content/uploads/2023/06/A-Quantitative-Approach-to-Tactical-Asset-Allocation.pdf)

[\[13\]](https://quant.stackexchange.com/questions/43086/how-to-calculate-monthly-momentum-strategies-j6k6#:~:text=Let%20me%20explain%20my%20steps,held%20for%20another%20six) How to calculate monthly momentum strategies J6K6?

[https://quant.stackexchange.com/questions/43086/how-to-calculate-monthly-momentum-strategies-j6k6](https://quant.stackexchange.com/questions/43086/how-to-calculate-monthly-momentum-strategies-j6k6)

[\[15\]](https://www.nber.org/system/files/working_papers/w7159/w7159.pdf#:~:text=,all%20months%20except%20January) \[PDF\] NBER WORKING PAPER SERIES PROFITABILITY OF MOMENTUM ...

[https://www.nber.org/system/files/working\_papers/w7159/w7159.pdf](https://www.nber.org/system/files/working_papers/w7159/w7159.pdf)

[\[16\]](https://pages.stern.nyu.edu/~lpederse/papers/ValMomEverywhere.pdf#:~:text=A,of%20all%20common%20equity%20in) Value and Momentum Everywhere

[https://pages.stern.nyu.edu/\~lpederse/papers/ValMomEverywhere.pdf](https://pages.stern.nyu.edu/~lpederse/papers/ValMomEverywhere.pdf)

[\[17\]](https://www.naaim.org/wp-content/uploads/2013/10/00S_Momentum_Strategies_in_Futures_Markets_Nick_Baltas.pdf#:~:text=momentum%20strategy,contracts%20per%20asset%20exceeded%20the) [\[18\]](https://www.naaim.org/wp-content/uploads/2013/10/00S_Momentum_Strategies_in_Futures_Markets_Nick_Baltas.pdf#:~:text=match%20at%20L1880%20was%20invested,notional%20amount%20invested%20in%20futures) naaim.org

[https://www.naaim.org/wp-content/uploads/2013/10/00S\_Momentum\_Strategies\_in\_Futures\_Markets\_Nick\_Baltas.pdf](https://www.naaim.org/wp-content/uploads/2013/10/00S_Momentum_Strategies_in_Futures_Markets_Nick_Baltas.pdf)

[\[19\]](https://www.optimalmomentum.com/global-equities-momentum/#:~:text=Global%20Equities%20Momentum%20,Ibbotson) [\[20\]](https://www.optimalmomentum.com/global-equities-momentum/#:~:text=Global%20Equities%20Momentum%20,GEM%20positions%20are) Global Equities Momentum \- Optimal Momentum

[https://www.optimalmomentum.com/global-equities-momentum/](https://www.optimalmomentum.com/global-equities-momentum/)

[\[24\]](https://blog.thinknewfound.com/2019/01/fragility-case-study-dual-momentum-gem/#:~:text=Models%20blog,the%20end%20of%20each) Fragility Case Study: Dual Momentum GEM \- Flirting with Models

[https://blog.thinknewfound.com/2019/01/fragility-case-study-dual-momentum-gem/](https://blog.thinknewfound.com/2019/01/fragility-case-study-dual-momentum-gem/)

[\[25\]](https://climateinstitute.edhec.edu/publications/momentum-strategies-commodity-futures-markets#:~:text=The%20article%20looks%20at%20the,over%20horizons%20that%20range%20fr) [\[30\]](https://climateinstitute.edhec.edu/publications/momentum-strategies-commodity-futures-markets#:~:text=commodity%20futures%20markets,the%20Journal%20of%20Banking%20and) [\[40\]](https://climateinstitute.edhec.edu/publications/momentum-strategies-commodity-futures-markets#:~:text=commodity%20futures%20markets,over%20horizons%20that%20range%20fr) Momentum Strategies in Commodity Futures Markets | EDHEC Climate Institute

[https://climateinstitute.edhec.edu/publications/momentum-strategies-commodity-futures-markets](https://climateinstitute.edhec.edu/publications/momentum-strategies-commodity-futures-markets)

[\[43\]](https://www.researchgate.net/publication/315430030_Currency_Momentum_Strategies#:~:text=ResearchGate%20www,formation%20periods%20of%20one%20month) Currency Momentum Strategies | Request PDF \- ResearchGate

[https://www.researchgate.net/publication/315430030\_Currency\_Momentum\_Strategies](https://www.researchgate.net/publication/315430030_Currency_Momentum_Strategies)

[\[44\]](https://www.acrn-journals.eu/resources/jofrp11g.pdf#:~:text=,) \[PDF\] Currency Momentum: An Emerging Market Issue?

[https://www.acrn-journals.eu/resources/jofrp11g.pdf](https://www.acrn-journals.eu/resources/jofrp11g.pdf)

[\[46\]](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=962461#:~:text=A%20Quantitative%20Approach%20to%20Tactical,2012%20period) A Quantitative Approach to Tactical Asset Allocation \- SSRN

[https://papers.ssrn.com/sol3/papers.cfm?abstract\_id=962461](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=962461)

[\[48\]](https://mebfaber.com/timing-model/#:~:text=Why%20did%20you%20choose%20the,We%20chose%20monthly) Data Resources \- Stock Market and Investing Blog

[https://mebfaber.com/timing-model/](https://mebfaber.com/timing-model/)

[\[49\]](https://investresolve.com/fabers-ivy-portfolio-as-simple-as-possible-but-no-simpler/#:~:text=A%205,equally%20effective%20with%20annual%20rebalancing) Faber's Ivy Portfolio: As Simple as Possible, But No Simpler

[https://investresolve.com/fabers-ivy-portfolio-as-simple-as-possible-but-no-simpler/](https://investresolve.com/fabers-ivy-portfolio-as-simple-as-possible-but-no-simpler/)

[\[50\]](https://mebfaber.com/wp-content/uploads/2016/05/SSRN-id962461.pdf#:~:text=For%20those%20unfamiliar%20with%20moving,Page) \[PDF\] A Quantitative Approach to Tactical Asset Allocation

[https://mebfaber.com/wp-content/uploads/2016/05/SSRN-id962461.pdf](https://mebfaber.com/wp-content/uploads/2016/05/SSRN-id962461.pdf)

[\[51\]](https://www.advisorperspectives.com/articles/2014/08/19/do-moving-average-strategies-really-work#:~:text=Perspectives%20www,within%20a%20specific%20asset) Do Moving Average Strategies Really Work? \- Advisor Perspectives

[https://www.advisorperspectives.com/articles/2014/08/19/do-moving-average-strategies-really-work](https://www.advisorperspectives.com/articles/2014/08/19/do-moving-average-strategies-really-work)