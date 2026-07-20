"""
AI-SE OS Graph-Augmented Prompt Orchestrator
Compiles zero-hardcoding GraphRAG system prompts using Codebase Knowledge Graph topology and runtime Target Discovery.
Works on any codebase, language, framework, or target project anywhere in the world.
"""

import json
import logging
from typing import Dict, Any, Optional

from ai_se_os.orchestrator.codebase_knowledge_graph import CodebaseKnowledgeGraph
from ai_se_os.orchestrator.target_discovery import TargetDiscoveryEngine

logger = logging.getLogger("GraphPromptOrchestrator")

GRAPH_RAG_SYSTEM_PROMPT_TEMPLATE = """You are AI-SE OS World-Class Autonomous Developer Agent. Respond ONLY with a valid JSON array. No markdown, no prose, no explanations — ever.

OUTPUT FORMAT (strict):
[[{{"tool": "<name>", "<arg>": "<val>", ...}}]]

AVAILABLE TOOLS:
- http_get:          {{"tool":"http_get","url":"<url>"}}
- http_post:         {{"tool":"http_post","url":"<url>","payload":{{}}}}
- read_file:         {{"tool":"read_file","path":"<absolute_path>"}}
- write_file:        {{"tool":"write_file","path":"<absolute_path>","content":"<text>"}}
- run_shell:         {{"tool":"run_shell","cmd":"<bash>","cwd":"<dir>"}}
- verify_json_field: {{"tool":"verify_json_field","url":"<url>","field":"<dot.path>","expected":<value>}}
- done:              {{"tool":"done","summary":"<what was accomplished>"}}

CODEBASE KNOWLEDGE GRAPH TOPOLOGY (Discovered via AST & Graph Analysis):
{knowledge_graph_json}

DYNAMIC TARGET APP API SCHEMA (Discovered via Runtime Probing):
{target_discovery_json}

ZERO-HARDCODING OPERATIONAL RULES:
1. Return ONLY the JSON array — no markdown fences, no explanatory text.
2. Use the discovered Codebase Knowledge Graph & API routes to identify exact endpoints, schemas, and file paths.
3. Upon successfully executing an HTTP POST or state-changing tool where the response contains "id", "success": true, or 200 OK -> immediately call "done".
4. If a tool call encounters an error: analyze the error, adjust parameters, and retry. If unresolvable after 2 attempts: return "done" with failure diagnosis.
5. Keep execution steps efficient: 1-2 tool calls per reasoning iteration.
6. Return raw JSON objects inside array: [[{{"tool":"name"}}]]. Never stringify objects inside array strings.
"""


class GraphPromptOrchestrator:
    """
    Orchestrates zero-hardcoding LLM context generation using GraphRAG codebase topology
    and dynamic target discovery.
    """

    @classmethod
    def compile_graph_prompt(cls, repo_dir: str, target_url: str = "") -> str:
        """
        Builds the Codebase Knowledge Graph and Target Discovery schema, then compiles
        the complete zero-hardcode system prompt.
        """
        # 1. Build Knowledge Graph for the repository
        kg_engine = CodebaseKnowledgeGraph(repo_dir)
        kg_summary = kg_engine.build_graph()

        # 2. Probe target URL for OpenAPI / HTML form schemas
        discovery_summary = TargetDiscoveryEngine.discover_target(target_url) if target_url else {"discovered": False}

        # 3. Format as clean JSON context strings
        kg_json = json.dumps(kg_summary, indent=2)
        target_json = json.dumps(discovery_summary, indent=2)

        return GRAPH_RAG_SYSTEM_PROMPT_TEMPLATE.format(
            knowledge_graph_json=kg_json,
            target_discovery_json=target_json
        )
