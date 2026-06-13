#!/usr/bin/env python3
"""Launcher that starts both FastAPI and Streamlit for HuggingFace Spaces."""

import subprocess
import time
import sys
import os
import signal
import threading
import requests


def wait_for_backend(max_retries=60, timeout=2):
    """Wait for backend to be ready."""
    print("Waiting for backend to be ready...")
    for i in range(max_retries):
        try:
            response = requests.get("http://localhost:8000/health", timeout=timeout)
            if response.status_code == 200:
                print("Backend is ready!")
                return True
        except Exception:
            pass

        if i % 10 == 0:
            print(f"  Attempt {i+1}/{max_retries}...")
        time.sleep(1)

    print("Backend failed to start!")
    return False


def main():
    print("=" * 60)
    print("Starting Autonomous AI Data Analyst")
    print("=" * 60)

    backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
    app_dir = os.path.dirname(os.path.abspath(__file__))

    # Start FastAPI backend
    print("\nStarting FastAPI backend on port 8000...")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app:app",
         "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    # Log backend output in background
    def log_backend():
        for line in backend_process.stdout:
            print(f"[BACKEND] {line}", end="")

    backend_logger = threading.Thread(target=log_backend, daemon=True)
    backend_logger.start()

    # Wait for backend to be ready
    time.sleep(3)
    if not wait_for_backend():
        print("\nBackend failed to start. Exiting.")
        backend_process.terminate()
        sys.exit(1)

    # Start Streamlit
    print("\nStarting Streamlit frontend on port 7860...")
    streamlit_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py",
         "--server.port", "7860",
         "--server.address", "0.0.0.0",
         "--server.headless", "true",
         "--logger.level", "info"],
        cwd=app_dir,
    )

    print("\nAll services started!")
    print("=" * 60)

    # Wait for Streamlit (main process)
    try:
        streamlit_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
        streamlit_process.terminate()
        backend_process.terminate()
        sys.exit(0)


if __name__ == "__main__":
    main()
