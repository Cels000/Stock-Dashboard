import streamlit as st
import os
from datetime import datetime
from typing import Dict
from config import (
    API_CONFIGS,
    ANALYSIS_PROMPT,
    PAGE_CONFIG,
    DEFAULT_STOCK,
    ERROR_MESSAGES
)
from utils import load_css, display_metric, format_large_number
from stock_data import get_stock_data
from ai_analysis import get_available_models, get_ai_analysis
from charts import create_stock_chart, plot_moving_averages, plot_rsi, plot_macd
from settings import init_settings, render_settings, get_api_configs

def render_metrics(data: Dict):
    st.header(f"{data['company_name']} ({data.get('symbol', '')})")

    col1, col2, col3 = st.columns(3)
    with col1:
        display_metric("Current Price", data['current_price'], "$")
        display_metric("Target Price", data['target_price'], "$")
    with col2:
        display_metric("P/E Ratio", data['pe_ratio'])
        display_metric("Market Cap", format_large_number(data['market_cap']), "$")
    with col3:
        display_metric("Volume", format_large_number(data['volume']))
        display_metric("Beta", data['beta'])


def render_additional_metrics(data: Dict):
    with st.expander("Additional Metrics"):
        col1, col2, col3 = st.columns(3)
        with col1:
            display_metric("52 Week High", data['fifty_two_week_high'], "$")
            display_metric("Revenue Growth", data['revenue_growth'])
        with col2:
            display_metric("52 Week Low", data['fifty_two_week_low'], "$")
            display_metric("Profit Margins", data['profit_margins'])
        with col3:
            display_metric("Analyst Count", data['analyst_count'])
            display_metric("Avg Volume", format_large_number(data['avg_volume']))


def main():
    """Main application function for the Stock Analysis Dashboard"""
    try:
        # Initialize application
        init_settings()
        st.set_page_config(**PAGE_CONFIG)
        load_css()

        # Create main tabs
        dashboard_tab, settings_tab = st.tabs(["Dashboard", "Settings"])

        with dashboard_tab:
            render_dashboard()

        with settings_tab:
            render_settings()

    except Exception as e:
        st.error(f"Application Error: {str(e)}")
        st.error("Please refresh the page and try again.")


def render_dashboard():
    """Render the main dashboard content"""
    st.title("Stock Analysis Dashboard")

    # Sidebar Controls
    render_sidebar_controls()

    # Main Content
    try:
        stock_symbol = st.session_state.get('stock_symbol', DEFAULT_STOCK)
        provider = st.session_state.get('selected_provider')
        model = st.session_state.get('selected_model')

        # Fetch and display stock data
        if stock_symbol:
            display_stock_analysis(stock_symbol, provider, model)

    except Exception as e:
        st.error(f"Dashboard Error: {str(e)}")


def render_sidebar_controls():
    """Render sidebar controls for stock and AI model selection"""
    st.sidebar.title("Controls")

    # Stock Symbol Input
    stock_symbol = st.sidebar.text_input(
        "Enter Stock Symbol",
        value=st.session_state.get('stock_symbol', DEFAULT_STOCK)
    ).upper()
    st.session_state.stock_symbol = stock_symbol

    # Get configured providers
    api_configs = get_api_configs()

    # List all providers regardless of configuration
    all_providers = [
        "Claude (Anthropic)",
        "OpenAI (ChatGPT)",
        "Google AI",
        "OpenRouter",
        "Hugging Face",
        "Ollama"
    ]

    # Provider Selection
    provider = st.sidebar.selectbox(
        "Choose AI Provider",
        all_providers,
        key='selected_provider'
    )

    # Check if provider is configured
    if provider not in api_configs:
        st.sidebar.warning(f"{provider} is not configured. Please add API key in Settings.")
        return None, None

    # Model Selection
    available_models = get_available_models(provider)
    if not available_models:
        st.sidebar.error(f"No models available for {provider}")
        model = None
    else:
        model = st.sidebar.selectbox(
            "Choose Model",
            available_models,
            key='selected_model'
        )

    return provider, model


def get_available_providers(api_configs: dict) -> list:
    """Get list of available AI providers with valid configurations"""
    available_providers = []
    for provider in api_configs.keys():
        try:
            models = get_available_models(provider)
            if models:
                available_providers.append(provider)
        except Exception as e:
            st.sidebar.warning(f"Error loading {provider}: {str(e)}")
    return available_providers


def display_stock_analysis(stock_symbol: str, provider: str, model: str):
    """Display stock analysis data and charts"""
    try:
        # Fetch stock data
        with st.spinner("Fetching stock data..."):
            data = get_stock_data(stock_symbol)
            data['symbol'] = stock_symbol

        # Display timestamp
        col1, col2 = st.columns([2, 1])
        with col2:
            st.write(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Display metrics
        render_metrics(data)
        render_additional_metrics(data)

        # Technical Analysis Section
        st.subheader("Technical Analysis")
        display_technical_analysis(stock_symbol)

        # AI Analysis Section
        if model:
            display_ai_analysis(data, stock_symbol, provider, model)

    except Exception as e:
        st.error(f"Error analyzing {stock_symbol}: {str(e)}")
        st.error(ERROR_MESSAGES['invalid_symbol'])


def display_technical_analysis(stock_symbol: str):
    """Display technical analysis charts"""
    try:
        tab1, tab2, tab3, tab4 = st.tabs(["Price", "Moving Averages", "RSI", "MACD"])

        historical_data = get_stock_data(stock_symbol, include_history=True)

        charts = {
            tab1: ("Price Chart", create_stock_chart),
            tab2: ("Moving Averages", plot_moving_averages),
            tab3: ("RSI", plot_rsi),
            tab4: ("MACD", plot_macd)
        }

        for tab, (title, chart_func) in charts.items():
            with tab:
                with st.spinner(f"Loading {title}..."):
                    fig = chart_func(historical_data)
                    st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading charts: {str(e)}")


def display_ai_analysis(data: dict, symbol: str, provider: str, model: str):
    """Display AI analysis section"""
    st.subheader("AI Analysis")
    try:
        with st.spinner(f"Generating analysis using {provider} - {model}..."):
            analysis = get_ai_analysis(data, symbol, provider, model)
            st.markdown(analysis)
    except Exception as e:
        st.error(f"Error generating AI analysis: {str(e)}")


if __name__ == "__main__":
    main()
