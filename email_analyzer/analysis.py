# email_analyzer/analysis.py
import re
from typing import Tuple, List
import pandas as pd
from collections import Counter

def total_emails(df: pd.DataFrame) -> int:
    """Return total number of rows (emails) in the DataFrame."""
    return len(df)

def avg_emails_per_day(df: pd.DataFrame) -> float:
    """
    Compute average emails per day.
    Requires df['Date'] to be datetime-like.
    """
    if "Date" not in df.columns:
        return 0.0
    # drop NA dates, group by date (date part only) and count
    s = df["Date"].dropna().dt.normalize()  # normalize -> midnight of that day
    if s.empty:
        return 0.0
    counts = s.value_counts()  # number of emails per day
    return counts.mean()

def date_with_most_emails(df: pd.DataFrame) -> Tuple[pd.Timestamp, int]:
    """
    Return the date (as Timestamp at midnight UTC/naive) with the most emails and the count.
    If no dates present, returns (None, 0).
    """
    if "Date" not in df.columns or df["Date"].dropna().empty:
        return (None, 0)
    s = df["Date"].dropna().dt.normalize()
    vc = s.value_counts()
    top_date = vc.idxmax()
    return (pd.Timestamp(top_date), int(vc.max()))

def top_n_senders(df: pd.DataFrame, n: int = 10) -> List[Tuple[str, int]]:
    """Return list of (sender, count) sorted by count descending."""
    if "From" not in df.columns:
        return []
    senders = df["From"].fillna("").astype(str).str.strip().str.lower()
    vc = senders[senders != ""].value_counts().head(n)
    return list(vc.items())

_WORD_RE = re.compile(r"\b[a-z0-9']+\b", flags=re.I)

def most_frequent_word(df: pd.DataFrame, column: str = "Body", top_n: int = 1) -> List[Tuple[str, int]]:
    """
    Find most frequent words in a text column.
    Very simple tokenizer: words with letters/numbers/apostrophe.
    Returns list of (word, count) of length up to top_n.
    """
    if column not in df.columns:
        return []
    texts = df[column].fillna("").astype(str).str.lower()
    counter = Counter()
    for t in texts:
        for m in _WORD_RE.finditer(t):
            word = m.group(0)
            if len(word) <= 1:
                continue
            counter[word] += 1
    return counter.most_common(top_n)

def most_repetitive_label(df: pd.DataFrame, top_n: int = 1) -> List[Tuple[str, int]]:
    """
    Expect Labels column to be semicolon-separated (normalized earlier).
    Splits labels, counts frequency, returns top_n labels.
    """
    if "Labels" not in df.columns:
        return []
    labels_series = df["Labels"].fillna("").astype(str)
    counter = Counter()
    for s in labels_series:
        if s.strip() == "":
            continue
        parts = [p.strip().lower() for p in s.split(";") if p.strip() != ""]
        for p in parts:
            counter[p] += 1
    return counter.most_common(top_n)
