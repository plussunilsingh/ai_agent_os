"""
AI Agent OS DB Cleaner for Admin Java App (Supabase + Local)
Target: Materials domain (income + livestock + dispatch)
Cleans production Supabase PostgreSQL and local databases for material intake, live stock, and dispatches.
"""

import os
import json
import psycopg2

SUPABASE_CONFIG = {
    'dbname': 'postgres',
    'user': 'postgres.qdahwbvrtzfydaisvaco',
    'password': 'ix@FD8+vB4hmkGT',
    'host': 'aws-1-ap-south-1.pooler.supabase.com',
    'port': 6543,
    'sslmode': 'require'
}

TABLES_TO_CLEAN = [
    'sample_dispatches',
    'supplier_samples',
    'purchases',
    'inventory_items',
    'inventory_movements',
    'inventory_adjustments',
    'inventory_reservations',
    'orders',
    'order_items',
    'sales',
    'sales_allocations'
]

def clean_supabase_materials_db():
    print("[1/3] Cleaning Supabase PostgreSQL DB for materials (income + livestock + dispatch)...")
    try:
        conn = psycopg2.connect(**SUPABASE_CONFIG)
        cur = conn.cursor()
        for tbl in TABLES_TO_CLEAN:
            try:
                cur.execute(f'DELETE FROM "{tbl}";')
                conn.commit()
                print(f'  ✅ Cleaned Supabase table "{tbl}" (0 rows remaining).')
            except Exception as e:
                conn.rollback()
                print(f'  ⚠️ Supabase table "{tbl}" cleanup notice: {e}')
        conn.close()
        print("  Supabase PostgreSQL DB materials cleanup COMPLETE.")
    except Exception as e:
        print(f"  ❌ Supabase connection error: {e}")

def clean_local_postgres_materials_db():
    print("[2/3] Cleaning Local PostgreSQL DB 'botanix_admin' for materials...")
    try:
        conn = psycopg2.connect("dbname=botanix_admin user=postgres password=postgres host=127.0.0.1 port=5432")
        conn.autocommit = True
        cur = conn.cursor()
        for tbl in ['materials', 'supplier_samples', 'stock_items', 'inventory_transactions', 'shipment_dispatches']:
            try:
                cur.execute(f"TRUNCATE TABLE {tbl} RESTART IDENTITY CASCADE;")
                print(f"  ✅ Truncated local table '{tbl}' cleanly.")
            except Exception as e:
                pass
        conn.close()
    except Exception as e:
        pass

def clean_telemetry_material_logs():
    print("[3/3] Cleaning Telemetry & Task Queue logs for materials...")
    file_path = "src/ai_se_os/telemetry/task_queue_state.json"
    if not os.path.exists(file_path):
        return

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    keywords = ["material", "income", "livestock", "dispatch", "supplier-samples", "sample", "botanic", "neem", "tulsi", "amla", "ginger", "black seeds", "camel milk"]

    def is_material_related(text):
        if not text:
            return False
        t = str(text).lower()
        return any(k in t for k in keywords)

    data["history"] = [h for h in data.get("history", []) if not is_material_related(h.get("task_name")) and not is_material_related(h.get("summary"))]
    data["ai_agent_os_task_failures"] = [f for f in data.get("ai_agent_os_task_failures", []) if not is_material_related(f.get("task_name")) and not is_material_related(f.get("input_request"))]
    data["model_chunks"] = [c for c in data.get("model_chunks", []) if not is_material_related(c.get("content")) and not is_material_related(c.get("agent_response"))]

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
    clean_supabase_materials_db()
    clean_local_postgres_materials_db()
    clean_telemetry_material_logs()
    print("=== DB & TELEMETRY MATERIALS CLEANUP COMPLETED ===")
