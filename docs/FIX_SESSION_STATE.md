# AI-SE OS Fix Session State
# Written: 2026-07-20 16:03 IST
# Purpose: Token-efficient task reference — read this instead of re-analyzing large context

## STATUS: IN_PROGRESS

## CONFIRMED FIXED (committed to git)
- botanixUI incomingDataHelper.js — quantity/internalBatch/date key mapping
- botanixUI route.js — sampleDispatches→samples alias in proxy unwrapper
- botanixUI IncomingMaterialPage.jsx — setSamples fallback chain
- AI_AGENT_OS stale task reaper (45s TTL in task_queue_tracker.py)
- AI_AGENT_OS 1.5s polling loop (index.html setInterval)
- AI_AGENT_OS active_subagents metric chip (index.html + task_queue_tracker.py)
- AI_AGENT_OS Task History DAG Timeline panel (index.html)
- AI_AGENT_OS DAG engine (cosmetic only — stages are time.sleep stubs — see TO_FIX)

## TO_FIX (4 phases, ordered by priority)

### PHASE 1 — Real Tool Executor
CREATE: src/ai_se_os/orchestrator/real_executor.py
TOOLS NEEDED: http_get, http_post, read_file, write_file, run_shell, verify_json_field
WIRED_INTO: llm_task_runner.py

### PHASE 2 — LLM Reasoning Loop  
CREATE: src/ai_se_os/orchestrator/llm_task_runner.py
LOGIC: system_prompt lists tools in JSON → Ollama parses task → [{tool,args}] → executor runs → feeds result back → loop max 10 iters
USES: src/ai_se_os/execution/ollama_adapter.py (OllamaAdapter.generate)
OLLAMA: http://127.0.0.1:11434, model=qwen2.5:7b, CONFIRMED RUNNING

### PHASE 3 — Replace Dummy DAG Stubs with Real Executor Calls
MODIFY: src/ai_se_os/orchestrator/dag_engine.py
CHANGE: Replace time.sleep(1.0) with llm_task_runner.run(task_name, target_url)

### PHASE 4 — FastAPI endpoint + Rust Bridge
MODIFY: src/ai_se_os/api/routes.py — add POST /agent/execute
MODIFY: src/ai_se_os/rust_engine/src/main.rs — dispatch-task → HTTP POST to FastAPI instead of dummy subprocess

## KEY FILES
- src/ai_se_os/execution/ollama_adapter.py      # OllamaAdapter.generate(prompt, system_prompt)
- src/ai_se_os/telemetry/task_queue_tracker.py  # register_task, update_task_progress, complete_task, log_model_chunk
- src/ai_se_os/orchestrator/dag_engine.py       # STUB — replace time.sleep with real work
- src/ai_se_os/rust_engine/src/main.rs          # POST /api/v1/system/dispatch-task — currently spawns dummy subprocess
- src/ai_se_os/api/routes.py                    # FastAPI routes — add /agent/execute here

## TARGET SERVICES
- Rust Engine: http://127.0.0.1:8000
- FastAPI:     http://127.0.0.1:8001
- BotanixUI:   http://127.0.0.1:9000
- Java Admin:  http://127.0.0.1:8080
- Ollama:      http://127.0.0.1:11434 model=qwen2.5:7b

## LLM TOOL CALL FORMAT
[
  {"tool": "http_post", "url": "http://127.0.0.1:9000/api/admin/inventory/supplier-samples",
   "payload": {"internalBatchNumber": "BATCH-X", "quantity": 100, "status": "Pending", "dispatchType": "SupplierSample"}},
  {"tool": "http_get", "url": "http://127.0.0.1:9000/api/admin/inventory/supplier-samples?page=0&size=100"},
  {"tool": "verify_json_field", "url": "...", "field": "samples[0].internalBatchNumber", "expected": "BATCH-X"},
  {"tool": "run_shell", "cmd": "npm run build", "cwd": "/Users/suniltomar/Desktop/workspace/botanixUI"},
  {"tool": "read_file", "path": "..."},
  {"tool": "write_file", "path": "...", "content": "..."}
]
