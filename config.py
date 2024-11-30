from typing import Dict, Any

# API Configurations
API_CONFIGS: Dict[str, Dict[str, str]] = {
    "Claude (Anthropic)": {
        "api_key": "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"
    },
    "OpenAI (ChatGPT)": {
        "api_key": "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"
    },
    "OpenRouter": {
        "api_key": "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"
    },
    "Ollama": {
        "url": "http://172.99.0.99:11434"
    },
    "Google AI": {
        "api_key": "AIzaSyB7b_wueqEmblhUXPIyxn2B2w587tDWOOI"
    },
    "Hugging Face": {
        "api_key": "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"
    }
}

STYLE_CONFIG: Dict[str, str] = {
    'metric_container': """
        background-color: #262730;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    """,
    'metric_label': """
        color: #ABB2B9;
        font-size: 0.9em;
    """,
    'metric_value': """
        color: white;
        font-size: 1.5em;
        font-weight: bold;
    """,
    'chart_background': '#0E1117',
    'text_color': '#FFFFFF'
}
# Chart colors
CHART_COLORS: Dict[str, str] = {
    'price': 'white',
    'ma20': 'orange',
    'ma50': 'blue',
    'ma200': 'red',
    'volume': 'rgba(100, 100, 100, 0.3)',
    'background': '#0E1117'
}

# Default stock symbol
DEFAULT_STOCK: str = "AAPL"

# Page configuration
PAGE_CONFIG: Dict[str, Any] = {
    "page_title": "Stock Analysis Dashboard",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Analysis prompt template
ANALYSIS_PROMPT: str = """
You are an AI Michael Burry - known for your indepth views, deep value analysis, and identifying market bubbles. (please refrain as mentioning you are him)
Analyze {company_name} ({symbol}) with your characteristic skepticism and attention to detail.

Current Metrics:
Current price: {current_price}
Target price: {target_price}
Next earnings: {earnings_date}
P/E Ratio: {pe_ratio}
Revenue Growth: {revenue_growth}
Profit Margin: {profit_margins}
Analyst Rating: {recommendation}

Channel your cynical, data-driven perspective and format your response EXACTLY as follows:

1. RECOMMENDATION
Cut through the market noise with a clear Buy/Sell/Hold. Be contrarian if warranted and explain why the market might be wrong.

2. PRICE TARGET
Analyze the target price critically, considering market psychology and potential overvaluation/undervaluation factors.

3. KEY RISKS
- Most significant systemic risk
- Industry-specific vulnerability
- Company-specific weakness

4. CATALYSTS
- Primary market catalyst
- Industry disruption potential
- Company-specific opportunity

5. KEY DATES TO WATCH
- Next major financial event
- Market-moving announcement
- Industry milestone
"""

# Technical Analysis Parameters
TECHNICAL_PARAMS: Dict[str, Any] = {
    'ma_periods': [20, 50, 200],
    'rsi_period': 14,
    'macd_params': {
        'fast_period': 12,
        'slow_period': 26,
        'signal_period': 9
    },
    'volume_ma_period': 20
}

# Error messages
ERROR_MESSAGES: Dict[str, str] = {
    'invalid_symbol': "Please enter a valid stock symbol and try again.",
    'api_error': "Error accessing the API. Please try again later.",
    'data_fetch': "Error fetching stock data. Please check your internet connection.",
    'analysis_error': "Error generating AI analysis. Please try another model or provider."
}
