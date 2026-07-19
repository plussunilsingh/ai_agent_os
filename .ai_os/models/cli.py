#!/usr/bin/env python3
"""
AI-SE OS CLI - Compact Command and Cache Management
====================================================
Provides CLI commands for:
  - /compact: Compress long chat histories into structured summaries
  - /cache: Inspect and manage cache state
  - /route: Inspect model routing decisions
  - /metrics: View cache and routing metrics

Usage:
    python -m ai_os.models.cli compact --history history.json
    python -m ai_os.models.cli cache --status
    python -m ai_os.models.cli route --task planning
    python -m ai_os.models.cli metrics
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models.cache_service import CacheService
from models.context_compiler import CacheAwareContextCompiler, Task
from models.model_router import OpenRouterModelRouter, TaskType, RiskLevel


def cmd_compact(args):
    """
    Compact command: Compress long chat histories into structured summaries.

    Usage:
        python -m ai_os.models.cli compact --history history.json [--output summary.json]
        python -m ai_os.models.cli compact --auto --session-id <session_id>
    """
    cache_service = CacheService()
    compiler = CacheAwareContextCompiler(cache_service=cache_service)

    if args.auto:
        # Auto-compact: read from runtime state
        history_path = Path(".ai_os_runtime/state/session_history.json")
        if not history_path.exists():
            print(json.dumps({"error": "No session history found"}, indent=2))
            return

        with open(history_path) as f:
            history = json.load(f)

        summary = compiler.compact_history(history)

        # Save compacted summary
        output_path = Path(".ai_os_runtime/cache/history/compacted_latest.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump({
                "session_id": compiler.session_id,
                "sequence": compiler.compaction_sequence,
                "summary": summary,
                "compacted_at": time.time(),
            }, f, indent=2)

        result = {
            "status": "compacted",
            "session_id": compiler.session_id,
            "sequence": compiler.compaction_sequence,
            "summary": summary,
            "cache_metrics": cache_service.get_metrics_snapshot(),
        }
        print(json.dumps(result, indent=2))
        return

    if args.history:
        with open(args.history) as f:
            history = json.load(f)

        summary = compiler.compact_history(history)

        result = {
            "status": "compacted",
            "session_id": compiler.session_id,
            "sequence": compiler.compaction_sequence,
            "summary": summary,
        }

        if args.output:
            with open(args.output, "w") as f:
                json.dump(result, f, indent=2)
            print(f"Compacted summary written to {args.output}")
        else:
            print(json.dumps(result, indent=2))

    # Show token budget info
    if args.budget:
        budget = compiler.get_token_budget()
        print(json.dumps(budget, indent=2))


def cmd_cache(args):
    """
    Cache command: Inspect and manage cache state.

    Usage:
        python -m ai_os.models.cli cache --status
        python -m ai_os.models.cli cache --invalidate --key <cache_key>
        python -m ai_os.models.cli cache --clear-session --session-id <session_id>
        python -m ai_os.models.cli cache --warmup
    """
    cache_service = CacheService()

    if args.status:
        metrics = cache_service.get_metrics_snapshot()
        print(json.dumps(metrics, indent=2))

    if args.invalidate:
        cache_service.invalidate(args.key)
        print(f"Invalidated cache key: {args.key}")

    if args.clear_session:
        cache_service.invalidate_session_history(args.clear_session)
        print(f"Cleared session history: {args.clear_session}")

    if args.warmup:
        # Pre-warm system prefix cache for default models
        models = [
            "openrouter:deepseek/deepseek-chat",
            "openrouter:deepseek/deepseek-chat-v3",
            "openrouter:anthropic/claude-sonnet-4-20250514",
        ]
        for model_id in models:
            content = f"System Role: Engineering Intelligence Agent\nModel: {model_id}\nOS Version: AI-SE OS v3\n"
            cache_service.warmup_system_prefix(
                model_id=model_id,
                tool_list=["chat", "code", "tool_use"],
                policy_version="1.0.0",
                content=content,
            )
            print(f"Warmed cache for: {model_id}")

        metrics = cache_service.get_metrics_snapshot()
        print(f"\nCache metrics after warmup:")
        print(json.dumps(metrics, indent=2))


def cmd_route(args):
    """
    Route command: Inspect model routing decisions.

    Usage:
        python -m ai_os.models.cli route --task planning
        python -m ai_os.models.cli route --task execution --risk high
        python -m ai_os.models.cli route --list-models
    """
    router = OpenRouterModelRouter()

    if args.list_models:
        for model in router.models:
            print(f"  {model['id']:50s} ${model['cost_input_per_million']:.2f}/M in  ${model['cost_output_per_million']:.2f}/M out  role={model.get('routing_role', '')}")
        return

    task_type_map = {
        "planning": TaskType.PLANNING,
        "execution": TaskType.EXECUTION,
        "recovery": TaskType.RECOVERY,
        "analysis": TaskType.ANALYSIS,
        "review": TaskType.REVIEW,
    }
    risk_map = {
        "low": RiskLevel.LOW,
        "medium": RiskLevel.MEDIUM,
        "high": RiskLevel.HIGH,
    }

    task_type = task_type_map.get(args.task, TaskType.EXECUTION)
    risk = risk_map.get(args.risk, RiskLevel.MEDIUM)
    mode = args.mode or ("plan" if task_type == TaskType.PLANNING else "act")

    route = router.route(
        task_type=task_type,
        risk=risk,
        context_tokens=args.tokens or 4000,
        mode=mode,
    )

    print(json.dumps(route.to_dict(), indent=2))


def cmd_metrics(args):
    """
    Metrics command: View cache and routing metrics.

    Usage:
        python -m ai_os.models.cli metrics
        python -m ai_os.models.cli metrics --watch
    """
    cache_service = CacheService()
    metrics = cache_service.get_metrics_snapshot()

    print("=== AI-SE OS Cache Metrics ===")
    print(f"  Hit Rate:        {metrics['hit_rate']:.1%}")
    print(f"  Hits:            {metrics['hits']}")
    print(f"  Misses:          {metrics['misses']}")
    print(f"  Divergence:      {metrics['divergence_count']}")
    print(f"  Evictions:       {metrics['eviction_count']}")
    print(f"  Compactions:     {metrics['compaction_count']}")
    print(f"  Tokens Saved:    {metrics['tokens_saved']}")
    print(f"  Tokens Spent:    {metrics['tokens_spent']}")
    print(f"  Alerts:          {metrics['alerts_raised']}")

    print("\n=== By Layer ===")
    for layer, lm in metrics.get("by_layer", {}).items():
        layer_hits = lm.get("hits", 0)
        layer_misses = lm.get("misses", 0)
        layer_total = layer_hits + layer_misses
        rate = layer_hits / layer_total if layer_total > 0 else 0
        print(f"  {layer:20s}  hits={layer_hits:4d}  misses={layer_misses:4d}  rate={rate:.1%}  saved={lm.get('tokens_saved', 0)}")

    if args.watch:
        try:
            while True:
                time.sleep(5)
                metrics = cache_service.get_metrics_snapshot()
                print(f"\r  Hit Rate: {metrics['hit_rate']:.1%}  Hits: {metrics['hits']}  Misses: {metrics['misses']}  Divergence: {metrics['divergence_count']}", end="")
        except KeyboardInterrupt:
            print("\nStopped.")


def main():
    parser = argparse.ArgumentParser(description="AI-SE OS CLI - Cache and Model Management")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # compact command
    compact_parser = subparsers.add_parser("compact", help="Compress chat histories into structured summaries")
    compact_parser.add_argument("--history", help="Path to session history JSON file")
    compact_parser.add_argument("--output", "-o", help="Output path for compacted summary")
    compact_parser.add_argument("--auto", action="store_true", help="Auto-compact from runtime state")
    compact_parser.add_argument("--session-id", help="Session ID for auto-compact")
    compact_parser.add_argument("--budget", action="store_true", help="Show token budget allocation")

    # cache command
    cache_parser = subparsers.add_parser("cache", help="Inspect and manage cache state")
    cache_parser.add_argument("--status", action="store_true", help="Show cache status and metrics")
    cache_parser.add_argument("--invalidate", action="store_true", help="Invalidate a cache entry")
    cache_parser.add_argument("--key", help="Cache key to invalidate")
    cache_parser.add_argument("--clear-session", help="Clear session history cache")
    cache_parser.add_argument("--warmup", action="store_true", help="Pre-warm system prefix cache")

    # route command
    route_parser = subparsers.add_parser("route", help="Inspect model routing decisions")
    route_parser.add_argument("--task", choices=["planning", "execution", "recovery", "analysis", "review"], default="execution")
    route_parser.add_argument("--risk", choices=["low", "medium", "high"], default="medium")
    route_parser.add_argument("--mode", choices=["plan", "act"], help="Plan or Act mode")
    route_parser.add_argument("--tokens", type=int, default=4000, help="Estimated context tokens")
    route_parser.add_argument("--list-models", action="store_true", help="List all registered models")

    # metrics command
    metrics_parser = subparsers.add_parser("metrics", help="View cache and routing metrics")
    metrics_parser.add_argument("--watch", action="store_true", help="Watch metrics in real-time")

    args = parser.parse_args()

    if args.command == "compact":
        cmd_compact(args)
    elif args.command == "cache":
        cmd_cache(args)
    elif args.command == "route":
        cmd_route(args)
    elif args.command == "metrics":
        cmd_metrics(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()