"""
Provider Manager for LLM abstraction
Supports: Gemini 2.5 (ADC), Vendor1, Vendor2
"""
import os
import requests
from typing import Generator, Optional
from google.auth import default
from google.auth.transport.requests import Request


class BaseProvider:
    """Abstract base class for LLM providers"""
    
    def chat(self, messages: list, stream: bool = True) -> str | Generator[str, None, None]:
        raise NotImplementedError


class GeminiProvider(BaseProvider):
    """Google Gemini 2.5 via ADC or Direct API Key"""
    
    def __init__(self):
        self.model_name = os.environ.get("GEMINI_MODEL", "gemini-2.5-pro")
        
        # Try multiple auth methods in priority order
        self.auth_method = None
        self.api_key = None
        self.credentials = None
        self.project_id = None
        
        # Method 1: Direct API Key (from env variable or user-provided key)
        direct_api_key = os.environ.get("GEMINI_API_KEY")
        if direct_api_key:
            self.api_key = direct_api_key
            self.auth_method = "api_key"
            print(f"Gemini configured with API Key (method: {self.auth_method})")
            return
        
        # Method 2: Service Account Key File (for Vertex AI or API Key generation)
        sa_key_file = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if sa_key_file and os.path.exists(sa_key_file):
            from google.oauth2 import service_account
            try:
                # Use scopes for Vertex AI API
                self.credentials = service_account.Credentials.from_service_account_file(
                    sa_key_file, scopes=["https://www.googleapis.com/auth/cloud-platform"]
                )
                self.project_id = self.credentials.project_id
                self.auth_method = "service_account"
                print(f"Gemini configured with Service Account Key - Project: {self.project_id}")
                return
            except Exception as e:
                print(f"Service Account Key load failed: {e}")
        
        # Method 3: ADC (for production GCP environments)
        try:
            credentials, project_id = default()
            self.credentials = credentials
            self.project_id = project_id
            self.auth_method = "adc"
            print(f"Gemini configured with ADC - Project: {project_id}")
            return
        except Exception as e:
            print(f"ADC not available: {e}")
        
        raise RuntimeError("No valid authentication method found for Gemini")
    
    def _get_auth_headers(self) -> dict:
        if self.auth_method == "api_key":
            return {}
        elif self.auth_method in ["adc", "service_account"]:
            if self.credentials:
                self.credentials.refresh(Request())
                return {"Authorization": f"Bearer {self.credentials.token}"}
        return {}
    
    def chat(self, messages: list, stream: bool = True) -> str | Generator[str, None, None]:
        # Choose endpoint based on auth method
        if self.auth_method == "api_key":
            # Use Gemini API endpoint with API Key
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent"
            params = {"key": self.api_key} if self.api_key else {}
            headers = {}
        else:
            # Use Vertex AI endpoint with OAuth token (generateContent, not predict)
            url = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{self.project_id}/locations/us-central1/publishers/google/models/{self.model_name}:generateContent"
            headers = self._get_auth_headers()
            params = {}
        
        # Build request payload based on endpoint
        if self.auth_method == "api_key":
            payload = {
                "contents": [
                    {"role": m["role"], "parts": [{"text": m["content"]}]}
                    for m in messages
                ]
            }
        else:
            # Vertex AI generateContent format (same as Gemini API)
            payload = {
                "contents": [
                    {"role": m["role"], "parts": [{"text": m["content"]}]}
                    for m in messages
                ]
            }
        
        response = requests.post(url, headers=headers, params=params, json=payload, stream=stream)
        
        if response.status_code >= 400:
            error_body = response.text[:500]
            raise RuntimeError(f"LLM API error [{response.status_code}]: {error_body}")
        
        response.raise_for_status()
        
        # For streaming, return generator
        if stream:
            def generate():
                for line in response.iter_lines():
                    if line:
                        yield line.decode('utf-8')
            return generate()
        
        raw_data = response.json()
        # Vertex AI may return a list with one element
        data = raw_data[0] if isinstance(raw_data, list) and len(raw_data) > 0 else raw_data
        
        # Parse response based on endpoint
        if self.auth_method == "api_key":
            if not data.get("candidates"):
                raise RuntimeError(f"Empty response from Gemini: {data}")
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            # Vertex AI generateContent format (same as Gemini API)
            if not data.get("candidates"):
                raise RuntimeError(f"Empty response from Vertex AI: {data}")
            return data["candidates"][0]["content"]["parts"][0]["text"]


class FallbackProvider(BaseProvider):
    """Generic OpenAI-compatible fallback provider"""
    
    def __init__(self, provider_name: str):
        self.name = provider_name
        self.endpoint = os.environ.get(f"{provider_name.upper()}_ENDPOINT")
        self.api_key = os.environ.get(f"{provider_name.upper()}_API_KEY")
    
    def chat(self, messages: list, stream: bool = True) -> str:
        if not self.endpoint or not self.api_key:
            raise ValueError(f"{self.name} not configured")
        
        response = requests.post(
            self.endpoint,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": "default",
                "messages": messages,
                "stream": stream
            },
            timeout=60
        )
        response.raise_for_status()
        
        data = response.json()
        return data["choices"][0]["message"]["content"]


class ProviderRouter:
    """Route requests with automatic failover"""
    
    def __init__(self):
        self.providers = [
            GeminiProvider(),
            # FallbackProvider("VENDOR1"),
            # FallbackProvider("VENDOR2"),
        ]
    
    def chat(self, messages: list, system_prompt: Optional[str] = None) -> str:
        # Prepend system prompt if provided (convert to user message for Vertex AI compatibility)
        if system_prompt:
            messages = [{"role": "user", "content": f"System instruction: {system_prompt}"}] + messages
        
        last_error = None
        
        for provider in self.providers:
            try:
                result = provider.chat(messages, stream=False)
                print(f"✓ Response from {provider.__class__.__name__}")
                return result
            except Exception as e:
                last_error = e
                print(f"✗ {provider.__class__.__name__} failed: {e}")
                continue
        
        raise RuntimeError(f"All providers failed. Last error: {last_error}")