import pandas as pd
from pathlib import Path

# mapping of common variants -> canonical column name
_CANONICAL = {
    "date": "Date",
    "dates": "Date",
    "datetime": "Date",
    "timestamp": "Date",
    "time": "Date",
    "from": "From",
    "from_address": "From",
    "sender": "From",
    "to": "To",
    "recipient": "To",
    "recipients": "To",
    "cc": "To",
    "bcc": "To",
    "subject": "Subject",
    "title": "Subject",
    "body": "Body",
    "message": "Body",
    "content": "Body",
    "labels": "Labels",
    "tags": "Labels",
    "category": "Labels",
    "label": "Labels",
}

REQUIRED_COLUMNS = ["Date", "From", "To", "Subject", "Body", "Labels"]

def _normalize_name(name: str) -> str:
    clean=name.strip().lower().replace(" ", "_")
    return _CANONICAL.get(clean, name.strip())

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a copy of df with normalized column names:
    - strip whitespace, lowercase-match to common names (Date, From, To, Subject, Body, Labels)
    """
    new_columns = {}
    for col in df.columns:
        new_columns[col] = _normalize_name(col)
    df = df.rename(columns=new_columns)
    return df

def auto_correct_csv(input_path: str, output_path: str = None, parse_date: bool = True) -> str:
    """
    Load a CSV, normalize columns, ensure required columns exist (add empty ones if needed),
    optionally parse the Date column, and write corrected CSV to output_path.
    Returns the path to the corrected CSV.
    """
    p = Path(input_path)
    if not p.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    df = pd.read_csv(input_path, dtype=str)  # read everything as string initially

    # normalize column names
    df = normalize_columns(df)

    # ensure required columns exist
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = ""  # create an empty column if missing

    # parse Date column if requested
    if parse_date and df["Date"].notna().any():
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True, utc=True)
    # decide output path
    if output_path is None:
        output_path = str(p.with_name(p.stem + "_corrected.csv"))

    # write corrected CSV (index=False to avoid adding an extra column)
    df.to_csv(output_path, index=False)
    print(f"Corrected path generated at {output_path}")
    return output_path


