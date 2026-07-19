"""
AI-SE OS Compact Command
Compresses long chat histories for cache efficiency
"""

import json
from typing import List, Dict, Any
from datetime import datetime


class CompactCommand:
    """
    Compact command for compressing chat histories
    Preserves key information while reducing token usage
    """

    def __init__(self):
        self.compaction_format = """
--- COMPACTED HISTORY ---
Generated: {timestamp}

Timeline:
{timeline}

Decisions:
{decisions}

Outcomes:
{outcomes}

Current State:
{current_state}

Next Steps:
{next_steps}
--------------------------
"""

    def compact(self, history: List[Dict[str, Any]]) -> str:
        """
        Compact chat history into structured summary.

        Args:
            history: List of chat entries

        Returns:
            Compacted summary string
        """
        summary = {
            "timeline": [],
            "decisions": [],
            "outcomes": [],
            "current_state": {},
            "next_steps": []
        }

        for entry in history:
            entry_type = entry.get('type', '')

            if entry_type == 'decision':
                summary["decisions"].append({
                    "id": entry.get('id', ''),
                    "title": entry.get('title', ''),
                    "rationale": entry.get('rationale', '')[:200],
                    "confidence": entry.get('confidence', 0.0)
                })

            elif entry_type == 'outcome':
                summary["outcomes"].append({
                    "description": entry.get('description', ''),
                    "success": entry.get('success', False),
                    "files_changed": entry.get('files_changed', 0)
                })

            elif entry_type == 'task':
                summary["timeline"].append({
                    "task": entry.get('name', ''),
                    "status": entry.get('status', ''),
                    "timestamp": entry.get('timestamp', '')
                })

            elif entry_type == 'state':
                summary["current_state"] = {
                    "files_changed": entry.get('files_changed', []),
                    "tests_passed": entry.get('tests_passed', 0),
                    "issues": entry.get('issues', [])
                }

            elif entry_type == 'next':
                summary["next_steps"].append({
                    "step": entry.get('step', ''),
                    "priority": entry.get('priority', 'medium')
                })

        return self._format_summary(summary)

    def _format_summary(self, summary: Dict[str, Any]) -> str:
        """Format summary with compaction format"""
        return self.compaction_format.format(
            timestamp=datetime.now().isoformat(),
            timeline=json.dumps(summary["timeline"], indent=2),
            decisions=json.dumps(summary["decisions"], indent=2),
            outcomes=json.dumps(summary["outcomes"], indent=2),
            current_state=json.dumps(summary["current_state"], indent=2),
            next_steps=json.dumps(summary["next_steps"], indent=2)
        )

    def auto_compact(self, history: List[Dict[str, Any]], max_tokens: int = 20000) -> str:
        """
        Auto-compact if history exceeds token budget.

        Args:
            history: List of chat entries
            max_tokens: Maximum tokens allowed before compaction

        Returns:
            Compacted summary if needed, original history as string otherwise
        """
        # Approximate token count
        token_count = len(json.dumps(history)) // 4

        if token_count > max_tokens * 0.8:  # 80% threshold
            return self.compact(history)

        return json.dumps(history, indent=2)