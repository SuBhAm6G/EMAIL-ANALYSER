import pandas as pd
from typing import Optional

def load_csv(filepath: str) -> pd.DataFrame:
    """
    Simple loader that reads CSV and tries to parse Date if present.
    """
    df = pd.read_csv(filepath, dtype=str)  # read everything as string to avoid surprises
    # attempt to parse Date if present
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce", utc=True, dayfirst=True)
    return df

def basic_clean(df: pd.DataFrame, text_columns: Optional[list] = None) -> pd.DataFrame:
    """
    Lightweight cleaning:
      - fill NaN in text columns with empty string
      - strip whitespace and lowercase
      - normalize Labels into semicolon-separated tokens (no spaces)
    """
    if text_columns is None:
        text_columns = ["Subject", "Body"]

    df = df.copy()  # work on a copy so caller's DataFrame is unchanged

    # Clean text columns
    for col in text_columns:
        if col in df.columns:
            # ensure column exists as string
            df[col] = df[col].fillna("").astype(str).str.strip().str.lower()

    # Normalize Labels column: split on common separators, rejoin with semicolon
    if "Labels" in df.columns:
        def _norm_labels(val):
            if pd.isna(val) or str(val).strip() == "":
                return ""
            s = str(val)
            # replace commas and pipes with semicolons, remove duplicate spaces
            s = s.replace("|", ";").replace(",", ";")
            parts = [p.strip().lower() for p in s.split(";") if p.strip() != ""]
            # deduplicate while preserving order
            seen = set()
            out = []
            for p in parts:
                if p not in seen:
                    seen.add(p)
                    out.append(p)
            return ";".join(out)

        df["Labels"] = df["Labels"].fillna("").astype(str).apply(_norm_labels)

    return df
