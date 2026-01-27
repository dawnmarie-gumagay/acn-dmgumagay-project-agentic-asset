"""
Module for integrating with the Ollama Cloud LLM API via HTTP.

    OllamaCloudGenerateLLM: A CrewAI-compatible wrapper for Ollama Cloud's text generation API.

        model (str): Name of the model to use.
        api_key (Optional[str]): API key for authentication. Defaults to Config.OLLAMA_API_KEY.
        endpoint (str): Base URL for the Ollama Cloud API. Defaults to Config.OLLAMA_BASE_URL.


    Returns False, indicating function calling is not supported.
"""

import json
import requests
from typing import Any, Dict, List, Optional, Union
from crewai import BaseLLM
from config import Config


class OllamaCloudGenerateLLM(BaseLLM):
    def __init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        endpoint: str = Config.OLLAMA_BASE_URL,
        temperature: Optional[float] = None,
        stream: bool = False,
        stop: Optional[List[str]] = None,
        **kwargs,
    ):
        super().__init__(model=model, temperature=temperature)
        self.api_key = api_key or Config.OLLAMA_API_KEY
        if not self.api_key:
            raise RuntimeError("Missing OLLAMA_API_KEY.")

        self.endpoint = endpoint.rstrip("/")
        self._stream = stream
        self.stop = stop or []

    def call(
        self,
        messages: Union[str, List[Dict[str, str]]],
        tools: Optional[List[dict]] = None,
        callbacks: Optional[List[Any]] = None,
        available_functions: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> str:
        # Convert CrewAI message history → prompt
        if isinstance(messages, str):
            prompt = messages
        else:
            # Use last user message as prompt
            prompt = next(
                (m["content"] for m in reversed(messages) if m.get("role") == "user"),
                messages[-1]["content"],
            )

        payload = {
            "model": self.model,
            "prompt": prompt,
        }

        # Add sampling params as needed
        if self.temperature is not None:
            payload["options"] = {"temperature": float(self.temperature)}

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # Streaming path
        if self._stream:
            response_text = []
            with requests.post(
                f"{self.endpoint}/api/generate",
                headers=headers,
                json=payload,
                stream=True,
                timeout=60,
            ) as r:
                r.raise_for_status()
                for line in r.iter_lines(decode_unicode=True):
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                        chunk = obj.get("response", "")
                        if chunk:
                            response_text.append(chunk)
                    except json.JSONDecodeError:
                        # Ignore heartbeat lines
                        continue

            final = "".join(response_text).strip()

        # Non-streaming path
        else:
            print("non-streaming response")
            r = requests.post(
                f"{self.endpoint}/api/generate",
                headers=headers,
                json={**payload, "stream": False},
                timeout=60,
            )
            r.raise_for_status()
            result = r.json()
            final = (result.get("response") or "").strip()

        # Stop‑word truncation
        for sw in self.stop:
            if sw in final:
                final = final.split(sw)[0].strip()
                break

        if not final:
            raise ValueError("Invalid response from LLM call — empty output.")

        return final

    def supports_function_calling(self) -> bool:
        return False

    def get_context_window_size(self) -> int:
        return 8192
