"""
In-Memory Chat Store for AI-SE OS Interactive Agent
Zero-config in-memory database keeping track of multi-turn conversations.
"""

import time
from typing import List, Dict, Any

class InMemoryChatStore:
    _history: List[Dict[str, Any]] = []

    @classmethod
    def get_history(cls) -> List[Dict[str, Any]]:
        """Returns in-memory conversation history."""
        return cls._history

    @classmethod
    def add_message(cls, sender: str, text: str) -> Dict[str, Any]:
        """Appends a message to the in-memory chat store."""
        msg = {
            "id": f"msg-{int(time.time() * 1000)}",
            "sender": sender, # 'user' or 'ai_se_os_agent'
            "text": text,
            "timestamp": time.strftime("%H:%M:%S IST")
        }
        cls._history.append(msg)
        # Keep latest 100 messages in memory
        if len(cls._history) > 100:
            cls._history = cls._history[-100:]
        return msg

    @classmethod
    def clear_history(cls):
        """Clears the in-memory chat store."""
        cls._history = []
