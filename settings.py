# settings.py
import streamlit as st
from key_management import ApiKeyManager


def init_settings():
    """Initialize settings and load saved API keys"""
    if 'key_manager' not in st.session_state:
        st.session_state.key_manager = ApiKeyManager()

    if 'api_keys' not in st.session_state:
        # Load saved keys
        saved_keys = st.session_state.key_manager.load_keys()
        st.session_state.api_keys = {
            "Claude (Anthropic)": saved_keys.get("Claude (Anthropic)", ""),
            "OpenAI (ChatGPT)": saved_keys.get("OpenAI (ChatGPT)", ""),
            "OpenRouter": saved_keys.get("OpenRouter", ""),
            "Google AI": saved_keys.get("Google AI", ""),
            "Hugging Face": saved_keys.get("Hugging Face", ""),
            "Ollama": saved_keys.get("Ollama", "http://localhost:11434")
        }


def render_settings():
    """Render settings page with API key inputs"""
    st.header("API Settings")

    # Create two columns for better layout
    col1, col2 = st.columns(2)

    changed = False
    with col1:
        st.subheader("Primary Services")
        for provider in ["Claude (Anthropic)", "OpenAI (ChatGPT)", "Google AI"]:
            new_value = st.text_input(
                f"{provider} API Key",
                value=st.session_state.api_keys.get(provider, ""),
                type="password",
                key=f"setting_{provider}",
                help=f"Enter your {provider} API key"
            )
            if new_value != st.session_state.api_keys.get(provider):
                st.session_state.api_keys[provider] = new_value
                changed = True

    with col2:
        st.subheader("Additional Services")
        for provider in ["OpenRouter", "Hugging Face"]:
            new_value = st.text_input(
                f"{provider} API Key",
                value=st.session_state.api_keys.get(provider, ""),
                type="password",
                key=f"setting_{provider}",
                help=f"Enter your {provider} API key"
            )
            if new_value != st.session_state.api_keys.get(provider):
                st.session_state.api_keys[provider] = new_value
                changed = True

        new_ollama = st.text_input(
            "Ollama URL",
            value=st.session_state.api_keys.get("Ollama", "http://localhost:11434"),
            key="setting_Ollama",
            help="URL where Ollama is running"
        )
        if new_ollama != st.session_state.api_keys.get("Ollama"):
            st.session_state.api_keys["Ollama"] = new_ollama
            changed = True

    # Save button (optional, as changes are saved automatically)
    if st.button("Save Settings") or changed:
        st.session_state.key_manager.save_keys(st.session_state.api_keys)
        st.success("Settings saved successfully!")

        # Debug info - remove in production
        st.info(f"Keys saved to: {st.session_state.key_manager.key_file}")


def get_api_configs() -> dict:
    """Get the current API configurations"""
    return st.session_state.api_keys
