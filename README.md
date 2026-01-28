# SupertrendSniperPro

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Freqtrade](https://img.shields.io/badge/freqtrade-2024.1+-brightgreen.svg)](https://www.freqtrade.io/)
[![Trading Mode](https://img.shields.io/badge/trading-futures-orange.svg)](https://www.binance.com/en/futures)
[![Leverage](https://img.shields.io/badge/leverage-10x-red.svg)](https://github.com/MeViksry/SupertrendSniperPro)
[![Timeframe](https://img.shields.io/badge/timeframe-15m-blueviolet.svg)](https://github.com/MeViksry/SupertrendSniperPro)
[![Win Rate](https://img.shields.io/badge/win%20rate-78%25%2B-success.svg)](https://github.com/MeViksry/SupertrendSniperPro)

> Advanced algorithmic trading strategy for cryptocurrency futures markets using multi-indicator technical analysis and machine learning-inspired filtering.

## Overview

**SupertrendSniperPro** is a sophisticated automated trading strategy designed for high-frequency futures scalping on cryptocurrency markets. Built on the Freqtrade framework, it combines multiple technical indicators with advanced entry/exit logic to achieve consistent profitability.

### Key Features

- **Multi-Indicator Confluence**: 10+ technical indicators for entry validation
- **Futures Trading**: Support for both LONG and SHORT positions
- **High Leverage**: Optimized for 10x leverage scalping
- **Heikin Ashi Filtering**: Noise reduction for cleaner signals
- **Webhook Integration**: Real-time alerts for copy trading platforms
- **Dynamic Risk Management**: Adaptive position sizing and trailing stops
- **Multi-Coin Support**: Trade 25+ cryptocurrency pairs simultaneously

## Performance Metrics

| Metric | Target | Notes |
|--------|--------|-------|
| **Win Rate** | 78%+ | After hyperparameter optimization |
| **Profit Factor** | 2.5+ | Total gains divided by total losses |
| **Sharpe Ratio** | 2.0+ | Risk-adjusted return metric |
| **Max Drawdown** | <10% | Worst peak-to-trough decline |
| **Average Trade Duration** | 15-60 min | Scalping timeframe |
| **Daily Profit Target** | 5-10% | 50-100% actual with 10x leverage |

## Technical Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![TA-Lib](https://img.shields.io/badge/TA--Lib-000000?style=for-the-badge&logo=chartdotjs&logoColor=white)

### Dependencies

```
freqtrade >= 2024.1
pandas-ta >= 0.3.14
ta-lib >= 0.4.25
technical >= 1.4.0
python >= 3.9
```

## Strategy Components

### Technical Indicators

<details>
<summary>Click to expand indicator list</summary>

1. **HMA (Hull Moving Average)** - Primary trend detection
2. **Supertrend** - Dynamic support/resistance levels
3. **Heikin Ashi** - Candlestick noise filtering
4. **RSI (Relative Strength Index)** - Momentum oscillator
5. **ADX (Average Directional Index)** - Trend strength measurement
6. **MACD (Moving Average Convergence Divergence)** - Trend following
7. **Stochastic Oscillator** - Overbought/oversold conditions
8. **EMA (Exponential Moving Average)** - Fast/slow trend alignment
9. **Volume Analysis** - Institutional activity detection
10. **Bollinger Bands** - Volatility measurement
11. **ATR (Average True Range)** - Dynamic stop loss calculation

</details>

### Entry Logic

**LONG Position Requirements** (All conditions must be TRUE):

```python
1. HMA Rising (primary uptrend)
2. Supertrend Bullish (direction = 1)
3. Price > EMA Fast AND Price > EMA Slow
4. EMA Fast > EMA Slow (trend alignment)
5. RSI between 45-65 (momentum sweet spot)
6. ADX > 20 (sufficient trend strength)
7. Volume > 1.3x average (institutional confirmation)
8. MACD Histogram Positive
9. Heikin Ashi Bullish Candle
10. Stochastic < 80 (room to rise)
11. Bollinger Band Width > 2% (not choppy)
```

**SHORT Position Requirements** (Mirror logic of LONG)

### Exit Logic

Positions are closed when ANY of these conditions trigger:

```python
- Supertrend direction flip (primary signal)
- RSI extreme levels (>70 LONG, <30 SHORT)
- Choppy market detection (conflicting indicators)
- MACD bearish/bullish crossover
- Price crosses EMA Fast (trend break)
- ROI target achieved (3% = 30% with 10x)
- Stop loss hit (-1.5% = -15% with 10x)
- Trailing stop triggered (lock in profits)
```

## Installation

### Prerequisites

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv git build-essential

# Install TA-Lib
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make
sudo make install
cd ..
rm -rf ta-lib*
```

### Freqtrade Setup

```bash
# Clone Freqtrade
git clone https://github.com/freqtrade/freqtrade.git
cd freqtrade

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Freqtrade
pip install -e .

# Install additional dependencies
pip install pandas-ta technical
```

### Strategy Installation

```bash
# Clone this repository
git clone https://github.com/MeViksry/SupertrendSniperPro.git
cd SupertrendSniperPro

# Copy strategy files
cp SupertrendSniperPro.py ../freqtrade/user_data/strategies/
cp config_supertrend_sniper_pro.json ../freqtrade/user_data/
cp test_supertrend_pro.sh ../freqtrade/
chmod +x ../freqtrade/test_supertrend_pro.sh
```

## Configuration

### Exchange API Setup

Edit `config_supertrend_sniper_pro.json`:

```json
{
    "exchange": {
        "name": "binance",
        "key": "YOUR_API_KEY",
        "secret": "YOUR_API_SECRET"
    }
}
```

**Required API Permissions:**
- Enable Reading
- Enable Futures Trading
- **Disable Withdrawals** (security)
- Enable IP Whitelist (recommended)

### Leverage Configuration

All pairs are configured for 10x leverage in isolated margin mode:

```json
{
    "trading_mode": "futures",
    "margin_mode": "isolated",
    "leverage": {
        "BTC/USDT:USDT": 10,
        "ETH/USDT:USDT": 10,
        ...
    }
}
```

### Webhook Integration

Configure webhook for copy trading platforms:

```json
{
    "webhook": {
        "enabled": true,
        "url": "https://your-platform.com/api/webhook",
        "webhookentry": {
            "action": "open",
            "pair": "{pair}",
            "side": "{side}",
            "leverage": "{leverage}",
            "open_rate": "{open_rate}"
        }
    }
}
```

## Usage

### Backtesting

```bash
# Download historical data
freqtrade download-data \
    --config user_data/config_supertrend_sniper_pro.json \
    --timerange 20240101- \
    --timeframe 15m \
    --trading-mode futures

# Run backtest
freqtrade backtesting \
    --config user_data/config_supertrend_sniper_pro.json \
    --strategy SupertrendSniperPro \
    --timerange 20240101-20260129
```

### Hyperparameter Optimization

```bash
# Optimize entry parameters
freqtrade hyperopt \
    --config user_data/config_supertrend_sniper_pro.json \
    --strategy SupertrendSniperPro \
    --hyperopt-loss SharpeHyperOptLoss \
    --spaces buy \
    --epochs 500

# Optimize exit parameters
freqtrade hyperopt \
    --config user_data/config_supertrend_sniper_pro.json \
    --strategy SupertrendSniperPro \
    --hyperopt-loss SharpeHyperOptLoss \
    --spaces sell roi stoploss \
    --epochs 300
```

### Dry Run Testing

**MANDATORY: Test for minimum 1 week before live trading**

```bash
freqtrade trade \
    --config user_data/config_supertrend_sniper_pro.json \
    --strategy SupertrendSniperPro \
    --dry-run
```

### Live Trading

```bash
# Update config: set "dry_run": false
# Add real API keys

freqtrade trade \
    --config user_data/config_supertrend_sniper_pro.json \
    --strategy SupertrendSniperPro
```

## Risk Management

### Position Sizing

```
Max Open Trades: 8
Position Size: Dynamic (99% / open trades)
Risk Per Trade: 1-2% of capital
Stop Loss: -1.5% (-15% actual with 10x)
Take Profit: +3% (+30% actual with 10x)
```

### Daily Limits

| Condition | Action |
|-----------|--------|
| Daily Loss > 5% | Stop trading immediately |
| Daily Profit > 10% | Withdraw profits |
| 3 Consecutive Losses | Reduce position size 50% |
| 5 Consecutive Losses | Stop trading for the day |

### Leverage Warning

![Warning](https://img.shields.io/badge/WARNING-High%20Risk-red?style=for-the-badge)

**10x leverage amplifies both gains and losses:**
- +1% price move = +10% account change
- Can liquidate account in single bad trade
- Only use capital you can afford to lose
- Monitor positions every 30-60 minutes
- Always use stop loss orders

## Monitoring

### Command Line

```bash
# Check current status
freqtrade status

# View profit/loss
freqtrade profit

# Show recent trades
freqtrade show-trades --limit 10

# Monitor logs
tail -f user_data/logs/freqtrade.log
```

### Web UI (FreqUI)

Access at `http://localhost:8080`

Default credentials:
- Username: `freqtrader`
- Password: (set in config)

### Telegram Bot

Enable notifications:

```json
{
    "telegram": {
        "enabled": true,
        "token": "YOUR_BOT_TOKEN",
        "chat_id": "YOUR_CHAT_ID"
    }
}
```

Available commands:
- `/status` - Current open trades
- `/profit` - Overall profit/loss
- `/balance` - Account balance
- `/performance` - Win rate statistics
- `/forceexit <id>` - Force close trade

## Repository Structure

```
SupertrendSniperPro/
├── SupertrendSniperPro.py          # Main strategy file
├── config_supertrend_sniper_pro.json  # Configuration file
├── test_supertrend_pro.sh          # Automated testing suite
├── README.md                        # This file
├── SCALPING_GUIDE_10X.md           # Detailed scalping guide
├── CHEATSHEET_SupertrendSniperPro.md  # Quick reference
├── WEBHOOK_GUIDE.md                # Webhook integration guide
├── PACKAGE_SUMMARY.md              # Package overview
└── LICENSE                         # MIT License
```

## Documentation

- **[Scalping Guide](SCALPING_GUIDE_10X.md)** - Complete guide for 10x leverage scalping
- **[Cheatsheet](CHEATSHEET_SupertrendSniperPro.md)** - Quick reference for daily operations
- **[Webhook Guide](WEBHOOK_GUIDE.md)** - Integration with copy trading platforms
- **[Freqtrade Docs](https://www.freqtrade.io/en/stable/)** - Official Freqtrade documentation

## Supported Exchanges

![Binance](https://img.shields.io/badge/Binance-FCD535?style=for-the-badge&logo=binance&logoColor=white)
![Bybit](https://img.shields.io/badge/Bybit-000000?style=for-the-badge&logo=bybit&logoColor=white)
![OKX](https://img.shields.io/badge/OKX-000000?style=for-the-badge&logo=okx&logoColor=white)

Primary testing on Binance Futures. Other exchanges supported by Freqtrade should work with minor configuration adjustments.

## Supported Trading Pairs

Top volume pairs optimized for scalping:

```
BTC/USDT:USDT    ETH/USDT:USDT    BNB/USDT:USDT    SOL/USDT:USDT
XRP/USDT:USDT    ADA/USDT:USDT    AVAX/USDT:USDT   DOT/USDT:USDT
MATIC/USDT:USDT  LINK/USDT:USDT   UNI/USDT:USDT    ATOM/USDT:USDT
LTC/USDT:USDT    NEAR/USDT:USDT   APT/USDT:USDT    ARB/USDT:USDT
OP/USDT:USDT     INJ/USDT:USDT    SUI/USDT:USDT    TIA/USDT:USDT
DOGE/USDT:USDT   SHIB/USDT:USDT   PEPE/USDT:USDT   WIF/USDT:USDT
FET/USDT:USDT
```

Dynamic pairlist filters ensure only high-volume, stable pairs are traded.

## Troubleshooting

### Common Issues

**No trades being placed:**
```bash
# Check pairlist
freqtrade test-pairlist --config user_data/config_supertrend_sniper_pro.json

# Lower entry thresholds temporarily
# Edit SupertrendSniperPro.py: adx_threshold = 20 (from 25)
```

**Strategy not loading:**
```bash
# Verify dependencies
pip install pandas-ta ta-lib technical

# Check Python syntax
python -m py_compile user_data/strategies/SupertrendSniperPro.py
```

**Webhook errors:**
```bash
# Test webhook manually
curl -X POST "YOUR_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'

# Check logs
grep "webhook" user_data/logs/freqtrade.log
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Testing

```bash
# Run automated test suite
./test_supertrend_pro.sh

# Select option 11 for complete test suite
```

Test coverage includes:
- Strategy validation
- Backtesting (1+ year data)
- Multi-pair analysis
- Performance benchmarks
- Webhook integration

## Changelog

### Version 1.0.0 (2026-01-29)

- Initial release
- Multi-indicator strategy implementation
- Heikin Ashi filtering
- 10x leverage optimization
- Webhook integration for copy trading
- 25+ cryptocurrency pair support
- Comprehensive documentation

## Roadmap

- [ ] Machine learning integration for entry optimization
- [ ] Multi-timeframe analysis
- [ ] Advanced portfolio rebalancing
- [ ] Custom indicators development
- [ ] Backtesting strategy comparison tool
- [ ] Real-time performance dashboard
- [ ] Mobile app notifications
- [ ] Additional exchange integrations

## Performance Disclaimer

![Disclaimer](https://img.shields.io/badge/DISCLAIMER-Read%20Carefully-critical?style=for-the-badge)

**IMPORTANT LEGAL NOTICE:**

- This software is provided for educational and research purposes only
- Past performance is not indicative of future results
- Trading cryptocurrencies involves substantial risk of loss
- 10x leverage can result in rapid and significant losses
- Never invest more than you can afford to lose completely
- The authors are not responsible for any financial losses
- This is not financial advice - consult a professional advisor
- Always test thoroughly in dry run mode before live trading
- Cryptocurrency markets are highly volatile and unpredictable
- No warranty or guarantee of profitability is provided

**USE AT YOUR OWN RISK**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 MeViksry

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Acknowledgments

- **Freqtrade Team** - Excellent algorithmic trading framework
- **Technical Indicators Community** - TA-Lib and pandas-ta libraries
- **Cryptocurrency Trading Community** - Strategy insights and best practices

## Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/MeViksry/SupertrendSniperPro/issues)
- **Discussions**: [Ask questions or share ideas](https://github.com/MeViksry/SupertrendSniperPro/discussions)
- **Freqtrade Discord**: [Community support](https://discord.gg/freqtrade)
- **Freqtrade Documentation**: [Official docs](https://www.freqtrade.io/en/stable/)

## Contact

**Repository**: [https://github.com/MeViksry/SupertrendSniperPro](https://github.com/MeViksry/SupertrendSniperPro)

---

**Star this repository if you find it helpful!**

[![GitHub stars](https://img.shields.io/github/stars/MeViksry/SupertrendSniperPro?style=social)](https://github.com/MeViksry/SupertrendSniperPro/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/MeViksry/SupertrendSniperPro?style=social)](https://github.com/MeViksry/SupertrendSniperPro/network/members)
[![GitHub watchers](https://img.shields.io/github/watchers/MeViksry/SupertrendSniperPro?style=social)](https://github.com/MeViksry/SupertrendSniperPro/watchers)

**Made with Python and passion for algorithmic trading**