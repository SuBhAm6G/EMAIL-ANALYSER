# app.py
"""
Simple Streamlit entry that makes sure the repo root is importable,
then imports and runs your top-level dashboard module.
"""
import sys
from pathlib import Path

# Ensure project root is on sys.path so imports like "email_analyzer.*" work.
REPO_ROOT = str(Path(__file__).parent.resolve())
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# Import the dashboard (this file contains the Streamlit UI)
# Keep the import at module level so Streamlit can discover it.
import dashboard  # noqa: F401
