# ⚡ SupertrendSniperPro - Futures Scalping Guide (10x Leverage)

## 🎯 Strategy Overview

**Trading Style:** Aggressive Futures Scalping  
**Leverage:** 10x (High Risk, High Reward)  
**Timeframe:** 15 minutes  
**Trading Mode:** Futures (LONG & SHORT)  
**Max Open Trades:** 8 positions  
**Target Win Rate:** 78%+  

---

## ⚠️ CRITICAL WARNING - 10x LEVERAGE

**10x leverage = 10x profits BUT also 10x losses!**

### What This Means:
- ✅ **+1% price move = +10% account profit** 🚀
- ❌ **-1% price move = -10% account loss** 💥
- ✅ **+3% target = +30% actual profit**
- ❌ **-1.5% stop = -15% actual loss**

### Risk Per Trade:
- With $1000 capital and 10x leverage
- Each position controls $10,000 worth
- **-1% move = $100 loss (10% of account!)**
- **NEVER risk more than you can afford to lose!**

---

## 💰 Profit Targets (With 10x Leverage)

| Strategy % | Actual Profit | Duration | Action |
|------------|---------------|----------|--------|
| 3% | **30%** | Immediate | Main target 🎯 |
| 2% | **20%** | 15 min | Quick scalp |
| 1.5% | **15%** | 30 min | Safe exit |
| 1% | **10%** | 45 min | Minimum |
| 0.8% | **8%** | 60 min | Emergency |

### Stop Loss:
- **-1.5% = -15% actual loss**
- Hits quickly with 10x leverage
- Must be disciplined!

---

## 🚀 Quick Start

### 1. Prerequisites

```bash
# Binance Futures Account
# Enable Futures Trading
# Set 10x leverage in Binance
# Isolated Margin Mode
# Minimum $500 capital recommended
```

### 2. API Setup

**IMPORTANT:** Enable these permissions:
- ✅ Enable Reading
- ✅ Enable Futures Trading
- ❌ NO Withdrawals (security!)
- ✅ IP Whitelist (your server IP)

### 3. Install & Configure

```bash
# Copy files
cp SupertrendSniperPro.py freqtrade/user_data/strategies/
cp config_supertrend_sniper_pro.json freqtrade/user_data/

# Edit config
nano freqtrade/user_data/config_supertrend_sniper_pro.json

# Critical settings to verify:
- "dry_run": true  # ALWAYS test first!
- "trading_mode": "futures"
- "margin_mode": "isolated"
- All leverage set to 10
- Pairs use :USDT suffix (e.g., BTC/USDT:USDT)
```

### 4. Test First (MANDATORY!)

```bash
# Dry run for 1 WEEK minimum
freqtrade trade \
    --config user_data/config_supertrend_sniper_pro.json \
    --strategy SupertrendSniperPro \
    --dry-run

# Monitor daily:
tail -f user_data/logs/freqtrade.log
```

**DO NOT skip dry run with 10x leverage! Test at least 1 week!**

---

## 📊 Strategy Logic

### LONG Position Entry (All Must Be True):

1. ✅ **HMA Rising** - Primary uptrend
2. ✅ **Supertrend Bullish** (direction = 1)
3. ✅ **Price > EMA Fast & Slow** - Above moving averages
4. ✅ **EMA Fast > EMA Slow** - Trend alignment
5. ✅ **RSI 45-65** - Good momentum, not overbought
6. ✅ **ADX > 20** - Sufficient trend strength
7. ✅ **Volume > 1.3x** - Institutional interest
8. ✅ **MACD Positive** - Momentum confirmation
9. ✅ **Heikin Ashi Bullish** - Clean candle
10. ✅ **Stochastic < 80** - Room to rise

### SHORT Position Entry (Mirror Logic):

1. ✅ **HMA Falling** - Primary downtrend
2. ✅ **Supertrend Bearish** (direction = -1)
3. ✅ **Price < EMA Fast & Slow** - Below moving averages
4. ✅ **EMA Fast < EMA Slow** - Downtrend alignment
5. ✅ **RSI 35-55** - Good momentum down
6. ✅ **ADX > 20** - Strong downtrend
7. ✅ **Volume > 1.3x** - Selling pressure
8. ✅ **MACD Negative** - Bearish momentum
9. ✅ **Heikin Ashi Bearish** - Clean red candle
10. ✅ **Stochastic > 20** - Room to fall

### CLOSE Position (Any True):

- ❌ **Supertrend Flip** - Main exit signal
- ❌ **RSI Extreme** (>70 long, <30 short)
- ❌ **Choppy Market** - Conflicting signals
- ❌ **MACD Crossover** - Momentum reversal
- ❌ **Price Cross EMA Fast** - Trend break
- ❌ **ROI Target Hit** - Take profit
- ❌ **Stop Loss Hit** - Cut loss
- ❌ **Trailing Stop** - Lock profit

---

## 💡 Scalping Best Practices

### 1. **Position Sizing**

```python
# Conservative approach with 10x leverage:
Capital: $1000
Max Risk Per Trade: 2% = $20
With -1.5% stop = -15% actual

Calculation:
Position Size = Risk / (Stop % × Leverage)
Position Size = $20 / (0.015 × 10) = $133 per trade

# With 8 max trades:
Total Exposure = 8 × $133 = $1064
Manageable with $1000 account
```

### 2. **Time Management**

```
Best Trading Hours (UTC):
- 08:00-12:00 (Europe open)
- 13:00-17:00 (US open)
- 00:00-04:00 (Asia open)

Avoid:
- Weekends (low volume)
- Major news events (high volatility)
- Low liquidity hours (02:00-06:00 UTC)
```

### 3. **Trade Duration**

```
Target: 15-60 minutes per trade
- <15 min: Quick scalp (+2-3%)
- 15-30 min: Normal trade (+1.5-2%)
- 30-60 min: Let winners run (+1-1.5%)
- >60 min: Exit regardless (avoid overnight)
```

### 4. **Daily Targets**

```
Conservative: 3-5% daily = 30-50% with 10x
Moderate: 5-8% daily = 50-80% with 10x
Aggressive: 8-10% daily = 80-100% with 10x

STOP TRADING if:
- Daily loss > 5% (-50% actual)
- 3 consecutive losses
- Market too choppy
- Feeling emotional
```

---

## 📈 Expected Performance

### Realistic Projections:

**With $1000 Capital & 10x Leverage:**

| Scenario | Win Rate | Trades/Day | Daily Profit | Weekly | Monthly |
|----------|----------|------------|--------------|--------|---------|
| Conservative | 65% | 5-8 | 3-5% | 15-25% | 60-100% |
| Moderate | 70% | 8-12 | 5-8% | 25-40% | 100-160% |
| Optimal | 78%+ | 10-15 | 8-12% | 40-60% | 160-240% |

**These are BEST CASE scenarios! Market conditions vary!**

### Risk Scenarios:

**Bad Day:**
- 5 losing trades × -15% = -75% drawdown
- **Can blow account in ONE bad day!**

**Bad Week:**
- 60% win rate (below target)
- High volatility
- -20% to -40% account loss possible

**Recovery:**
- Need 100% gain to recover from 50% loss
- Need 400% gain to recover from 75% loss
- **Risk management is CRITICAL!**

---

## 🛡️ Risk Management Rules

### MANDATORY Rules (NEVER Break These!):

1. **✅ Start Small**
   - First week: $100-200 only
   - After 1 week profit: Scale to $500
   - After 1 month profit: Scale to $1000+

2. **✅ Daily Stop Loss**
   - If lose 5% (50% actual): STOP for the day
   - If lose 10% (100% actual): STOP for the week
   - If lose 20% (200% actual): STOP and review

3. **✅ Consecutive Loss Limit**
   - 3 losses in a row: Reduce position size 50%
   - 5 losses in a row: STOP trading for the day
   - 8 losses in a row: STOP and review strategy

4. **✅ Maximum Positions**
   - Never exceed 8 open trades
   - Preferably keep 3-5 trades
   - Each trade max 2% risk

5. **✅ Avoid Revenge Trading**
   - Lost money? DON'T chase it back
   - Take a break after big loss
   - Come back with clear mind

6. **✅ Take Profits**
   - Withdraw 50% of profits weekly
   - Reinvest 50% for compound growth
   - NEVER risk all profits

7. **✅ Monitor Constantly**
   - Check positions every 30-60 min
   - Set price alerts
   - Use stop loss ALWAYS

8. **✅ Psychological Limits**
   - Don't trade when emotional
   - Don't trade when tired
   - Don't trade when drunk
   - Don't trade when stressed

---

## 📱 Monitoring Setup

### 1. Telegram Alerts

```json
{
    "telegram": {
        "enabled": true,
        "token": "YOUR_BOT_TOKEN",
        "chat_id": "YOUR_CHAT_ID",
        "notification_settings": {
            "entry": "on",
            "exit": "on",
            "entry_fill": "on",
            "exit_fill": "on"
        }
    }
}
```

### 2. Price Alerts (Binance App)

Set alerts for:
- ✅ Position entry price
- ✅ Stop loss level (-1.5%)
- ✅ Take profit levels (+1%, +2%, +3%)
- ✅ Major support/resistance

### 3. FreqUI Dashboard

```bash
# Access at: http://localhost:8080
# Monitor:
- Open positions real-time
- P&L per position
- Total daily P&L
- Win rate statistics
```

### 4. Command Line Monitoring

```bash
# Check status every 30-60 min
freqtrade status

# Check profit
freqtrade profit

# View recent trades
freqtrade show-trades --trade-source database --limit 10

# Live logs
tail -f user_data/logs/freqtrade.log
```

---

## 🔧 Optimization for Scalping

### 1. Increase Win Rate (Safer)

Edit `SupertrendSniperPro.py`:

```python
# Stricter entry conditions
adx_threshold = IntParameter(20, 35, default=25)  # Higher ADX
rsi_buy_threshold = IntParameter(48, 58, default=50)  # Tighter RSI
volume_factor = DecimalParameter(1.5, 2.5, default=1.8)  # More volume
```

### 2. Faster Exits (More Trades)

```python
# Quicker profit taking
minimal_roi = {
    "0": 0.025,   # 2.5% = 25% with 10x
    "10": 0.02,   # After 10 min
    "20": 0.015,  # After 20 min
    "30": 0.01    # After 30 min
}
```

### 3. Tighter Stop Loss (Less Risk)

```python
# Reduce risk per trade
stoploss = -0.01  # -1% = -10% actual (from -1.5%)
```

### 4. Hyperopt for Scalping

```bash
# Optimize for short-term trades
freqtrade hyperopt \
    --config user_data/config_supertrend_sniper_pro.json \
    --strategy SupertrendSniperPro \
    --hyperopt-loss SharpeHyperOptLoss \
    --spaces buy sell roi stoploss \
    --epochs 1000 \
    --timerange 20250801-
```

---

## 🎯 Best Pairs for Scalping

### Top Performers:

1. **BTC/USDT:USDT** - Most stable, high liquidity
2. **ETH/USDT:USDT** - Good volatility, predictable
3. **SOL/USDT:USDT** - High momentum, fast moves
4. **BNB/USDT:USDT** - Consistent trends
5. **DOGE/USDT:USDT** - High volatility (risky but profitable)

### Avoid for Beginners:

- ❌ Low volume pairs (<$10M daily)
- ❌ New coins (<7 days listed)
- ❌ Extreme memecoins (PEPE, SHIB for beginners)
- ❌ Pairs with wide spreads (>0.3%)

### Recommended Starting List:

Focus on 5-10 pairs maximum:
```
BTC/USDT:USDT
ETH/USDT:USDT
SOL/USDT:USDT
BNB/USDT:USDT
MATIC/USDT:USDT
LINK/USDT:USDT
AVAX/USDT:USDT
ARB/USDT:USDT
```

---

## 📊 Daily Routine

### Morning (Before Trading):

```
☐ Check Binance Futures account
☐ Verify bot is running
☐ Review overnight positions (if any)
☐ Check news/events for the day
☐ Set daily profit target
☐ Set daily loss limit
☐ Clear mind, no emotions
```

### During Trading:

```
☐ Check positions every 30-60 min
☐ Monitor Telegram alerts
☐ Don't interfere unless emergency
☐ Take breaks every 2 hours
☐ Stay hydrated and focused
☐ Stop if daily target hit
☐ Stop if daily loss limit hit
```

### Evening (After Trading):

```
☐ Review day's trades
☐ Calculate win rate
☐ Record in trading journal
☐ Analyze losses (what went wrong?)
☐ Analyze wins (what went right?)
☐ Update strategy notes
☐ Set goals for tomorrow
☐ Withdraw profits if milestone reached
```

### Weekly Review:

```
☐ Full performance analysis
☐ Win rate vs target (78%+?)
☐ Profit factor (>2.0?)
☐ Average win vs average loss
☐ Best performing pairs
☐ Worst performing pairs
☐ Adjust parameters if needed
☐ Backup database
☐ Withdraw 50% profits
```

---

## 🚨 Emergency Procedures

### If Bot Crashes:

```bash
# Check if running
ps aux | grep freqtrade

# If crashed, restart
freqtrade trade --config user_data/config_supertrend_sniper_pro.json --strategy SupertrendSniperPro

# Check logs for errors
tail -100 user_data/logs/freqtrade.log
```

### If Market Crashes:

```bash
# Close all positions immediately
freqtrade forceexit all

# Stop bot
pkill -f freqtrade

# Wait for market to stabilize
# Review losses
# Restart only when calm
```

### If Account Liquidation Risk:

```bash
# Check margin ratio in Binance
# If <20%: Close losing positions
# If <10%: Close ALL positions
# Add more margin OR
# Accept loss and close
```

### If Exchange Issues:

```bash
# Check Binance status
# Stop bot if exchange down
# Wait for resolution
# Don't panic trade manually
```

---

## 💡 Pro Tips for 10x Scalping

1. **Start Conservative**
   - Week 1: $100, 5x leverage
   - Week 2: $200, 7x leverage
   - Week 3: $500, 10x leverage
   - Scale up SLOWLY!

2. **Compound Wisely**
   - Withdraw 50% profits weekly
   - Reinvest 50% for growth
   - NEVER risk all capital

3. **Trade Best Hours**
   - High volume = better fills
   - Avoid 2-6 AM UTC (low liquidity)
   - Best: 8-12, 13-17 UTC

4. **One Screen Rule**
   - Have FreqUI on one screen
   - Binance on another
   - Quick reaction time

5. **Preset Stop Loss**
   - Set in Binance as backup
   - In case bot fails
   - Always use stop loss!

6. **Journal Everything**
   - Every trade, every day
   - Emotions, conditions, results
   - Learn from mistakes

7. **Take Breaks**
   - Don't trade 24/7
   - 6-8 hours max per day
   - Weekend breaks important

8. **Community Learning**
   - Join Freqtrade Discord
   - Share experiences
   - Learn from others

9. **Paper Trade First**
   - Minimum 1 week dry run
   - Test ALL scenarios
   - Understand the bot

10. **Know When to Stop**
    - Bad day? Stop trading
    - Emotional? Step away
    - Tired? Take break
    - Losing streak? Review strategy

---

## ⚠️ FINAL WARNING

**10x leverage is NOT for everyone!**

### You Should NOT Use 10x If:

- ❌ You're a beginner trader
- ❌ You can't afford to lose the money
- ❌ You haven't tested in dry run
- ❌ You don't understand leverage
- ❌ You trade emotionally
- ❌ You can't monitor frequently
- ❌ You don't have risk management

### You CAN Use 10x If:

- ✅ You tested 1+ week dry run successfully
- ✅ You understand leverage risks
- ✅ You have strict risk management
- ✅ You can monitor frequently
- ✅ You have capital you can lose
- ✅ You trade with discipline
- ✅ You have emergency exit plan

---

## 📚 Resources

- **Freqtrade Docs**: https://www.freqtrade.io/en/stable/
- **Binance Futures**: https://www.binance.com/en/futures
- **Discord Support**: https://discord.gg/freqtrade
- **Leverage Guide**: https://www.freqtrade.io/en/stable/leverage/

---

**Remember:**

> "With great leverage comes great responsibility"
> 
> 10x leverage can make you rich OR broke - very quickly.
> 
> Trade smart, not greedy. Risk management > Profit targets.

**Start small. Test thoroughly. Scale gradually. Stay disciplined.**

---

**Good luck and trade safe! ⚡💰**

*May your stop losses be rare and your take profits frequent!*
