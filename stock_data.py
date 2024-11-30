import yfinance as yf
import pandas as pd
from typing import Dict, Any, Union
from datetime import datetime
import streamlit as st
from config import TECHNICAL_PARAMS


def process_stock_info(info: Dict, symbol: str) -> Dict[str, Any]:
    try:
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))
        earnings_date = get_earnings_date(info)

        return {
            'company_name': info.get('longName', symbol),
            'current_price': current_price,
            'target_price': info.get('targetMeanPrice', 'N/A'),
            'recommendation': info.get('recommendationKey', 'N/A').upper(),
            'earnings_date': earnings_date,
            'pe_ratio': info.get('forwardPE', 'N/A'),
            'market_cap': info.get('marketCap', 'N/A'),
            'volume': info.get('volume', 'N/A'),
            'avg_volume': info.get('averageVolume', 'N/A'),
            'fifty_two_week_high': info.get('fiftyTwoWeekHigh', 'N/A'),
            'fifty_two_week_low': info.get('fiftyTwoWeekLow', 'N/A'),
            'revenue_growth': info.get('revenueGrowth', 'N/A'),
            'profit_margins': info.get('profitMargins', 'N/A'),
            'beta': info.get('beta', 'N/A'),
            'analyst_count': info.get('numberOfAnalystOpinions', 'N/A')
        }
    except Exception as e:
        raise ValueError(f"Error processing stock info: {str(e)}")


def get_earnings_date(info: Dict) -> str:
    try:
        if 'earningsDate' in info:
            timestamp = info['earningsDate']
            if isinstance(timestamp, list) and timestamp:
                return datetime.fromtimestamp(timestamp[0]).strftime('%Y-%m-%d')
            elif isinstance(timestamp, (int, float)):
                return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        elif 'earningsTimestamp' in info:
            return datetime.fromtimestamp(info['earningsTimestamp']).strftime('%Y-%m-%d')
    except:
        pass
    return 'Not Available'


@st.cache_data(ttl=300)
def get_stock_data(symbol: str, include_history: bool = False) -> Union[Dict[str, Any], pd.DataFrame]:
    try:
        stock = yf.Ticker(symbol)

        if include_history:
            df = stock.history(period="1y")
            if df.empty:
                raise ValueError(f"No historical data available for {symbol}")

            # Calculate technical indicators
            for period in TECHNICAL_PARAMS['ma_periods']:
                df[f'MA{period}'] = df['Close'].rolling(window=period).mean()

            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=TECHNICAL_PARAMS['rsi_period']).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=TECHNICAL_PARAMS['rsi_period']).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))

            macd_params = TECHNICAL_PARAMS['macd_params']
            exp1 = df['Close'].ewm(span=macd_params['fast_period'], adjust=False).mean()
            exp2 = df['Close'].ewm(span=macd_params['slow_period'], adjust=False).mean()
            df['MACD'] = exp1 - exp2
            df['Signal_Line'] = df['MACD'].ewm(span=macd_params['signal_period'], adjust=False).mean()
            df['MACD_Histogram'] = df['MACD'] - df['Signal_Line']

            df.index = pd.to_datetime(df.index)
            return df

        return process_stock_info(stock.info, symbol)

    except Exception as e:
        raise ValueError(f"Error fetching stock data: {str(e)}")