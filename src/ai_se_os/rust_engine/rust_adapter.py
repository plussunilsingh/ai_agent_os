"""
Rust Native Engine Adapter for AI-SE OS
Bridges high-performance compiled Rust binaries and Python runtime.
"""

import os
import subprocess
import json
from typing import Dict, Any

RUST_ENGINE_DIR = os.path.dirname(__file__)

class RustNativeEngineAdapter:
    @classmethod
    def is_rust_compiled(cls) -> bool:
        """Checks if release binary exists."""
        binary = os.path.join(RUST_ENGINE_DIR, "target", "release", "ai_se_os_rust_engine")
        return os.path.exists(binary)

    @classmethod
    def build_release_binary(cls) -> Dict[str, Any]:
        """Compiles Rust release binary with cargo --release."""
        cargo_bin = os.path.expanduser("~/.cargo/bin/cargo")
        if not os.path.exists(cargo_bin):
            cargo_bin = "cargo"

        res = subprocess.run([cargo_bin, "build", "--release"], cwd=RUST_ENGINE_DIR, capture_output=True, text=True)
        return {
            "success": res.returncode == 0,
            "stdout": res.stdout,
            "stderr": res.stderr
        }

    @classmethod
    def start_rust_engine(cls, port: int = 8000) -> bool:
        """Launches native Rust HTTP Control Plane binary."""
        binary = os.path.join(RUST_ENGINE_DIR, "target", "release", "ai_se_os_rust_engine")
        if not os.path.exists(binary):
            build_res = cls.build_release_binary()
            if not build_res["success"]:
                print("Rust build error:", build_res["stderr"])
                return False

        subprocess.Popen([binary], cwd=RUST_ENGINE_DIR)
        return True
