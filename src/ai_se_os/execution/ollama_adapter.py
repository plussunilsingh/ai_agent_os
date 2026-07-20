"""
AI-SE OS Ollama Integration Adapter
Connects AI-SE OS to local Ollama server (e.g. qwen2.5:14b)
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
import urllib.request
import urllib.error

logger = logging.getLogger(__name__)

class OllamaAdapter:
    """Adapter to interface AI-SE OS with a local Ollama instance."""
    
    def __init__(
        self,
        host: Optional[str] = None,
        model: Optional[str] = None,
        timeout: int = 60
    ):
        self.host = host or os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
        self.model = model or os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
        self.timeout = timeout
        # Build opener bypassing any local proxies
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

    def check_connection(self) -> bool:
        """Check if Ollama server is running and accessible."""
        try:
            req = urllib.request.Request(f"{self.host}/api/tags")
            with self.opener.open(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    models = [m.get("name") for m in data.get("models", [])]
                    logger.info(f"Connected to Ollama. Available models: {models}")
                    return True
        except Exception as e:
            logger.warning(f"Ollama connection check failed: {e}")
        return False

    def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Generate completion using Ollama local model via native /api/chat or /api/generate endpoints.
        """
        # Inject Truth Governance Policy into System Prompt
        truth_directive = (
            "TRUTH GOVERNANCE POLICY: Never generate simulated metrics, hardcoded response times, "
            "or mock reports. Output only valid executable code targeting the correct repository without markdown prose at the bottom."
        )
        if system_prompt:
            messages.append({"role": "system", "content": f"{system_prompt}\n\n{truth_directive}"})
        else:
            messages.append({"role": "system", "content": truth_directive})
        messages.append({"role": "user", "content": prompt})

        # Payload for /api/chat
        payload_chat = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature}
        }
        
        # Payload for /api/generate fallback
        payload_gen = {
            "model": self.model,
            "prompt": f"{system_prompt}\n\n{prompt}" if system_prompt else prompt,
            "stream": False,
            "options": {"temperature": temperature}
        }

        endpoints = [
            (f"{self.host}/api/chat", payload_chat),
            (f"{self.host}/api/generate", payload_gen),
            (f"{self.host}/v1/chat/completions", payload_chat)
        ]
        
        last_error = None

        for endpoint, payload in endpoints:
            try:
                req = urllib.request.Request(
                    endpoint,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={
                        "Content-Type": "application/json",
                        "User-Agent": "AI-SE-OS"
                    },
                    method="POST"
                )
                with self.opener.open(req, timeout=self.timeout) as response:
                    res_data = json.loads(response.read().decode())
                    
                    # 1. Native /api/chat response
                    if "message" in res_data and isinstance(res_data["message"], dict):
                        content = res_data["message"].get("content", "")
                        return {
                            "success": True,
                            "model": self.model,
                            "response": content,
                            "usage": {"eval_count": res_data.get("eval_count", 0)}
                        }
                    # 2. Native /api/generate response
                    elif "response" in res_data:
                        content = res_data.get("response", "")
                        return {
                            "success": True,
                            "model": self.model,
                            "response": content,
                            "usage": {"eval_count": res_data.get("eval_count", 0)}
                        }
                    # 3. OpenAI /v1/chat/completions response
                    elif "choices" in res_data and len(res_data["choices"]) > 0:
                        content = res_data["choices"][0]["message"].get("content", "")
                        return {
                            "success": True,
                            "model": self.model,
                            "response": content,
                            "usage": res_data.get("usage", {})
                        }
            except Exception as e:
                last_error = e
                logger.warning(f"Ollama call to {endpoint} failed: {e}")

        return {"success": False, "error": f"Ollama connection error: {last_error}"}

    def generate_plan_from_requirement(self, requirement: str, repo_id: str) -> Dict[str, Any]:
        """
        Use Ollama to generate an engineering task plan from a requirement.
        """
        system_prompt = (
            "You are AI-SE OS Engineering Task Planner. Breakdown the requirement "
            "into structured actionable engineering steps."
        )
        user_prompt = f"Requirement for repo '{repo_id}': {requirement}"
        res = self.generate(prompt=user_prompt, system_prompt=system_prompt)
        
        if res.get("success"):
            return {
                "requirement": requirement,
                "repository_id": repo_id,
                "model_used": self.model,
                "plan_output": res.get("response")
            }
        return res
