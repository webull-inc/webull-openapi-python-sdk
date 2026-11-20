# Low-risk HMM regime bot (SPY, long-only, paper-first)

## What changed to cut risk (vs. the first plan)
| Area | Before | Now |
|---|---|---|
| Max equity exposure | 95-100% | **70%**, never leveraged, rest in cash |
| Hard drawdown halt | 10% | **6%** -> flat + halt, manual reset live |
| Soft drawdown | none | **3%** -> exposure capped at 35% |
| Daily loss limit | optional | **-1.5%** -> flat next bar |
| Vol targeting | none | exposure <= 10% / realized vol |
| Trend filter | none | below 200d SMA -> max 40% |
| Crash override | none | P(high-vol state) >= 60% -> cash |
| Re-entry | immediate | **3 confirming bars, +20% per bar**; exits are immediate |
| Training window | 252d | **504d** (more stable fits), states sorted by volatility |
| Execution | same bar | signal at close t, trade at **open t+1**, 5 bps/side cost |
| Go-live | flag | `paper=True`, `dry_run=True` by default; live needs `ALLOW_LIVE=YES` |

## Run
    pip install -r requirements.txt
    python -m unittest discover -s tests -v       # 14 tests, incl. look-ahead checks
    python backtest.py --csv data/SPY.csv         # real data: columns date,open,high,low,close,volume
    python backtest.py                            # synthetic data, offline demo only

Live (paper): set `ALPACA_API_KEY` / `ALPACA_SECRET_KEY`, then `python main.py --once`
(dry-run logs orders only). Set `LiveConfig.dry_run=False` to send paper orders.
Create a file named `KILL` to flatten and stop. After a halt: `python main.py --reset-halt`.

## Pre-live checklist
1. Backtest on 15+ years of real SPY (include 2008, 2020, 2022). Treat anything that looks great as a bug first.
2. Dry-run, then paper trade 2-3 months; compare fills with the 5 bps assumption.
3. Confirm after-hours orders queue for the next open on your Alpaca account (AlpacaBroker is untested offline).
4. Only then consider small real money. Nothing here guarantees profit or prevents loss.
