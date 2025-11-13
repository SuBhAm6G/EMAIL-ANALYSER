"""
app.py
Runs the top-level dashboard.py as the Streamlit entry point.

Usage:
    streamlit run app.py
"""
from pathlib import Path
import runpy
import sys

# Path to project root (folder containing app.py & dashboard.py)
PROJECT_ROOT = Path(__file__).resolve().parent
DASHBOARD_PATH = PROJECT_ROOT / "dashboard.py"

# Ensure project root is importable
sys.path.insert(0, str(PROJECT_ROOT))

# Sanity check
if not DASHBOARD_PATH.exists():
    raise FileNotFoundError(f"dashboard.py not found at: {DASHBOARD_PATH}")

# Execute dashboard.py as if it were the main Streamlit script
runpy.run_path(str(DASHBOARD_PATH), run_name="__main__")
