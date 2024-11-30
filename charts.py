import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Optional
from config import CHART_COLORS, TECHNICAL_PARAMS


def create_stock_chart(df: pd.DataFrame, show_volume: bool = True) -> go.Figure:
    """Create main stock price candlestick chart with optional volume"""
    fig = make_subplots(
        rows=2 if show_volume else 1,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.7, 0.3] if show_volume else [1]
    )

    # Add candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='OHLC'
        ),
        row=1, col=1
    )

    # Add moving averages
    for period in TECHNICAL_PARAMS['ma_periods']:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df[f'MA{period}'],
                name=f'{period} MA',
                line=dict(color=CHART_COLORS[f'ma{period}']),
                opacity=0.7
            ),
            row=1, col=1
        )

    # Add volume bars if requested
    if show_volume:
        colors = [CHART_COLORS['price'] if row['Close'] >= row['Open'] else 'red' for _, row in df.iterrows()]
        fig.add_trace(
            go.Bar(
                x=df.index,
                y=df['Volume'],
                name='Volume',
                marker_color=colors,
                opacity=0.5
            ),
            row=2, col=1
        )

    fig.update_layout(
        title='Stock Price History',
        yaxis_title='Stock Price (USD)',
        yaxis2_title='Volume' if show_volume else None,
        template='plotly_dark',
        xaxis_rangeslider_visible=False,
        height=800 if show_volume else 600
    )

    return fig


def plot_moving_averages(df: pd.DataFrame, periods: Optional[list] = None) -> go.Figure:
    """Create moving averages comparison chart"""
    fig = go.Figure()

    # Base price
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Close'],
        name='Price',
        line=dict(color=CHART_COLORS['price'])
    ))

    # Add moving averages
    periods = periods or TECHNICAL_PARAMS['ma_periods']
    for period in periods:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df[f'MA{period}'],
            name=f'{period} MA',
            line=dict(color=CHART_COLORS[f'ma{period}']),
            opacity=0.7
        ))

    fig.update_layout(
        title='Moving Averages',
        yaxis_title='Price',
        template='plotly_dark',
        height=500,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    return fig


def plot_rsi(df: pd.DataFrame, period: int = None) -> go.Figure:
    """Create RSI chart with overbought/oversold zones"""
    fig = go.Figure()

    period = period or TECHNICAL_PARAMS['rsi_period']

    # Add RSI line
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['RSI'],
        name='RSI',
        line=dict(color=CHART_COLORS['price'])
    ))

    # Add overbought/oversold zones
    fig.add_hrect(
        y0=70, y1=100,
        fillcolor="red", opacity=0.1,
        layer="below", line_width=0,
        name="Overbought"
    )
    fig.add_hrect(
        y0=0, y1=30,
        fillcolor="green", opacity=0.1,
        layer="below", line_width=0,
        name="Oversold"
    )

    # Add reference lines
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought (70)")
    fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold (30)")
    fig.add_hline(y=50, line_dash="dash", line_color="yellow", annotation_text="Neutral (50)")

    fig.update_layout(
        title=f'Relative Strength Index (RSI-{period})',
        yaxis_title='RSI',
        yaxis=dict(range=[0, 100]),
        template='plotly_dark',
        height=400
    )

    return fig


def plot_macd(df: pd.DataFrame) -> go.Figure:
    """Create MACD chart with histogram"""
    params = TECHNICAL_PARAMS['macd_params']

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=(
            'Price',
            f'MACD ({params["fast_period"]},{params["slow_period"]},{params["signal_period"]})'
        )
    )

    # Add price
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['Close'],
            name='Price',
            line=dict(color=CHART_COLORS['price'])
        ),
        row=1, col=1
    )

    # Add MACD line
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['MACD'],
            name='MACD',
            line=dict(color=CHART_COLORS['ma50'])
        ),
        row=2, col=1
    )

    # Add Signal line
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['Signal_Line'],
            name='Signal',
            line=dict(color=CHART_COLORS['ma20'])
        ),
        row=2, col=1
    )

    # Add MACD histogram
    colors = ['green' if val >= 0 else 'red' for val in df['MACD_Histogram']]
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df['MACD_Histogram'],
            name='Histogram',
            marker_color=colors,
            opacity=0.5
        ),
        row=2, col=1
    )

    fig.update_layout(
        template='plotly_dark',
        height=800,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig