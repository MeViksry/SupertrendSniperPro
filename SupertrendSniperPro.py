# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these imports ---
import numpy as np
import pandas as pd
from datetime import datetime, timezone
from pandas import DataFrame
from typing import Optional, Union

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,
                                IntParameter, IStrategy, merge_informative_pair)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import pandas_ta as pta
from technical import qtpylib


class SupertrendSniperPro(IStrategy):
    """
    /$$      /$$ /$$$$$$$$       /$$    /$$ /$$$$$$ /$$   /$$  /$$$$$$  /$$$$$$$  /$$     /$$
   | $$$    /$$$| $$_____/      | $$   | $$|_  $$_/| $$  /$$/ /$$__  $$| $$__  $$|  $$   /$$/
   | $$$$  /$$$$| $$            | $$   | $$  | $$  | $$ /$$/ | $$  \__/| $$  \ $$ \  $$ /$$/ 
   | $$ $$/$$ $$| $$$$$         |  $$ / $$/  | $$  | $$$$$/  |  $$$$$$ | $$$$$$$/  \  $$$$/  
   | $$  $$$| $$| $$__/          \  $$ $$/   | $$  | $$  $$   \____  $$| $$__  $$   \  $$/   
   | $$\  $ | $$| $$              \  $$$/    | $$  | $$\  $$  /$$  \ $$| $$  \ $$    | $$    
   | $$ \/  | $$| $$$$$$$$         \  $/    /$$$$$$| $$ \  $$|  $$$$$$/| $$  | $$    | $$    
   |__/     |__/|________/          \_/    |______/|__/  \__/ \______/ |__/  |__/    |__/    
                                                                                          
                                                                                          
                                                                                          
    🚀 SupertrendSniperPro - Advanced Futures Scalping Strategy
    
    Trading Mode: FUTURES (Long & Short)
    Timeframe: 15 minutes (scalping)
    Leverage: 10x (aggressive scalping)
    
    Combines:
    - HMA (Hull Moving Average) for trend direction
    - Supertrend for dynamic support/resistance
    - Heikin Ashi candles for noise filtering
    - RSI for momentum confirmation
    - ADX for trend strength
    - Volume confirmation
    - EMA filters for additional trend validation
    
    Target: 78%+ Win Rate with optimal R:R ratio
    Multi-coin support with dynamic position sizing
    Webhook alerts for copy trading integration
    """

    INTERFACE_VERSION = 3

    # ============================================
    # STRATEGY METADATA
    # ============================================
    
    can_short: bool = True  # Enable SHORT positions for futures
    
    # Timeframe for scalping
    timeframe = '15m'
    
    # Startup candle count
    startup_candle_count: int = 100
    
    # ============================================
    # POSITION MANAGEMENT - SCALPING OPTIMIZED
    # ============================================
    
    # ROI table - Quick scalping profits with 10x leverage
    minimal_roi = {
        "0": 0.03,      # 3% = 30% with 10x leverage (main target)
        "15": 0.02,     # After 15 min, take 2% = 20% actual
        "30": 0.015,    # After 30 min, take 1.5% = 15% actual
        "45": 0.01,     # After 45 min, take 1% = 10% actual
        "60": 0.008     # After 1 hour, take 0.8% = 8% actual
    }

    # Stoploss - Tight for scalping with 10x leverage
    stoploss = -0.015  # -1.5% = -15% actual loss with 10x leverage

    # Trailing stop - Lock in profits quickly
    trailing_stop = True
    trailing_stop_positive = 0.008  # Start trailing at 0.8% = 8% actual
    trailing_stop_positive_offset = 0.012  # Trail 1.2% below peak
    trailing_only_offset_is_reached = True

    # ============================================
    # HYPEROPTABLE PARAMETERS - SCALPING OPTIMIZED
    # ============================================
    
    # HMA Parameters - Faster for scalping
    hma_length = IntParameter(20, 50, default=30, space='buy', optimize=True)
    
    # Supertrend Parameters - Tighter for scalping
    supertrend_period = IntParameter(5, 12, default=8, space='buy', optimize=True)
    supertrend_multiplier = DecimalParameter(1.5, 3.0, default=2.5, decimals=1, space='buy', optimize=True)
    
    # RSI Parameters - More responsive
    rsi_period = IntParameter(7, 14, default=10, space='buy', optimize=True)
    rsi_buy_threshold = IntParameter(40, 55, default=45, space='buy', optimize=True)
    rsi_sell_threshold = IntParameter(60, 80, default=70, space='sell', optimize=True)
    
    # ADX Parameters (Trend Strength) - Lower threshold for scalping
    adx_period = IntParameter(10, 20, default=14, space='buy', optimize=True)
    adx_threshold = IntParameter(15, 30, default=20, space='buy', optimize=True)
    
    # Volume Parameters - More aggressive
    volume_factor = DecimalParameter(1.0, 2.0, default=1.3, decimals=1, space='buy', optimize=True)
    
    # EMA Filters - Faster for scalping
    ema_fast = IntParameter(10, 25, default=15, space='buy', optimize=True)
    ema_slow = IntParameter(30, 60, default=40, space='buy', optimize=True)
    
    # Exit on choppy market
    exit_on_choppy = BooleanParameter(default=True, space='sell', optimize=False)
    
    # ============================================
    # WEBHOOK CONFIGURATION
    # ============================================
    
    # Set this to your webhook URL in config.json under "webhook" section
    # Example config addition:
    # "webhook": {
    #     "enabled": true,
    #     "url": "https://your-copy-trading-platform.com/webhook",
    #     "webhookentry": {
    #         "value1": "{pair}",
    #         "value2": "{stake_amount}",
    #         "value3": "{enter_tag}"
    #     },
    #     "webhookexit": {
    #         "value1": "{pair}",
    #         "value2": "{profit_amount}",
    #         "value3": "{exit_reason}"
    #     }
    # }

    # ============================================
    # INFORMATIVE PAIRS
    # ============================================
    
    def informative_pairs(self):
        """
        Define additional pairs to download
        """
        return []

    # ============================================
    # INDICATOR POPULATION
    # ============================================
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Generate all indicators needed for entry and exit conditions
        """
        
        # ===== HEIKIN ASHI CANDLES =====
        # Convert to Heikin Ashi for smoother price action
        heikinashi = qtpylib.heikinashi(dataframe)
        dataframe['ha_open'] = heikinashi['open']
        dataframe['ha_close'] = heikinashi['close']
        dataframe['ha_high'] = heikinashi['high']
        dataframe['ha_low'] = heikinashi['low']
        
        # ===== HULL MOVING AVERAGE (HMA) =====
        # Primary trend indicator
        dataframe['hma'] = pta.hma(dataframe['close'], length=self.hma_length.value)
        dataframe['hma_rising'] = dataframe['hma'] > dataframe['hma'].shift(1)
        dataframe['hma_falling'] = dataframe['hma'] < dataframe['hma'].shift(1)
        
        # ===== SUPERTREND =====
        # Dynamic support/resistance
        supertrend = pta.supertrend(
            dataframe['ha_high'],  # Use Heikin Ashi for smoother signals
            dataframe['ha_low'],
            dataframe['ha_close'],
            length=self.supertrend_period.value,
            multiplier=self.supertrend_multiplier.value
        )
        dataframe['supertrend'] = supertrend[f'SUPERT_{self.supertrend_period.value}_{self.supertrend_multiplier.value}']
        dataframe['supertrend_direction'] = supertrend[f'SUPERTd_{self.supertrend_period.value}_{self.supertrend_multiplier.value}']
        
        # ===== RSI (Relative Strength Index) =====
        # Momentum oscillator
        dataframe['rsi'] = ta.RSI(dataframe['close'], timeperiod=self.rsi_period.value)
        
        # ===== ADX (Average Directional Index) =====
        # Trend strength indicator
        dataframe['adx'] = ta.ADX(dataframe['high'], dataframe['low'], dataframe['close'], timeperiod=self.adx_period.value)
        
        # ===== EMA (Exponential Moving Averages) =====
        # Additional trend filters
        dataframe['ema_fast'] = ta.EMA(dataframe['close'], timeperiod=self.ema_fast.value)
        dataframe['ema_slow'] = ta.EMA(dataframe['close'], timeperiod=self.ema_slow.value)
        
        # ===== VOLUME =====
        # Volume confirmation
        dataframe['volume_mean'] = dataframe['volume'].rolling(window=20).mean()
        dataframe['volume_surge'] = dataframe['volume'] > (dataframe['volume_mean'] * self.volume_factor.value)
        
        # ===== BOLLINGER BANDS =====
        # Volatility indicator (for choppy market detection)
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lower'] = bollinger['lower']
        dataframe['bb_middle'] = bollinger['mid']
        dataframe['bb_upper'] = bollinger['upper']
        dataframe['bb_width'] = ((dataframe['bb_upper'] - dataframe['bb_lower']) / dataframe['bb_middle']) * 100
        
        # ===== ATR (Average True Range) =====
        # For position sizing and stop loss
        dataframe['atr'] = ta.ATR(dataframe['high'], dataframe['low'], dataframe['close'], timeperiod=14)
        
        # ===== MACD =====
        # Additional momentum confirmation
        macd = ta.MACD(dataframe['close'])
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']
        
        # ===== STOCHASTIC =====
        # Overbought/oversold confirmation
        stoch = ta.STOCH(dataframe['high'], dataframe['low'], dataframe['close'])
        dataframe['stoch_k'] = stoch['slowk']
        dataframe['stoch_d'] = stoch['slowd']
        
        # ===== MARKET CONDITIONS =====
        # Bullish: HMA rising + Supertrend bullish
        dataframe['is_bullish'] = (
            dataframe['hma_rising'] & 
            (dataframe['supertrend_direction'] == 1)
        )
        
        # Bearish: HMA falling + Supertrend bearish
        dataframe['is_bearish'] = (
            dataframe['hma_falling'] & 
            (dataframe['supertrend_direction'] == -1)
        )
        
        # Choppy: HMA and Supertrend disagree
        dataframe['is_choppy'] = (
            (dataframe['hma_rising'] & (dataframe['supertrend_direction'] == -1)) |
            (dataframe['hma_falling'] & (dataframe['supertrend_direction'] == 1))
        )
        
        return dataframe

    # ============================================
    # ENTRY CONDITIONS (LONG)
    # ============================================
    
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        LONG ENTRY CONDITIONS - Multi-layer confirmation for high win rate
        
        Requirements for LONG:
        1. HMA is rising (primary trend)
        2. Supertrend is bullish (direction = 1)
        3. Price is above EMA fast (short-term trend alignment)
        4. RSI > threshold (not oversold, has momentum)
        5. ADX > threshold (strong trend, not ranging)
        6. Volume surge (institutional interest)
        7. MACD histogram positive (momentum confirmation)
        8. Price above EMA slow (long-term trend alignment)
        9. Heikin Ashi candle is bullish
        10. Stochastic not overbought (room to run)
        """
        
        dataframe.loc[
            (
                # Primary conditions
                (dataframe['is_bullish']) &
                (dataframe['hma_rising']) &
                (dataframe['supertrend_direction'] == 1) &
                
                # Trend alignment
                (dataframe['close'] > dataframe['ema_fast']) &
                (dataframe['close'] > dataframe['ema_slow']) &
                (dataframe['ema_fast'] > dataframe['ema_slow']) &
                
                # Momentum confirmation
                (dataframe['rsi'] > self.rsi_buy_threshold.value) &
                (dataframe['rsi'] < 70) &  # Not overbought yet
                (dataframe['adx'] > self.adx_threshold.value) &
                
                # Volume confirmation
                (dataframe['volume_surge']) &
                
                # MACD confirmation
                (dataframe['macdhist'] > 0) &
                (dataframe['macd'] > dataframe['macdsignal']) &
                
                # Heikin Ashi confirmation
                (dataframe['ha_close'] > dataframe['ha_open']) &
                
                # Stochastic not overbought
                (dataframe['stoch_k'] < 80) &
                
                # Not choppy market
                (dataframe['bb_width'] > 2) &  # Sufficient volatility
                
                # Volume safety
                (dataframe['volume'] > 0)
            ),
            ['enter_long', 'enter_tag']
        ] = (1, 'hma_supertrend_long')

        # ===== SHORT ENTRY CONDITIONS =====
        """
        SHORT ENTRY CONDITIONS - Mirror of long conditions
        
        Requirements for SHORT:
        1. HMA is falling (primary trend)
        2. Supertrend is bearish (direction = -1)
        3. Price is below EMA fast (short-term trend alignment)
        4. RSI < inverse threshold (not overbought, has momentum down)
        5. ADX > threshold (strong trend, not ranging)
        6. Volume surge (institutional interest)
        7. MACD histogram negative (momentum confirmation)
        8. Price below EMA slow (long-term trend alignment)
        9. Heikin Ashi candle is bearish
        10. Stochastic not oversold (room to fall)
        """
        
        dataframe.loc[
            (
                # Primary conditions
                (dataframe['is_bearish']) &
                (dataframe['hma_falling']) &
                (dataframe['supertrend_direction'] == -1) &
                
                # Trend alignment
                (dataframe['close'] < dataframe['ema_fast']) &
                (dataframe['close'] < dataframe['ema_slow']) &
                (dataframe['ema_fast'] < dataframe['ema_slow']) &
                
                # Momentum confirmation
                (dataframe['rsi'] < (100 - self.rsi_buy_threshold.value)) &
                (dataframe['rsi'] > 30) &  # Not oversold yet
                (dataframe['adx'] > self.adx_threshold.value) &
                
                # Volume confirmation
                (dataframe['volume_surge']) &
                
                # MACD confirmation
                (dataframe['macdhist'] < 0) &
                (dataframe['macd'] < dataframe['macdsignal']) &
                
                # Heikin Ashi confirmation
                (dataframe['ha_close'] < dataframe['ha_open']) &
                
                # Stochastic not oversold
                (dataframe['stoch_k'] > 20) &
                
                # Not choppy market
                (dataframe['bb_width'] > 2) &  # Sufficient volatility
                
                # Volume safety
                (dataframe['volume'] > 0)
            ),
            ['enter_short', 'enter_tag']
        ] = (1, 'hma_supertrend_short')

        return dataframe

    # ============================================
    # EXIT CONDITIONS
    # ============================================
    
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        EXIT CONDITIONS - Protect profits and cut losses
        
        Exit LONG when:
        1. Supertrend flips bearish (primary signal)
        2. OR RSI extremely overbought (take profits)
        3. OR choppy market detected (if enabled)
        4. OR MACD bearish crossover
        5. OR price closes below EMA fast
        
        Exit SHORT when:
        1. Supertrend flips bullish (primary signal)
        2. OR RSI extremely oversold (take profits)
        3. OR choppy market detected (if enabled)
        4. OR MACD bullish crossover
        5. OR price closes above EMA fast
        """
        
        # ===== EXIT LONG =====
        dataframe.loc[
            (
                # Primary exit: Supertrend flip
                (dataframe['supertrend_direction'] == -1) |
                
                # Take profit: Extreme overbought
                (dataframe['rsi'] > self.rsi_sell_threshold.value) |
                
                # Exit on choppy (if enabled)
                (self.exit_on_choppy.value & dataframe['is_choppy']) |
                
                # MACD bearish crossover
                (
                    (dataframe['macd'] < dataframe['macdsignal']) &
                    (dataframe['macd'].shift(1) > dataframe['macdsignal'].shift(1))
                ) |
                
                # Price broke below fast EMA
                (dataframe['close'] < dataframe['ema_fast']) |
                
                # Heikin Ashi turned bearish
                (dataframe['ha_close'] < dataframe['ha_open'])
            ),
            ['exit_long', 'exit_tag']
        ] = (1, 'exit_signal_long')

        # ===== EXIT SHORT =====
        dataframe.loc[
            (
                # Primary exit: Supertrend flip
                (dataframe['supertrend_direction'] == 1) |
                
                # Take profit: Extreme oversold
                (dataframe['rsi'] < (100 - self.rsi_sell_threshold.value)) |
                
                # Exit on choppy (if enabled)
                (self.exit_on_choppy.value & dataframe['is_choppy']) |
                
                # MACD bullish crossover
                (
                    (dataframe['macd'] > dataframe['macdsignal']) &
                    (dataframe['macd'].shift(1) < dataframe['macdsignal'].shift(1))
                ) |
                
                # Price broke above fast EMA
                (dataframe['close'] > dataframe['ema_fast']) |
                
                # Heikin Ashi turned bullish
                (dataframe['ha_close'] > dataframe['ha_open'])
            ),
            ['exit_short', 'exit_tag']
        ] = (1, 'exit_signal_short')

        return dataframe

    # ============================================
    # CUSTOM METHODS
    # ============================================
    
    def confirm_trade_entry(self, pair: str, order_type: str, amount: float, rate: float,
                           time_in_force: str, current_time: datetime, entry_tag: Optional[str],
                           side: str, **kwargs) -> bool:
        """
        Called right before placing a trade entry order.
        Use this to add additional entry validation.
        
        Example: Block trades during high impact news events
        """
        # Add custom validation here if needed
        # For now, allow all trades that pass indicator checks
        return True
    
    def confirm_trade_exit(self, pair: str, trade, order_type: str, amount: float,
                          rate: float, time_in_force: str, exit_reason: str,
                          current_time: datetime, **kwargs) -> bool:
        """
        Called right before placing a trade exit order.
        Use this to prevent exits under certain conditions.
        """
        # Add custom validation here if needed
        # For now, allow all exits
        return True
    
    def custom_stake_amount(self, pair: str, current_time: datetime, current_rate: float,
                           proposed_stake: float, min_stake: Optional[float], max_stake: float,
                           leverage: float, entry_tag: Optional[str], side: str,
                           **kwargs) -> float:
        """
        Customize stake amount per trade.
        You can implement dynamic position sizing based on:
        - ATR (volatility)
        - Account balance
        - Win streak
        - etc.
        """
        # For now, use default stake amount
        return proposed_stake

    # ============================================
    # WEBHOOK CALLBACKS
    # ============================================
    
    def custom_entry_price(self, pair: str, current_time: datetime, proposed_rate: float,
                          entry_tag: Optional[str], side: str, **kwargs) -> float:
        """
        Custom entry price logic
        """
        return proposed_rate
    
    def custom_exit_price(self, pair: str, trade, current_time: datetime,
                         proposed_rate: float, current_profit: float,
                         exit_tag: Optional[str], **kwargs) -> float:
        """
        Custom exit price logic
        """
        return proposed_rate
