"""
Module for integrating with the Ollama Cloud LLM API via HTTP.

    OllamaCloudGenerateLLM: A CrewAI-compatible wrapper for Ollama Cloud's text generation API.

        model (str): Name of the model to use.
        api_key (Optional[str]): API key for authentication. Defaults to Config.OLLAMA_API_KEY.
        endpoint (str): Base URL for the Ollama Cloud API. Defaults to Config.OLLAMA_BASE_URL.
        temperature (Optional[float]): Sampling temperature for generation. (This is for non-deterministic outputs.)
        stream (bool): Whether to stream the response.


    Returns False, indicating function calling is not supported.
"""

import json
import requests
from typing import Any, Dict, List, Optional, Union
from crewai import BaseLLM
from config import Config


class OllamaCloudGenerateLLM(BaseLLM):
    def __init__(self, model: str, api_key=None, endpoint: str = Config.OLLAMA_BASE_URL,
                 temperature: Optional[float] = Config.DEFAULT_TEMPERATURE, stream=False, **kwargs):
        super().__init__(model=model, temperature=temperature)
        self.api_key = api_key or Config.OLLAMA_API_KEY
        if not self.api_key:
            raise RuntimeError("Missing OLLAMA_API_KEY.")

        self.endpoint = endpoint.rstrip("/")
        self._stream = stream

    def supports_function_calling(self) -> bool:
        return True

    def get_context_window_size(self) -> int:
        return 128000

    def call(self, messages, tools=None, callbacks=None,
             available_functions=None, **kwargs):

        # Must send full messages to /v1/chat/completions
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }

        # Only send tools if we support them
        if tools and self.supports_function_calling():
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        r = requests.post(
            f"{self.endpoint}/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=60,
        )
        r.raise_for_status()
        data = r.json()

        # Extract message
        msg = data["choices"][0]["message"]

        # 1) TOOL CALL BRANCH
        if msg.get("tool_calls"):
            # Return entire message; CrewAI will run the tool
            return msg

        # 2) NORMAL TEXT BRANCH
        content = msg.get("content") or ""
        content = content.strip()
        if not content:
            raise ValueError("Empty LLM output.")
        return content
