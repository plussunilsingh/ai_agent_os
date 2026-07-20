"""
AI Agent OS DB Cleaner for Admin Java App & Telemetry
Target: Materials domain (income + livestock + dispatch)
Cleans PostgreSQL database tables and telemetry logs for material intake, live stock, and dispatches.
"""

import os
import json
import psycopg2

def clean_postgres_materials_db():
    print("[1/2] Cleaning PostgreSQL database 'botanix_admin' for materials (income + livestock + dispatch)...")
    try:
        conn = psycopg2.connect("dbname=botanix_admin user=postgres password=postgres host=127.0.0.1 port=5432")
        conn.autocommit = True
        cur = conn.cursor()

        # DDL Schema Initialization if missing
        cur.execute("""
            CREATE TABLE IF NOT EXISTS materials (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255),
                material_code VARCHAR(100),
                category VARCHAR(100),
                status VARCHAR(50)
            );
            CREATE TABLE IF NOT EXISTS supplier_samples (
                id VARCHAR(36) PRIMARY KEY,
                internal_batch_number VARCHAR(100),
                product_name VARCHAR(255),
                quantity INT,
                status VARCHAR(50),
                dispatch_type VARCHAR(100)
            );
            CREATE TABLE IF NOT EXISTS stock_items (
                id VARCHAR(36) PRIMARY KEY,
                product_name VARCHAR(255),
                quantity INT,
                zone VARCHAR(50)
            );
            CREATE TABLE IF NOT EXISTS inventory_transactions (
                id VARCHAR(36) PRIMARY KEY,
                item_id VARCHAR(36),
                movement_type VARCHAR(50),
                quantity INT
            );
            CREATE TABLE IF NOT EXISTS shipment_dispatches (
                id VARCHAR(36) PRIMARY KEY,
                order_id VARCHAR(36),
                status VARCHAR(50),
                dispatch_type VARCHAR(100)
            );
        """)

        # Truncate / Delete materials, income, livestock, dispatch tables
        tables_to_clean = [
            "materials",
            "supplier_samples",
            "stock_items",
            "inventory_transactions",
            "shipment_dispatches"
        ]

        for tbl in tables_to_clean:
            cur.execute(f"TRUNCATE TABLE {tbl} RESTART IDENTITY CASCADE;")
            print(f"  ✅ Truncated table '{tbl}' cleanly.")

        conn.close()
        print("  PostgreSQL DB 'botanix_admin' materials cleanup COMPLETE.")
    except Exception as e:
        print(f"  ⚠️ PostgreSQL DB notice: {e}")

def clean_telemetry_material_logs():
    print("[2/2] Cleaning Telemetry & Task Queue logs for materials (income + livestock + dispatch)...")
    file_path = "src/ai_se_os/telemetry/task_queue_state.json"
    if not os.path.exists(file_path):
        print("  No telemetry file found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    keywords = ["material", "income", "livestock", "dispatch", "supplier-samples", "sample", "botanic", "tulsi", "amla", "ginger", "black seeds", "camel milk"]

    def is_material_related(text):
        if not text:
            return False
        t = str(text).lower()
        return any(k in t for k in keywords)

    # Filter history
    data["history"] = [h for h in data.get("history", []) if not is_material_related(h.get("task_name")) and not is_material_related(h.get("summary"))]
    # Filter failures
    data["ai_agent_os_task_failures"] = [f for f in data.get("ai_agent_os_task_failures", []) if not is_material_related(f.get("task_name")) and not is_material_related(f.get("input_request"))]
    # Filter model chunks
    data["model_chunks"] = [c for c in data.get("model_chunks", []) if not is_material_related(c.get("content")) and not is_material_related(c.get("agent_response"))]
    # Filter task logs
    task_logs = data.get("task_logs", {})
    cleaned_task_logs = {}
    for tid, logs in task_logs.items():
        if not any(is_material_related(l.get("content")) for l in logs):
            cleaned_task_logs[tid] = logs
    data["task_logs"] = cleaned_task_logs

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("  ✅ Telemetry material logs cleaned successfully.")

if __name__ == "__main__":
    clean_postgres_materials_db()
    clean_telemetry_material_logs()
    print("=== DB & TELEMETRY MATERIALS CLEANUP COMPLETED ===")
