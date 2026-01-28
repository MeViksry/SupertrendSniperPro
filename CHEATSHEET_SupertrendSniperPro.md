# ⚡ SupertrendSniperPro - Futures Scalping Cheatsheet (10x Leverage)

## ⚡ Quick Start - FUTURES SCALPING

```bash
# 1. Download data
freqtrade download-data --config user_data/config_supertrend_sniper_pro.json --timerange 20240101- --trading-mode futures

# 2. Test strategy
freqtrade backtesting --config user_data/config_supertrend_sniper_pro.json --strategy SupertrendSniperPro --timerange 20251029- --trading-mode futures

# 3. Start dry run (MANDATORY 1 WEEK!)
freqtrade trade --config user_data/config_supertrend_sniper_pro.json --strategy SupertrendSniperPro --dry-run

# 4. Start LIVE (⚠️ 10x LEVERAGE - after extensive testing!)
freqtrade trade --config user_data/config_supertrend_sniper_pro.json --strategy SupertrendSniperPro
```

## ⚠️ LEVERAGE WARNING

**10x Leverage Means:**
- +1% move = +10% profit ✅
- -1% move = -10% loss ❌
- +3% target = +30% actual profit 🚀
- -1.5% stop = -15% actual loss 💥

**Can blow account in ONE bad day! Use with EXTREME caution!**

---

## 📊 Daily Commands

### Monitoring
```bash
# Check status
freqtrade status

# Check profit
freqtrade profit

# Check performance
freqtrade performance

# Live logs
tail -f user_data/logs/freqtrade.log
```

### Emergency
```bash
# Stop bot (graceful)
Ctrl + C

# Force stop
pkill -f freqtrade

# Exit all trades
freqtrade forceexit all

# Exit specific trade
freqtrade forceexit <trade_id>
```

---

## 🧪 Testing Suite

```bash
# Run automated test suite
./test_supertrend_pro.sh

# Options:
1. Download data
2. Quick backtest (3 months)
3. Full backtest (1 year+)
4. Hyperopt optimization
5. Validate strategy
6. Dry run test
7. Generate reports
8. Compare strategies
9. Multi-pair analysis
10. Test webhook
11. Complete suite
```

---

## 🎯 Optimization

### Quick Hyperopt
```bash
# Optimize buy parameters (500 epochs)
freqtrade hyperopt --config user_data/config_supertrend_sniper_pro.json \
  --strategy SupertrendSniperPro \
  --hyperopt-loss SharpeHyperOptLoss \
  --spaces buy \
  --epochs 500

# Optimize sell parameters (300 epochs)
freqtrade hyperopt --config user_data/config_supertrend_sniper_pro.json \
  --strategy SupertrendSniperPro \
  --hyperopt-loss SharpeHyperOptLoss \
  --spaces sell \
  --epochs 300

# Show best results
freqtrade hyperopt-list --best
freqtrade hyperopt-show -n -1
```

### Advanced Hyperopt
```bash
# For max win rate
freqtrade hyperopt \
  --hyperopt-loss WinRatioAndProfitRatioLoss \
  --spaces buy sell roi stoploss \
  --epochs 1000

# For min drawdown
freqtrade hyperopt \
  --hyperopt-loss CalmarHyperOptLoss \
  --spaces buy sell roi stoploss \
  --epochs 1000
```

---

## 📈 Analysis

### Plots
```bash
# Profit plot
freqtrade plot-profit --config user_data/config_supertrend_sniper_pro.json --strategy SupertrendSniperPro

# Indicator plot (BTC example)
freqtrade plot-dataframe \
  --config user_data/config_supertrend_sniper_pro.json \
  --strategy SupertrendSniperPro \
  --pairs BTC/USDT \
  --indicators1 hma supertrend ema_fast ema_slow \
  --indicators2 rsi adx
```

### Reports
```bash
# Trade analysis
freqtrade backtesting-analysis --config user_data/config_supertrend_sniper_pro.json

# Show trades from file
freqtrade show-trades --trade-source file

# Show trades from database
freqtrade show-trades --trade-source database
```

---

## 🔗 Webhook Testing

```bash
# Test webhook manually
curl -X POST "YOUR_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "test",
    "pair": "BTC/USDT",
    "direction": "long",
    "price": 50000,
    "strategy": "SupertrendSniperPro",
    "timestamp": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'"
  }'
```

---

## ⚙️ Configuration Quick Edit

### Update Webhook URL
```bash
# Edit config
nano user_data/config_supertrend_sniper_pro.json

# Find and update:
"webhook": {
    "enabled": true,
    "url": "https://YOUR-WEBHOOK-URL.com/webhook"
}
```

### Switch to Live Trading
```bash
# Edit config
nano user_data/config_supertrend_sniper_pro.json

# Change these:
"dry_run": false,                    # from true
"dry_run_wallet": 1000,              # doesn't matter in live
"exchange": {
    "key": "YOUR_REAL_API_KEY",      # add real key
    "secret": "YOUR_REAL_API_SECRET"  # add real secret
}
```

### Add Telegram Notifications
```bash
# Edit config
nano user_data/config_supertrend_sniper_pro.json

# Update:
"telegram": {
    "enabled": true,
    "token": "YOUR_BOT_TOKEN",
    "chat_id": "YOUR_CHAT_ID"
}
```

---

## 🎯 Key Strategy Parameters - SCALPING

### Entry Conditions (10+ filters)
```
✅ HMA rising (faster: 30 vs 50)
✅ Supertrend bullish (tighter: 8 period, 2.5 multiplier)
✅ Price > EMA fast (15) & EMA slow (40)
✅ RSI 45-65 (scalping range)
✅ ADX > 20 (lower for scalping)
✅ Volume surge (>1.3x average)
✅ MACD histogram positive
✅ Heikin Ashi bullish
✅ Stochastic < 80 (not overbought)
✅ BB Width > 2% (not choppy)
```

### Exit Conditions
```
❌ Supertrend flip (instant)
❌ RSI > 70 (overbought for scalp)
❌ Choppy market detected
❌ MACD bearish crossover
❌ Price < EMA fast
❌ Heikin Ashi bearish
❌ ROI target hit (3% = 30% actual)
```

### Risk Management - 10x LEVERAGE
```
Timeframe: 15m (scalping)
Max Trades: 8
Stop Loss: -1.5% = -15% actual
Take Profit: +3% = +30% actual
Trailing Stop: 0.8% = 8% actual (starts at 0.8% profit)
Leverage: 10x (AGGRESSIVE!)
Position Size: 99% available (divided by open trades)
Trade Duration: 15-60 minutes target
```

---

## 📊 Performance Targets - 10x SCALPING

| Metric | Target | Action if Below |
|--------|--------|-----------------|
| Win Rate | 78%+ | Optimize entry filters |
| Profit/Trade | 3% (30% actual) | Let winners run |
| Loss/Trade | -1.5% (-15% actual) | Tighten stop |
| Daily Profit | 5-10% (50-100% actual) | Scale position |
| Max Drawdown | <10% (-100% actual) | STOP TRADING! |
| Trades/Day | 8-15 | Good pace |

## ⚠️ DAILY LIMITS (MANDATORY!)

```
✅ Daily Profit Target: 10% = 100% actual → STOP & WITHDRAW
❌ Daily Loss Limit: -5% = -50% actual → STOP FOR THE DAY
❌ Consecutive Losses: 3 in row → Reduce size 50%
❌ Consecutive Losses: 5 in row → STOP trading
```

---

## 🛠️ Troubleshooting

### No Trades
```bash
# Check pairlist
freqtrade test-pairlist --config user_data/config_supertrend_sniper_pro.json

# Lower filters in strategy:
# - adx_threshold: 25 → 20
# - volume_factor: 1.5 → 1.2
# - rsi_buy_threshold: 40 → 35
```

### Too Many Losses
```bash
# Increase filter strictness:
# - adx_threshold: 25 → 30
# - rsi_buy_threshold: 40 → 45
# - volume_factor: 1.5 → 2.0

# Reduce position size:
"max_open_trades": 5 → 3
```

### Bot Crashed
```bash
# Check logs
tail -100 user_data/logs/freqtrade.log

# Common fixes:
pip install pandas-ta ta-lib technical
freqtrade test-pairlist --config user_data/config_supertrend_sniper_pro.json
```

### Exchange Errors
```bash
# Verify API keys
# Check permissions (trading enabled)
# Test connection:
ping api.binance.com

# Regenerate API keys if needed
```

---

## 💾 Backup Commands

```bash
# Backup database
cp user_data/tradesv3.sqlite user_data/backups/tradesv3_$(date +%Y%m%d).sqlite

# Backup config
cp user_data/config_supertrend_sniper_pro.json user_data/backups/

# Backup strategy
cp user_data/strategies/SupertrendSniperPro.py user_data/backups/

# Backup hyperopt results
cp user_data/hyperopt_results/* user_data/backups/hyperopt/

# Full backup
tar -czf freqtrade_backup_$(date +%Y%m%d).tar.gz user_data/
```

---

## 📱 FreqUI Access

```bash
# Start bot with API
freqtrade trade --config user_data/config_supertrend_sniper_pro.json --strategy SupertrendSniperPro

# Access web interface:
http://localhost:8080

# Login credentials (from config):
Username: freqtrader
Password: YOUR_PASSWORD
```

---

## 🔄 Multi-Coin Management

### Current Pairlist (Top 20)
```
BTC/USDT, ETH/USDT, BNB/USDT, SOL/USDT, XRP/USDT
ADA/USDT, AVAX/USDT, DOT/USDT, MATIC/USDT, LINK/USDT
UNI/USDT, ATOM/USDT, LTC/USDT, NEAR/USDT, APT/USDT
ARB/USDT, OP/USDT, INJ/USDT, SUI/USDT, TIA/USDT
```

### Add More Coins
```bash
# Edit config
nano user_data/config_supertrend_sniper_pro.json

# Increase number:
"number_assets": 20 → 30

# Or add specific pairs:
"pair_whitelist": [
    "DOGE/USDT",
    "SHIB/USDT",
    ...
]
```

---

## ⚠️ Daily Checklist

### Morning (Before Trading)
```
☐ Check bot status (freqtrade status)
☐ Review overnight trades
☐ Check logs for errors
☐ Verify balance (freqtrade profit)
☐ Check upcoming news events
```

### During Trading
```
☐ Monitor every 2 hours
☐ Check for alerts
☐ Don't interfere with bot
☐ Let strategy work
```

### Evening (After Trading)
```
☐ Review day's performance
☐ Update trading journal
☐ Backup database
☐ Check webhook logs
☐ Plan for tomorrow
```

### Weekly Review
```
☐ Full performance analysis
☐ Compare vs targets
☐ Adjust parameters if needed
☐ Withdraw profits (if milestone)
☐ Update strategy notes
```

---

## 🆘 Emergency Contacts

- **Freqtrade Docs**: https://www.freqtrade.io
- **Discord**: https://discord.gg/freqtrade
- **GitHub Issues**: https://github.com/freqtrade/freqtrade/issues
- **Telegram**: @freqtrade

---

## 💡 Pro Tips

1. **Never trade emotions** - Let bot do its job
2. **Test in dry run** - Minimum 2 weeks before live
3. **Start small** - $100-500 initial capital
4. **Risk 1-2%** - Per trade maximum
5. **Backup daily** - Database and config
6. **Monitor, don't interfere** - Trust the strategy
7. **Weekly review** - Adjust parameters quarterly
8. **Compound profits** - Reinvest 50-70%

---

**🚀 Remember:**
- 78% win rate + 3:1 R/R = Profitable long-term
- Quality > Quantity: 5 perfect trades > 20 mediocre
- Let winners run: Trailing stop captures big moves
- Cut losers quick: -4% hard stop protects capital
- Stay disciplined: Emotions are the enemy

---

*Print this and keep near your trading setup!*
