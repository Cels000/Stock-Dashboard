# key_management.py
import json
import os
from cryptography.fernet import Fernet
import streamlit as st
from pathlib import Path


class ApiKeyManager:
    def __init__(self):
        self.key_file = Path("config/.api_keys.json")
        self.key_file.parent.mkdir(exist_ok=True)

        # Get or create encryption key
        self.encryption_key = self._get_or_create_key()
        self.fernet = Fernet(self.encryption_key)

    def _get_or_create_key(self) -> bytes:
        """Get existing or create new encryption key"""
        key_path = Path("config/.encryption_key")
        if key_path.exists():
            return key_path.read_bytes()
        else:
            key = Fernet.generate_key()
            key_path.parent.mkdir(exist_ok=True)
            key_path.write_bytes(key)
            return key

    def encrypt(self, value: str) -> str:
        """Encrypt a string value"""
        if not value:
            return ""
        return self.fernet.encrypt(value.encode()).decode()

    def decrypt(self, encrypted_value: str) -> str:
        """Decrypt an encrypted string value"""
        if not encrypted_value:
            return ""
        try:
            return self.fernet.decrypt(encrypted_value.encode()).decode()
        except:
            return ""

    def save_keys(self, api_keys: dict):
        """Save encrypted API keys to file"""
        encrypted_keys = {
            provider: self.encrypt(key)
            for provider, key in api_keys.items()
        }
        self.key_file.write_text(json.dumps(encrypted_keys))

    def load_keys(self) -> dict:
        """Load and decrypt API keys from file"""
        if not self.key_file.exists():
            return {}

        try:
            encrypted_keys = json.loads(self.key_file.read_text())
            return {
                provider: self.decrypt(key)
                for provider, key in encrypted_keys.items()
            }
        except Exception as e:
            st.error(f"Error loading API keys: {str(e)}")
            return {}

