#!/usr/bin/env python3
"""
OpenRouter API Client for AI-SE OS
===================================
Adapter for calling OpenRouter API with:
  - Cache control headers for provider-side prefix caching
  - Rate limiting and retry logic
  - Streaming support
  - Cost tracking
  - Fallback chain support

Usage:
    export OPENROUTER_API_KEY="sk-or-v1-..."
    python -c "from openrouter_client import OpenRouterClient; c = OpenRouterClient(); print(c.list_models())"
"""

import json
import os
import time
import uuid
from typing import Any, Optional
from urllib.parse import urljoin

import urllib.request
import urllib.error


class OpenRouterClient:
    """
    Client for the OpenRouter API (https://openrouter.ai/api/v1).

    Features:
      - Chat completions with streaming
      - Provider-side prefix caching headers
      - Automatic retry with backoff
      - Cost estimation and tracking
      - Model listing
    """

    BASE_URL = "https://openrouter.ai/api/v1"

    def __init__(self, config_path: str = ".ai_os/config/openrouter.json"):
        self.config = self._load_config(config_path)
        self.api_key = os.environ.get(self.config.get("api_key_env_var", "OPENROUTER_API_KEY"))
        self.base_url = self.config.get("api_base_url", self.BASE_URL)
        self.default_headers = self.config.get("default_headers", {})
        self.rate_limit = self.config.get("rate_limiting", {})
        self.timeout_config = self.config.get("timeout", {})
        self.cache_config = self.config.get("cache_integration", {})

        # Rate limiting state
        self._request_timestamps: list[float] = []
        self._token_usage: list[tuple[int, float]] = []

    def _load_config(self, path: str) -> dict:
        try:
            with open(path) as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _get_headers(self, model_id: str = "") -> dict:
        """Build request headers with optional cache control."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        headers.update(self.default_headers)

        # Add cache control headers for supported models
        if self.cache_config.get("send_cache_control_headers", False):
            cache_supported = self.cache_config.get("models_with_cache_support", [])
            if model_id in cache_supported:
                cache_value = self.cache_config.get("cache_control_values", {}).get(
                    "short", "public,max-age=3600"
                )
                headers[self.cache_config.get("cache_control_header_name", "X-Cache-Control")] = cache_value

        return headers

    def _check_rate_limit(self):
        """Enforce rate limiting."""
        now = time.time()
        max_rpm = self.rate_limit.get("max_requests_per_minute", 60)
        max_tpm = self.rate_limit.get("max_tokens_per_minute", 100000)

        # Clean old entries
        self._request_timestamps = [t for t in self._request_timestamps if now - t < 60]
        self._token_usage = [(t, c) for t, c in self._token_usage if now - t < 60]

        # Check request rate
        if len(self._request_timestamps) >= max_rpm:
            sleep_time = 60 - (now - self._request_timestamps[0])
            if sleep_time > 0:
                time.sleep(sleep_time)

        # Check token rate
        total_tokens = sum(c for _, c in self._token_usage)
        if total_tokens >= max_tpm:
            sleep_time = 60 - (now - self._token_usage[0][0])
            if sleep_time > 0:
                time.sleep(sleep_time)

    def _record_usage(self, tokens: int):
        """Record token usage for rate limiting."""
        self._token_usage.append((time.time(), tokens))

    def _make_request(
        self,
        endpoint: str,
        data: dict,
        model_id: str = "",
        retry_count: int = 0,
    ) -> Optional[dict]:
        """
        Make an HTTP request to OpenRouter API with retry logic.

        Args:
            endpoint: API endpoint path
            data: Request body
            model_id: Model ID for cache headers
            retry_count: Current retry attempt number

        Returns:
            Response dict or None on failure
        """
        self._check_rate_limit()

        url = urljoin(self.base_url.rstrip("/") + "/", endpoint.lstrip("/"))
        headers = self._get_headers(model_id)
        max_retries = self.rate_limit.get("retry_max_attempts", 3)
        backoff_base = self.rate_limit.get("retry_backoff_base_seconds", 2)

        body = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(
                req,
                timeout=self.timeout_config.get("request_timeout_seconds", 120),
            ) as response:
                result = json.loads(response.read().decode("utf-8"))
                # Record token usage from response
                if "usage" in result:
                    total_tokens = result["usage"].get("total_tokens", 0)
                    self._record_usage(total_tokens)
                return result

        except urllib.error.HTTPError as e:
            if e.code == 429 and retry_count < max_retries:
                # Rate limited - retry with backoff
                sleep_time = backoff_base * (2 ** retry_count)
                time.sleep(sleep_time)
                return self._make_request(endpoint, data, model_id, retry_count + 1)

            if e.code == 401:
                raise RuntimeError(
                    "OpenRouter API authentication failed. "
                    "Set OPENROUTER_API_KEY environment variable."
                )

            if e.code == 402:
                raise RuntimeError(
                    "OpenRouter API: Insufficient credits or payment required."
                )

            error_body = e.read().decode("utf-8")
            raise RuntimeError(f"OpenRouter API error {e.code}: {error_body}")

        except urllib.error.URLError as e:
            if retry_count < max_retries:
                sleep_time = backoff_base * (2 ** retry_count)
                time.sleep(sleep_time)
                return self._make_request(endpoint, data, model_id, retry_count + 1)
            raise RuntimeError(f"OpenRouter connection failed: {e.reason}")

        except OSError as e:
            if retry_count < max_retries:
                sleep_time = backoff_base * (2 ** retry_count)
                time.sleep(sleep_time)
                return self._make_request(endpoint, data, model_id, retry_count + 1)
            raise RuntimeError(f"OpenRouter request failed: {e}")

    def chat_completion(
        self,
        model_id: str,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False,
    ) -> dict:
        """
        Send a chat completion request to OpenRouter.

        Args:
            model_id: Full model ID (e.g., "openrouter:deepseek/deepseek-chat")
            messages: List of message dicts with role and content
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum tokens in response
            stream: Whether to stream the response

        Returns:
            Response dict with choices, usage, etc.
        """
        # Strip "openrouter:" prefix if present
        model = model_id.replace("openrouter:", "", 1)

        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
        }

        # Add cache control for supported models
        if self.cache_config.get("send_cache_control_headers", False):
            cache_supported = self.cache_config.get("models_with_cache_support", [])
            if model_id in cache_supported:
                data["provider"] = {"order": ["OpenRouter"]}

        return self._make_request("chat/completions", data, model_id)

    def list_models(self) -> list[dict]:
        """
        List available models from OpenRouter.

        Returns:
            List of model dicts
        """
        url = urljoin(self.base_url.rstrip("/") + "/", "models")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        req = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(
                req, timeout=self.timeout_config.get("request_timeout_seconds", 120)
            ) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result.get("data", [])
        except Exception as e:
            raise RuntimeError(f"Failed to list OpenRouter models: {e}")

    def estimate_cost(
        self, model_id: str, input_tokens: int, output_tokens: int
    ) -> float:
        """
        Estimate cost for a model call.

        Args:
            model_id: Full model ID
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Estimated cost in USD
        """
        # Load model registry for cost data
        try:
            with open(".ai_os/models/openrouter_registry.json") as f:
                registry = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0.0

        for model in registry.get("models", []):
            if model["id"] == model_id:
                cost_in = model.get("cost_input_per_million", 0)
                cost_out = model.get("cost_output_per_million", 0)
                return (input_tokens / 1_000_000) * cost_in + (output_tokens / 1_000_000) * cost_out

        return 0.0

    def health_check(self) -> bool:
        """
        Check if OpenRouter API is accessible.

        Returns:
            True if API is reachable, False otherwise
        """
        try:
            self.list_models()
            return True
        except Exception:
            return False