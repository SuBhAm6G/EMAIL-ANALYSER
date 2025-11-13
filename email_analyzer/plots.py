# email_analyzer/plots.py
"""
Plotting helpers using Plotly for interactive charts suitable for Streamlit.
Each function returns a `plotly.graph_objs.Figure` or `None` when no data.
"""
from typing import Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def _ensure_dates(df: pd.DataFrame) -> pd.DataFrame:
    if "Date" not in df.columns:
        return pd.DataFrame()
    d = df.dropna(subset=["Date"]).copy()
    if d.empty:
        return pd.DataFrame()
    # normalize to date (drop time)
    d["_date"] = d["Date"].dt.normalize()
    return d


def plot_emails_per_day(df: pd.DataFrame, cmap: str = "viridis") -> Optional[go.Figure]:
    d = _ensure_dates(df)
    if d.empty:
        return None

    counts = d.groupby("_date").size().reset_index(name="count")
    counts = counts.sort_values("_date")

    fig = px.line(counts, x="_date", y="count", markers=True, title="Emails per Day")
    fig.update_traces(line=dict(width=2))
    fig.update_layout(xaxis_title="Date", yaxis_title="Number of Emails", template="plotly_white")
    return fig


def plot_top_senders(df: pd.DataFrame, n: int = 10, cmap: str = "tab10") -> Optional[go.Figure]:
    if "From" not in df.columns:
        return None
    series = (
        df["From"].fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
        .replace("", pd.NA)
        .dropna()
    )
    if series.empty:
        return None
    top = series.value_counts().head(n).rename_axis("sender").reset_index(name="count")
    fig = px.bar(top, x="sender", y="count", title=f"Top {len(top)} Senders", template="plotly_white")
    fig.update_layout(xaxis_tickangle= -45)
    return fig


def plot_top_labels(df: pd.DataFrame, n: int = 10, cmap: str = "Set2") -> Optional[go.Figure]:
    if "Labels" not in df.columns:
        return None
    labels = []
    for s in df["Labels"].fillna(""):
        parts = [p.strip().lower() for p in str(s).split(";") if p.strip()]
        labels.extend(parts)
    if not labels:
        return None
    label_counts = pd.Series(labels).value_counts().head(n).rename_axis("label").reset_index(name="count")
    fig = px.bar(label_counts, x="label", y="count", title=f"Top {len(label_counts)} Labels", template="plotly_white")
    fig.update_layout(xaxis_tickangle= -45)
    return fig
