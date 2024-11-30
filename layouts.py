import streamlit as st
from typing import Dict, Any, Callable
from config import STYLE_CONFIG


class DashboardLayout:
    """Class to handle different dashboard layouts"""

    @staticmethod
    def full_width(content_func: Callable) -> None:
        """Render content in full width layout"""
        st.set_page_config(layout="wide")
        content_func()

    @staticmethod
    def sidebar_layout(sidebar_content: Callable, main_content: Callable) -> None:
        """Render content with sidebar layout"""
        with st.sidebar:
            sidebar_content()
        main_content()

    @staticmethod
    def two_column_layout(left_content: Callable, right_content: Callable,
                          left_width: int = 2, right_width: int = 1) -> None:
        """Render content in two columns"""
        col1, col2 = st.columns([left_width, right_width])
        with col1:
            left_content()
        with col2:
            right_content()

    @staticmethod
    def card(title: str, content: Callable) -> None:
        """Render content in a card-like container"""
        st.markdown(f"""
            <div style='{STYLE_CONFIG["metric_container"]}'>
                <h3>{title}</h3>
                <div style='padding: 10px;'>
                    {content()}
                </div>
            </div>
        """, unsafe_allow_html=True)


class MetricsGrid:
    """Class to handle metric grid layouts"""

    @staticmethod
    def three_column(metrics: Dict[str, Any]) -> None:
        """Render metrics in a three-column grid"""
        cols = st.columns(3)
        for i, (label, value) in enumerate(metrics.items()):
            with cols[i % 3]:
                st.metric(label=label, value=value)

    @staticmethod
    def two_column(metrics: Dict[str, Any]) -> None:
        """Render metrics in a two-column grid"""
        cols = st.columns(2)
        for i, (label, value) in enumerate(metrics.items()):
            with cols[i % 2]:
                st.metric(label=label, value=value)