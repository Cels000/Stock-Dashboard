import streamlit as st
import pandas as pd
from typing import Union, Dict, Any
from datetime import datetime
from config import STYLE_CONFIG, ERROR_MESSAGES

def load_css() -> None:
    """Load custom CSS styles for the dashboard"""
    st.markdown(f"""
        <style>
        .metric-container {{
            {STYLE_CONFIG['metric_container']}
        }}
        .metric-label {{
            {STYLE_CONFIG['metric_label']}
        }}
        .metric-value {{
            {STYLE_CONFIG['metric_value']}
        }}
        .stTabs [data-baseweb="tab-list"] {{
            gap: 24px;
        }}
        .stTabs [data-baseweb="tab"] {{
            height: 50px;
            padding: 0 16px;
            background-color: #262730;
            border-radius: 4px;
        }}
        </style>
    """, unsafe_allow_html=True)

def format_large_number(num: Union[int, float]) -> str:
    """Format large numbers into K, M, B, T format"""
    if not isinstance(num, (int, float)) or pd.isna(num):
        return 'N/A'

    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return f"{num:.2f}{['', 'K', 'M', 'B', 'T'][magnitude]}"

def format_percentage(value: Union[int, float]) -> str:
    """Format number as percentage"""
    if not isinstance(value, (int, float)) or pd.isna(value):
        return 'N/A'
    return f"{value * 100:.2f}%"

def display_metric(label: str, value: Any, prefix: str = "") -> None:
    """Display a metric in the dashboard"""
    try:
        if isinstance(value, (int, float)):
            formatted_value = f"{prefix}{value:,.2f}"
        else:
            formatted_value = f"{prefix}{value}"

        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{formatted_value}</div>
            </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error displaying metric {label}: {str(e)}")

def safe_get(data: Dict[str, Any], key: str, default: Any = 'N/A') -> Any:
    """Safely get a value from a dictionary"""
    try:
        value = data.get(key, default)
        return value if value is not None else default
    except:
        return default

def format_timestamp(timestamp: Union[int, float, str]) -> str:
    """Format timestamp to readable date string"""
    try:
        if isinstance(timestamp, (int, float)):
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        elif isinstance(timestamp, str):
            return datetime.strptime(timestamp, '%Y-%m-%d').strftime('%Y-%m-%d')
        return 'N/A'
    except:
        return 'N/A'

def display_error(error_key: str, exception: Exception = None) -> None:
    """Display error message from config"""
    error_msg = ERROR_MESSAGES.get(error_key, str(exception) if exception else "Unknown error occurred")
    st.error(error_msg)

def format_currency(value: Union[int, float], currency: str = "$") -> str:
    """Format value as currency"""
    if not isinstance(value, (int, float)) or pd.isna(value):
        return 'N/A'
    return f"{currency}{value:,.2f}"

@st.cache_data(ttl=3600)
def cache_data(func):
    """Decorator for caching data with TTL"""
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# Function to check if market is open
def is_market_open() -> bool:
    """Check if US market is currently open"""
    now = datetime.now()
    # Check if it's a weekday
    if now.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
        return False
    # Check if it's between 9:30 AM and 4:00 PM EST
    market_start = now.replace(hour=9, minute=30, second=0)
    market_end = now.replace(hour=16, minute=0, second=0)
    return market_start <= now <= market_end