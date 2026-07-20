"""
Local File-Backed In-Memory Database for AI-SE OS Interactive Agent
Persists all chat conversation history to local storage (chat_db.json) with zero external setup.
"""

import os
import json
import time
from typing import List, Dict, Any

DB_FILE = os.path.join(os.path.dirname(__file__), "chat_db.json")

class InMemoryChatStore:
    _history: List[Dict[str, Any]] = []

    @classmethod
    def _load(cls):
        if not cls._history:
            if os.path.exists(DB_FILE):
                try:
                    with open(DB_FILE, "r", encoding="utf-8") as f:
                        cls._history = json.load(f)
                except Exception:
                    cls._history = []

    @classmethod
    def _save(cls):
        try:
            with open(DB_FILE, "w", encoding="utf-8") as f:
                json.dump(cls._history, f, indent=2)
        except Exception as e:
            print("Chat DB save error:", e)

    @classmethod
    def get_history(cls) -> List[Dict[str, Any]]:
        """Returns in-memory conversation history."""
        cls._load()
        return cls._history

    @classmethod
    def add_message(cls, sender: str, text: str) -> Dict[str, Any]:
        """Appends a message to the in-memory chat store and persists to local DB."""
        cls._load()
        msg = {
            "id": f"msg-{int(time.time() * 1000)}",
            "sender": sender, # 'user' or 'ai_se_os_agent'
            "text": text,
            "timestamp": time.strftime("%H:%M:%S IST")
        }
        cls._history.append(msg)
        if len(cls._history) > 100:
            cls._history = cls._history[-100:]
        cls._save()
        return msg

    @classmethod
    def clear_history(cls):
        """Clears the in-memory chat store."""
        cls._history = []
        cls._save()
