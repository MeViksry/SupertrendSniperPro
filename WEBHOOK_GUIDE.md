# 🔗 Webhook Integration Guide for Copy Trading

## Overview

SupertrendSniperPro mengirim real-time alerts dalam format JSON ke webhook URL Anda setiap kali terjadi:
- ✅ Entry signal (open position)
- ✅ Exit signal (close position)
- ✅ Order fill confirmation
- ✅ Order cancellation
- ✅ Bot status changes

## Webhook URL Configuration

Edit `config_supertrend_sniper_pro.json`:

```json
{
    "webhook": {
        "enabled": true,
        "url": "https://your-copy-trading-platform.com/api/webhook",
        "format": "json",
        "retries": 3,
        "retry_delay": 0.5
    }
}
```

---

## Payload Examples

### 1. ENTRY SIGNAL (Long Position)

**Trigger:** Strategy generates buy signal

```json
{
    "action": "entry",
    "exchange": "binance",
    "pair": "BTC/USDT",
    "leverage": "2",
    "direction": "long",
    "stake_amount": "100.00",
    "stake_currency": "USDT",
    "price": "50000.00",
    "timestamp": "2026-01-29T10:30:00Z",
    "strategy": "SupertrendSniperPro",
    "enter_tag": "hma_supertrend_long"
}
```

**Fields:**
- `action`: Always "entry" for new positions
- `exchange`: Exchange name (binance, bybit, etc)
- `pair`: Trading pair (BTC/USDT, ETH/USDT, etc)
- `leverage`: Leverage used (1, 2, 3, etc)
- `direction`: "long" or "short"
- `stake_amount`: Capital allocated to this trade
- `stake_currency`: Currency used (USDT, BUSD, etc)
- `price`: Entry price
- `timestamp`: ISO 8601 format timestamp
- `strategy`: Strategy name
- `enter_tag`: Entry reason tag

---

### 2. ENTRY FILL (Order Executed)

**Trigger:** Entry order successfully filled

```json
{
    "action": "entry_fill",
    "pair": "BTC/USDT",
    "amount": "0.002",
    "price": "50000.00",
    "timestamp": "2026-01-29T10:30:15Z"
}
```

---

### 3. EXIT SIGNAL (Close Position)

**Trigger:** Strategy generates sell signal

```json
{
    "action": "exit",
    "exchange": "binance",
    "pair": "BTC/USDT",
    "direction": "long",
    "amount": "0.002",
    "price": "51500.00",
    "profit_ratio": "0.03",
    "profit_amount": "3.00",
    "profit_abs": "3.00",
    "exit_reason": "exit_signal_long",
    "timestamp": "2026-01-29T11:00:00Z",
    "duration": "30 minutes",
    "strategy": "SupertrendSniperPro",
    "exit_tag": "exit_signal_long"
}
```

**Fields:**
- `action`: Always "exit" for closing positions
- `amount`: Position size being closed
- `price`: Exit price
- `profit_ratio`: Profit as percentage (0.03 = 3%)
- `profit_amount`: Profit in stake currency
- `profit_abs`: Absolute profit (same as profit_amount)
- `exit_reason`: Why position was closed
- `duration`: How long trade was open

---

### 4. EXIT FILL (Position Closed)

**Trigger:** Exit order successfully filled

```json
{
    "action": "exit_fill",
    "pair": "BTC/USDT",
    "amount": "0.002",
    "price": "51500.00",
    "profit_ratio": "0.03",
    "timestamp": "2026-01-29T11:00:15Z"
}
```

---

### 5. ENTRY CANCEL

**Trigger:** Entry order cancelled (timeout, insufficient funds, etc)

```json
{
    "action": "entry_cancel",
    "pair": "BTC/USDT",
    "reason": "timeout",
    "timestamp": "2026-01-29T10:35:00Z"
}
```

---

### 6. EXIT CANCEL

**Trigger:** Exit order cancelled

```json
{
    "action": "exit_cancel",
    "pair": "BTC/USDT",
    "reason": "insufficient_balance",
    "timestamp": "2026-01-29T11:05:00Z"
}
```

---

### 7. STATUS UPDATE

**Trigger:** Bot status changes

```json
{
    "action": "status",
    "status": "running",
    "timestamp": "2026-01-29T09:00:00Z"
}
```

Possible status values:
- `running` - Bot is active
- `stopped` - Bot was stopped
- `reloading` - Bot is reloading config

---

## Copy Trading Platform Integration

### Example 1: Basic Node.js Webhook Server

```javascript
const express = require('express');
const app = express();

app.use(express.json());

// Webhook endpoint
app.post('/api/webhook', async (req, res) => {
    const signal = req.body;
    
    console.log('Received signal:', signal);
    
    try {
        if (signal.action === 'entry') {
            await openPosition(signal);
        } else if (signal.action === 'exit') {
            await closePosition(signal);
        }
        
        res.status(200).json({ success: true });
    } catch (error) {
        console.error('Error processing signal:', error);
        res.status(500).json({ success: false, error: error.message });
    }
});

async function openPosition(signal) {
    // Your logic to open position on copy trading platform
    console.log(`Opening ${signal.direction} position on ${signal.pair}`);
    console.log(`Amount: ${signal.stake_amount} ${signal.stake_currency}`);
    console.log(`Price: ${signal.price}`);
    console.log(`Leverage: ${signal.leverage}x`);
    
    // Example API call to your exchange
    // await exchange.createOrder(signal.pair, 'market', signal.direction, amount);
}

async function closePosition(signal) {
    // Your logic to close position on copy trading platform
    console.log(`Closing ${signal.direction} position on ${signal.pair}`);
    console.log(`Exit price: ${signal.price}`);
    console.log(`Profit: ${signal.profit_ratio * 100}%`);
    
    // Example API call to your exchange
    // await exchange.closePosition(signal.pair);
}

app.listen(3000, () => {
    console.log('Webhook server running on port 3000');
});
```

---

### Example 2: Python Flask Webhook Server

```python
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/api/webhook', methods=['POST'])
def webhook():
    signal = request.json
    logging.info(f"Received signal: {signal}")
    
    try:
        if signal['action'] == 'entry':
            open_position(signal)
        elif signal['action'] == 'exit':
            close_position(signal)
        
        return jsonify({'success': True}), 200
    except Exception as e:
        logging.error(f"Error processing signal: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

def open_position(signal):
    """Open position on copy trading platform"""
    logging.info(f"Opening {signal['direction']} position on {signal['pair']}")
    logging.info(f"Amount: {signal['stake_amount']} {signal['stake_currency']}")
    logging.info(f"Price: {signal['price']}")
    logging.info(f"Leverage: {signal['leverage']}x")
    
    # Your API integration here
    # exchange.create_order(signal['pair'], 'market', signal['direction'], amount)

def close_position(signal):
    """Close position on copy trading platform"""
    logging.info(f"Closing {signal['direction']} position on {signal['pair']}")
    logging.info(f"Exit price: {signal['price']}")
    logging.info(f"Profit: {float(signal['profit_ratio']) * 100}%")
    
    # Your API integration here
    # exchange.close_position(signal['pair'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
```

---

## Testing Webhook

### Test dengan cURL

```bash
# Test entry signal
curl -X POST "https://your-webhook-url.com/api/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "entry",
    "exchange": "binance",
    "pair": "BTC/USDT",
    "leverage": "2",
    "direction": "long",
    "stake_amount": "100.00",
    "stake_currency": "USDT",
    "price": "50000.00",
    "timestamp": "2026-01-29T10:30:00Z",
    "strategy": "SupertrendSniperPro",
    "enter_tag": "hma_supertrend_long"
  }'

# Test exit signal
curl -X POST "https://your-webhook-url.com/api/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "exit",
    "exchange": "binance",
    "pair": "BTC/USDT",
    "direction": "long",
    "amount": "0.002",
    "price": "51500.00",
    "profit_ratio": "0.03",
    "profit_amount": "3.00",
    "exit_reason": "exit_signal_long",
    "timestamp": "2026-01-29T11:00:00Z",
    "duration": "30 minutes",
    "strategy": "SupertrendSniperPro"
  }'
```

### Test dengan Postman

1. Create new POST request
2. URL: `https://your-webhook-url.com/api/webhook`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON): Copy payload examples above
5. Send request
6. Check response: Should return `{"success": true}`

---

## Security Best Practices

### 1. Verify Webhook Signature

```python
import hmac
import hashlib

SECRET_KEY = 'your-secret-key'

def verify_signature(payload, signature):
    """Verify webhook came from authorized source"""
    expected = hmac.new(
        SECRET_KEY.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)

@app.route('/api/webhook', methods=['POST'])
def webhook():
    signature = request.headers.get('X-Signature')
    payload = request.data.decode()
    
    if not verify_signature(payload, signature):
        return jsonify({'error': 'Invalid signature'}), 401
    
    # Process webhook...
```

### 2. Use HTTPS

Always use HTTPS for webhook URL:
- ✅ `https://your-domain.com/webhook`
- ❌ `http://your-domain.com/webhook`

### 3. Rate Limiting

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/webhook', methods=['POST'])
@limiter.limit("100 per minute")
def webhook():
    # Process webhook...
```

### 4. IP Whitelist

```python
ALLOWED_IPS = ['your.server.ip.address']

@app.route('/api/webhook', methods=['POST'])
def webhook():
    if request.remote_addr not in ALLOWED_IPS:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Process webhook...
```

---

## Popular Copy Trading Platforms

### 1. TradingView Alerts
Convert to TradingView alert format:
```
{{strategy.order.action}} {{ticker}} @ {{strategy.order.price}}
Profit: {{strategy.position_avg_price}}
```

### 2. 3Commas
Use 3Commas webhook format:
```json
{
    "message_type": "bot",
    "bot_id": "YOUR_BOT_ID",
    "email_token": "YOUR_EMAIL_TOKEN",
    "delay_seconds": 0,
    "pair": "BTC_USDT",
    "action": "{{action}}"
}
```

### 3. Cornix
Format for Cornix Telegram bot:
```
Exchange: Binance Futures
Signal: {{direction}}
Pair: {{pair}}
Entry: {{price}}
Leverage: {{leverage}}x
```

---

## Monitoring Webhooks

### Check Webhook Logs

```bash
# Freqtrade logs
tail -f user_data/logs/freqtrade.log | grep webhook

# Filter for webhook errors
grep "webhook" user_data/logs/freqtrade.log | grep -i "error"
```

### Webhook Statistics

Track in your webhook server:
- Total signals received
- Success rate
- Average processing time
- Failed signals
- Retry attempts

Example:
```python
webhook_stats = {
    'total': 0,
    'success': 0,
    'failed': 0,
    'avg_time': 0
}

@app.route('/api/webhook', methods=['POST'])
def webhook():
    start_time = time.time()
    webhook_stats['total'] += 1
    
    try:
        # Process webhook...
        webhook_stats['success'] += 1
    except:
        webhook_stats['failed'] += 1
    
    processing_time = time.time() - start_time
    webhook_stats['avg_time'] = (webhook_stats['avg_time'] + processing_time) / 2
```

---

## Troubleshooting

### Webhook Not Sending

1. Check config:
```json
"webhook": {
    "enabled": true,  // Must be true!
    "url": "..."      // Must be valid URL
}
```

2. Check logs:
```bash
tail -f user_data/logs/freqtrade.log | grep webhook
```

3. Test URL manually:
```bash
curl -X POST "YOUR_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

### Webhook Timeout

Increase timeout in config:
```json
"webhook": {
    "enabled": true,
    "url": "...",
    "timeout": 10  // seconds
}
```

### Webhook Retries

Configure retry behavior:
```json
"webhook": {
    "enabled": true,
    "url": "...",
    "retries": 3,
    "retry_delay": 0.5
}
```

---

## Production Deployment

### Use Queue System (Recommended)

For high-frequency trading, use message queue:

```python
import redis
from rq import Queue

redis_conn = redis.Redis()
q = Queue(connection=redis_conn)

@app.route('/api/webhook', methods=['POST'])
def webhook():
    signal = request.json
    # Add to queue for async processing
    q.enqueue(process_signal, signal)
    return jsonify({'success': True, 'queued': True}), 202

def process_signal(signal):
    # Process in background worker
    if signal['action'] == 'entry':
        open_position(signal)
    elif signal['action'] == 'exit':
        close_position(signal)
```

### Use Database for Persistence

```python
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Signal(Base):
    __tablename__ = 'signals'
    id = Column(Integer, primary_key=True)
    action = Column(String)
    pair = Column(String)
    price = Column(Float)
    timestamp = Column(DateTime)
    processed = Column(Integer, default=0)

@app.route('/api/webhook', methods=['POST'])
def webhook():
    signal = request.json
    
    # Save to database
    db_signal = Signal(
        action=signal['action'],
        pair=signal['pair'],
        price=signal['price'],
        timestamp=datetime.fromisoformat(signal['timestamp'])
    )
    session.add(db_signal)
    session.commit()
    
    return jsonify({'success': True}), 200
```

---

## 🎯 Best Practices

1. ✅ **Always use HTTPS**
2. ✅ **Implement authentication**
3. ✅ **Log all webhooks**
4. ✅ **Handle errors gracefully**
5. ✅ **Use async processing**
6. ✅ **Validate payload format**
7. ✅ **Monitor webhook health**
8. ✅ **Set timeouts**
9. ✅ **Implement retries**
10. ✅ **Test thoroughly before live**

---

**Need Help?**
- Discord: https://discord.gg/freqtrade
- Docs: https://www.freqtrade.io/en/stable/webhooks/
- GitHub: https://github.com/freqtrade/freqtrade

---

*Happy Copy Trading! 🚀*
