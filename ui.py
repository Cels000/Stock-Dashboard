import streamlit as st
from datetime import datetime
from typing import Dict, Any, Tuple
from utils import display_metric, format_large_number
import plotly.graph_objects as go
from config import ERROR_MESSAGES


def render_header() -> Tuple[st.columns, st.columns]:
    """Render the dashboard header with title and timestamp"""
    title_col, time_col = st.columns([2, 1])
    with title_col:
        st.title("Stock Analysis Dashboard")
    with time_col:
        st.write("")
        st.write("")
        st.write(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return title_col, time_col


def render_sidebar(api_configs: Dict) -> Tuple[str, str, str]:
    """Render sidebar controls and return selected options"""
    st.sidebar.title("Controls")

    # Stock input
    stock_symbol = st.sidebar.text_input("Enter Stock Symbol", value="AAPL").upper()

    # Provider selection
    provider = st.sidebar.selectbox(
        "Choose AI Provider",
        list(api_configs.keys())
    )

    # Model loading indicator
    st.sidebar.text("Loading available models...")

    return stock_symbol, provider


def render_metrics(data: Dict[str, Any]) -> None:
    """Render key metrics in a three-column layout"""
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


def render_technical_charts(historical_data: Dict[str, Any]) -> None:
    """Render technical analysis charts in tabs"""
    st.subheader("Technical Analysis")
    tab1, tab2, tab3, tab4 = st.tabs(["Price", "Moving Averages", "RSI", "MACD"])

    with tab1:
        fig = create_stock_chart(historical_data)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        fig = plot_moving_averages(historical_data)
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        fig = plot_rsi(historical_data)
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        fig = plot_macd(historical_data)
        st.plotly_chart(fig, use_container_width=True)


def render_ai_analysis(analysis: str, provider: str, model: str) -> None:
    """Render AI analysis with loading indicator"""
    st.subheader("AI Analysis")
    with st.spinner(f"Generating analysis using {provider} - {model}..."):
        st.markdown(analysis)


def show_error(error_key: str, exception: Exception = None) -> None:
    """Display error message with proper formatting"""
    error_msg = ERROR_MESSAGES.get(error_key, str(exception) if exception else "Unknown error occurred")
    st.error(error_msg)


def render_additional_info(data: Dict[str, Any]) -> None:
    """Render additional stock information"""
    with st.expander("Additional Information"):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Price Statistics**")
            display_metric("52 Week High", data['fifty_two_week_high'], "$")
            display_metric("52 Week Low", data['fifty_two_week_low'], "$")
            display_metric("Average Volume", format_large_number(data['avg_volume']))
        with col2:
            st.write("**Company Statistics**")
            display_metric("Revenue Growth", data['revenue_growth'])
            display_metric("Profit Margins", data['profit_margins'])
            display_metric("Analyst Count", data['analyst_count'])


def render_model_selector(available_models: list) -> str:
    """Render model selection dropdown"""
    if not available_models:
        st.sidebar.error("No models available")
        return None
    return st.sidebar.selectbox("Choose Model", available_models)


def render_refresh_button() -> bool:
    """Render refresh button and return its state"""
    return st.sidebar.button("🔄 Refresh Data")