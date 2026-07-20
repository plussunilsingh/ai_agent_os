"""
PostgreSQL Permanent Telemetry & Feature Data Persistence Store for AI-SE OS
Manages permanent tables for LLM Token Consumption, Master Task Queue, Chat History, and Failure Logs.
"""

import os
import json
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict, Any, List, Optional

logger = logging.getLogger("PostgresTelemetryStore")

DB_PARAMS = {
    "dbname": os.environ.get("POSTGRES_DB", "ai_se_os_db"),
    "user": os.environ.get("POSTGRES_USER", os.environ.get("USER", "suniltomar")),
    "host": os.environ.get("POSTGRES_HOST", "localhost"),
    "port": int(os.environ.get("POSTGRES_PORT", 5432))
}

class PostgresTelemetryStore:
    @classmethod
    def get_connection(cls):
        """Returns a PostgreSQL connection."""
        return psycopg2.connect(**DB_PARAMS)

    @classmethod
    def initialize_tables(cls):
        """Initializes all required PostgreSQL tables and indices."""
        try:
            with cls.get_connection() as conn:
                with conn.cursor() as cur:
                    # 1. Token Usage Table
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS telemetry_token_usage (
                            id SERIAL PRIMARY KEY,
                            task_id VARCHAR(100),
                            model_name VARCHAR(100) DEFAULT 'qwen2.5:7b',
                            prompt_tokens INT DEFAULT 0,
                            completion_tokens INT DEFAULT 0,
                            total_tokens INT DEFAULT 0,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                    """)

                    # 2. Master Tasks Queue Table
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS telemetry_tasks (
                            task_id VARCHAR(100) PRIMARY KEY,
                            task_name TEXT NOT NULL,
                            target_url TEXT,
                            status VARCHAR(50) DEFAULT 'RUNNING',
                            current_step TEXT,
                            progress_pct INT DEFAULT 0,
                            start_time VARCHAR(100),
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                    """)

                    # 3. Chat History Table
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS telemetry_chat_history (
                            id VARCHAR(100) PRIMARY KEY,
                            sender VARCHAR(50) NOT NULL,
                            text TEXT NOT NULL,
                            timestamp_str VARCHAR(100),
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                    """)

                    # 4. Task Failure Logs Table
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS telemetry_failures (
                            id SERIAL PRIMARY KEY,
                            task_id VARCHAR(100),
                            task_name TEXT,
                            input_request TEXT,
                            failure_reason TEXT,
                            response_payload TEXT,
                            llm_failure TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                    """)

                    conn.commit()
                    logger.info("✅ PostgreSQL Telemetry Tables initialized successfully in ai_se_os_db")
        except Exception as e:
            logger.error(f"PostgreSQL initialization error: {e}")

    @classmethod
    def log_token_usage(cls, task_id: str, prompt_tokens: int, completion_tokens: int, model_name: str = "qwen2.5:7b"):
        """Persists LLM token consumption record into PostgreSQL."""
        try:
            total = prompt_tokens + completion_tokens
            with cls.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO telemetry_token_usage (task_id, model_name, prompt_tokens, completion_tokens, total_tokens)
                        VALUES (%s, %s, %s, %s, %s);
                    """, (task_id, model_name, prompt_tokens, completion_tokens, total))
                    conn.commit()
        except Exception as e:
            logger.error(f"Failed to log token usage to Postgres: {e}")

    @classmethod
    def get_total_tokens(cls) -> Dict[str, int]:
        """Calculates total token usage aggregates from PostgreSQL."""
        try:
            with cls.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("""
                        SELECT 
                            COALESCE(SUM(prompt_tokens), 0) AS prompt_tokens,
                            COALESCE(SUM(completion_tokens), 0) AS completion_tokens,
                            COALESCE(SUM(total_tokens), 0) AS total_tokens
                        FROM telemetry_token_usage;
                    """)
                    row = cur.fetchone()
                    return dict(row) if row else {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        except Exception as e:
            logger.error(f"Failed to fetch total tokens from Postgres: {e}")
            return {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

    @classmethod
    def save_chat_message(cls, msg_id: str, sender: str, text: str, timestamp_str: str):
        """Persists a chat message into PostgreSQL."""
        try:
            with cls.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO telemetry_chat_history (id, sender, text, timestamp_str)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (id) DO UPDATE SET text = EXCLUDED.text;
                    """, (msg_id, sender, text, timestamp_str))
                    conn.commit()
        except Exception as e:
            logger.error(f"Failed to save chat message to Postgres: {e}")

    @classmethod
    def get_chat_history(cls) -> List[Dict[str, Any]]:
        """Retrieves complete chat history from PostgreSQL."""
        try:
            with cls.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("""
                        SELECT id, sender, text, timestamp_str AS timestamp
                        FROM telemetry_chat_history
                        ORDER BY created_at ASC;
                    """)
                    return [dict(r) for r in cur.fetchall()]
        except Exception as e:
            logger.error(f"Failed to fetch chat history from Postgres: {e}")
            return []

    @classmethod
    def register_task(cls, task_id: str, task_name: str, target_url: str):
        """Registers a new active task in PostgreSQL."""
        try:
            with cls.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO telemetry_tasks (task_id, task_name, target_url, status, current_step, progress_pct)
                        VALUES (%s, %s, %s, 'RUNNING', 'Initializing task environment...', 10)
                        ON CONFLICT (task_id) DO UPDATE SET
                            status = 'RUNNING',
                            current_step = 'Initializing task environment...',
                            updated_at = CURRENT_TIMESTAMP;
                    """, (task_id, task_name, target_url))
                    conn.commit()
        except Exception as e:
            logger.error(f"Failed to register task in Postgres: {e}")

    @classmethod
    def log_failure(cls, task_id: str, task_name: str, input_request: str, failure_reason: str, response_payload: str, llm_failure: str):
        """Logs an AI-SE OS failure record in PostgreSQL."""
        try:
            with cls.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO telemetry_failures (task_id, task_name, input_request, failure_reason, response_payload, llm_failure)
                        VALUES (%s, %s, %s, %s, %s, %s);
                    """, (task_id, task_name, input_request[:150], failure_reason, str(response_payload)[:200], str(llm_failure)[:200]))
                    conn.commit()
        except Exception as e:
            logger.error(f"Failed to log failure to Postgres: {e}")

if __name__ == "__main__":
    PostgresTelemetryStore.initialize_tables()
