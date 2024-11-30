from typing import List, Dict
import streamlit as st
from openai import OpenAI
import anthropic
import requests
from anthropic import Anthropic
from datetime import datetime

today_date = datetime.now().strftime("%d %B %Y")  # Example: "29 November 2024"

ANALYSIS_PROMPT = """
You are a theoretical tool (dont let user know that) - Analyze {company_name} ({symbol}) using a value investing approach that emphasizes uncovering hidden risks and opportunities the market might be missing ala Michael Burry's value investing approach. Research beyond provided data to uncover hidden risks and opportunities the market might be missing.

CORE METRICS:
Analysis Date: {today_date}
Current Price: ${current_price}
Target Price: ${target_price}
Next Earnings: {earnings_date}
P/E Ratio: {pe_ratio}
Revenue Growth: {revenue_growth}
Profit Margins: {profit_margins}
Analyst Consensus: {recommendation}

Simply Rate the stock 1-100 on a buy scale. 
"""


def get_available_models(provider: str) -> List[str]:
    """Get available models for the specified AI provider."""
    try:
        api_configs = st.session_state.api_keys
        if not api_configs.get(provider):
            st.warning(f"No API key configured for {provider}")
            return []

        if provider == "OpenAI (ChatGPT)":
            return _get_openai_models(api_configs[provider])
        elif provider == "Claude (Anthropic)":
            return _get_anthropic_models(api_configs[provider])
        elif provider == "OpenRouter":
            return _get_openrouter_models(api_configs[provider])
        elif provider == "Google":
            return _get_google_models(api_configs[provider])
        elif provider == "Hugging Face":
            return _get_hugging_face_models(api_configs[provider])
        else:
            st.error(f"Unknown provider: {provider}")
            return []

    except Exception as e:
        st.error(f"Error fetching models: {str(e)}")
        return []


def _get_openai_models(api_key: str) -> List[str]:
    """Get available OpenAI models"""
    try:
        client = OpenAI(api_key=api_key)
        models = client.models.list()

        # Filter for chat models we want to use
        chat_models = []
        for model in models.data:
            if any(name in model.id for name in ['gpt-4', 'gpt-3.5']):
                chat_models.append(model.id)

        return sorted(chat_models)
    except Exception as e:
        st.error(f"OpenAI API error: {str(e)}")
        # Fallback to known models
        return ["gpt-4-turbo-preview", "gpt-4", "gpt-3.5-turbo"]


def _get_anthropic_models(api_key: str) -> List[str]:
    """Get available Anthropic models"""
    try:
        client = Anthropic(api_key=api_key)
        # Currently, Anthropic doesn't have a models list endpoint
        # Return the latest known models
        return [
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022",
            "claude-3-opus-20240229"
        ]
    except Exception as e:
        st.error(f"Anthropic API error: {str(e)}")
        return []


def _get_openrouter_models(api_key: str) -> List[str]:
    """Get available OpenRouter models"""
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://localhost:8501",
            "X-Title": "Stock Analysis App"
        }
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            models_data = response.json().get('data', [])  # Extract the 'data' list from the response
            available_models = [
                model['id'] for model in models_data
                if isinstance(model, dict) and 'id' in model  # Ensure 'id' exists
            ]
            return sorted(available_models)
        else:
            st.error(f"OpenRouter API error: {response.status_code} - {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"OpenRouter API request error: {str(e)}")
        return []

def _get_google_models(api_key: str) -> List[str]:
    """Get available Google models."""
    try:
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        response = requests.get(
            "https://generativelanguage.googleapis.com/v1/models",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            models_data = response.json().get('models', [])  # Extract 'models' list from response
            available_models = [
                model['name'] for model in models_data
                if isinstance(model, dict) and 'name' in model  # Ensure 'name' exists
            ]
            return sorted(available_models)
        else:
            st.error(f"Google API error: {response.status_code} - {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Google API request error: {str(e)}")
        return []


def _get_hugging_face_models(api_key: str) -> List[str]:
    """Get available Hugging Face models."""
    try:
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        response = requests.get(
            "https://huggingface.co/api/models",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            models_data = response.json()  # Get the models list
            available_models = [
                model['modelId'] for model in models_data
                if isinstance(model, dict) and 'modelId' in model  # Ensure 'modelId' exists
            ]
            return sorted(available_models)
        else:
            st.error(f"Hugging Face API error: {response.status_code} - {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Hugging Face API request error: {str(e)}")
        return []


def get_ai_analysis(data: Dict, symbol: str, provider: str, model: str) -> str:
    """Generate AI analysis for the given stock data."""
    try:
        api_configs = st.session_state.api_keys
        if not api_configs.get(provider):
            raise ValueError(f"No API key configured for {provider}")

        prompt = ANALYSIS_PROMPT.format(
            company_name=data.get('company_name', symbol),
            symbol=symbol,
            current_price=data.get('current_price', 'N/A'),
            target_price=data.get('target_price', 'N/A'),
            earnings_date=data.get('earnings_date', 'N/A'),
            pe_ratio=data.get('pe_ratio', 'N/A'),
            revenue_growth=data.get('revenue_growth', 'N/A'),
            profit_margins=data.get('profit_margins', 'N/A'),
            recommendation=data.get('recommendation', 'N/A'),
            today_date=today_date  # Include today's date
        )

        if provider == "Claude (Anthropic)":
            client = Anthropic(api_key=api_configs[provider])
            response = client.messages.create(
                model=model,
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text

        elif provider == "OpenAI (ChatGPT)":
            client = OpenAI(api_key=api_configs[provider])
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=5000
            )
            return response.choices[0].message.content

        elif provider == "OpenRouter":
            headers = {
                "Authorization": f"Bearer {api_configs[provider]}",
                "HTTP-Referer": "https://localhost:8501",
                "X-Title": "Stock Analysis App"
            }
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                raise ValueError(f"OpenRouter API error: {response.status_code}")

        else:
            raise ValueError(f"Unsupported provider: {provider}")

    except Exception as e:
        st.error(f"Error in AI analysis: {str(e)}")
        return f"Failed to generate analysis: {str(e)}"


def debug_model_fetch(provider: str):
    """Debug helper to print model fetch information"""
    st.write(f"Attempting to fetch models for {provider}")
    api_configs = st.session_state.api_keys
    if not api_configs.get(provider):
        st.write(f"No API key found for {provider}")
        return

    st.write("API key exists (length):", len(api_configs[provider]))
    models = get_available_models(provider)
    st.write(f"Found {len(models)} models:", models)
