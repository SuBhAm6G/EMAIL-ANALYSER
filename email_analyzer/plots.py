# email_analyzer/plots.py
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from typing import Optional

def _get_colors(n: int, cmap_name: str = "tab10"):
    """
    Return a list of `n` RGBA colors taken from the named colormap.
    Default uses 'tab10' which is a pleasant qualitative palette.
    """
    cmap = cm.get_cmap(cmap_name)
    # spread samples evenly across the colormap
    return [cmap(i / max(n - 1, 1)) for i in range(n)]

def plot_emails_per_day(df: pd.DataFrame, save_path: Optional[str] = None, cmap: str = "viridis"):
    """
    Plot number of emails per day as a line chart.
    cmap: name of matplotlib colormap (e.g. 'viridis','plasma','tab10','Set2')
    """
    if "Date" not in df.columns:
        print("No 'Date' column found.")
        return

    df = df.copy()
    df = df.dropna(subset=["Date"])
    counts = df["Date"].dt.normalize().value_counts().sort_index()

    dates = counts.index
    values = counts.values

    # choose a single color from the cmap for the line and markers
    cmap_obj = cm.get_cmap(cmap)
    line_color = cmap_obj(0.55)  # pick a mid tone

    plt.figure(figsize=(11, 5))
    plt.plot(dates, values, marker="o", linewidth=2, color=line_color)
    plt.fill_between(dates, values, alpha=0.1, color=line_color)

    plt.title("Emails per Day")
    plt.xlabel("Date")
    plt.ylabel("Number of Emails")
    plt.grid(alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        plt.close()
        print(f"📈 Saved plot to {save_path}")
    else:
        plt.show()


def plot_top_senders(df: pd.DataFrame, n: int = 10, save_path: Optional[str] = None, cmap: str = "tab10"):
    """
    Plot top N senders as a bar chart. Uses a colormap for bar colors.
    """
    if "From" not in df.columns:
        print("No 'From' column found.")
        return

    top_senders = (
        df["From"].fillna("")
        .astype(str)
        .str.lower()
        .str.strip()
        .value_counts()
        .head(n)
    )

    labels = top_senders.index.astype(str)
    values = top_senders.values
    colors = _get_colors(len(values), cmap)

    plt.figure(figsize=(11, 5))
    plt.bar(labels, values, color=colors, edgecolor="black", linewidth=0.4)
    plt.title(f"Top {len(values)} Senders")
    plt.xlabel("Sender")
    plt.ylabel("Email Count")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", alpha=0.25)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        plt.close()
        print(f"📊 Saved plot to {save_path}")
    else:
        plt.show()


def plot_top_labels(df: pd.DataFrame, n: int = 10, save_path: Optional[str] = None, cmap: str = "Set2"):
    """
    Plot top N labels as a bar chart using a colormap.
    """
    if "Labels" not in df.columns:
        print("No 'Labels' column found.")
        return

    labels = []
    for s in df["Labels"].fillna(""):
        parts = [p.strip().lower() for p in s.split(";") if p.strip()]
        labels.extend(parts)

    if not labels:
        print("No labels found to plot.")
        return

    label_counts = pd.Series(labels).value_counts().head(n)
    lbls = label_counts.index.astype(str)
    vals = label_counts.values
    colors = _get_colors(len(vals), cmap)

    plt.figure(figsize=(11, 5))
    plt.bar(lbls, vals, color=colors, edgecolor="black", linewidth=0.4)
    plt.title(f"Top {len(vals)} Labels")
    plt.xlabel("Label")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", alpha=0.25)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        plt.close()
        print(f"🏷️ Saved plot to {save_path}")
    else:
        plt.show()
