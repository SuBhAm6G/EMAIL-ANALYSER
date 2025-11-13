"""
Light wrapper to run the Streamlit app reliably from the project root.

Usage:
  pip install -r requirements.txt
  streamlit run app.py

This simply imports the package dashboard so Streamlit executes the app
in a predictable import context (avoids issues with duplicated filenames).
"""
from pathlib import Path
import sys

# Ensure project root is on sys.path (helps when running from other CWDs)
sys.path.insert(0, str(Path(__file__).parent))

# Import the package dashboard module which contains the Streamlit app code.
import email_analyzer.dashboard  # noqa: F401
