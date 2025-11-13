# EMAIL-ANALYSER

Run the Streamlit dashboard locally:

1. Create and activate a virtual environment (optional but recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Start the Streamlit app:

```powershell
streamlit run app.py
```

Notes:
- The wrapper `app.py` imports the package `email_analyzer.dashboard` so the
	app runs consistently even when filenames overlap. If you prefer, you can
	also run `streamlit run dashboard.py` from the project root.
