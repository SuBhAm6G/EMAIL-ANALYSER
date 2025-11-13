# email_analyzer/dashboard.py
# ensure project root is importable when Streamlit runs this file
import streamlit as st
import pandas as pd
from email_analyzer.preprocess import auto_correct_csv
from email_analyzer.loader import load_csv, basic_clean
from email_analyzer.analysis import (
    total_emails,
    avg_emails_per_day,
    date_with_most_emails,
    top_n_senders,
    most_frequent_word,
    most_repetitive_label,
)
from email_analyzer.plots import (
    plot_emails_per_day,
    plot_top_senders,
    plot_top_labels,
)
import tempfile
import os

st.set_page_config(
    page_title="📧 Email Analyzer Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Light-mode, modern styling for Streamlit (keeps layout compatible with Streamlit classnames)
st.markdown(
    """
    <style>
    :root{--bg:#f7fafc;--card:#ffffff;--muted:#6b7280;--accent:#2563eb}
    .stApp { background-color: var(--bg); color: #0f172a; }
    .css-1d391kg, .main { background-color: transparent; }
    .stSidebar { background-color: var(--card); box-shadow: 0 6px 18px rgba(15,23,42,0.06); }
    .stButton>button { background-color: var(--accent); color: white; }
    .stMetric { background-color: var(--card); box-shadow: 0 6px 18px rgba(15,23,42,0.04); border-radius: 8px; }
    .card { background: var(--card); padding: 0.75rem; border-radius: 10px; box-shadow: 0 6px 18px rgba(15,23,42,0.04); }
    .section-title { font-weight:600; color: #0f172a; }
    .stDataFrame table { background: white; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📧 Email Analyzer Dashboard")
st.write("Upload your email CSV and explore insights interactively!")

# --- Sidebar ---
st.sidebar.header("Upload and Settings")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

# Optional settings
top_n = st.sidebar.slider("Top N items to show", min_value=5, max_value=30, value=10)
color_map = st.sidebar.selectbox(
    "Choose color palette",
    ["tab10", "tab20", "Set2", "Set3", "viridis", "plasma", "cividis"],
    index=1
)

if uploaded_file is not None:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    st.sidebar.success("File uploaded successfully ✅")

    # --- Preprocess & Load ---
    corrected_path = auto_correct_csv(temp_path)
    df = load_csv(corrected_path)
    df = basic_clean(df)

    # --- Key Stats ---
    st.subheader("📊 Key Statistics")

    total = total_emails(df)
    avg_day = avg_emails_per_day(df)
    date_most, count_most = date_with_most_emails(df)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Emails", total)
    col2.metric("Avg per Day", f"{avg_day:.2f}")
    col3.metric("Most Emails on", f"{date_most.date() if date_most else 'N/A'} ({count_most})")

    st.markdown("---")

    # --- Top Senders ---
    st.subheader("📬 Top Senders")
    senders = top_n_senders(df, n=top_n)
    if senders:
        sender_df = pd.DataFrame(senders, columns=["Sender", "Count"])
        st.dataframe(sender_df, use_container_width=True)

        # Plot (interactive Plotly)
        fig = plot_top_senders(df, n=top_n, cmap=color_map)
        if fig is not None:
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No sender data found.")

    # --- Top Labels ---
    st.subheader("🏷️ Top Labels")
    labels = most_repetitive_label(df, top_n=top_n)
    if labels:
        label_df = pd.DataFrame(labels, columns=["Label", "Count"])
        st.dataframe(label_df, use_container_width=True)

        fig = plot_top_labels(df, n=top_n, cmap=color_map)
        if fig is not None:
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No label data found.")

    # --- Emails per Day ---
    st.subheader("📅 Emails per Day")
    fig = plot_emails_per_day(df, cmap=color_map)
    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)

    # --- Word Frequency (optional) ---
    st.subheader("💬 Most Frequent Words (Body)")
    words = most_frequent_word(df, column="Body", top_n=top_n)
    if words:
        word_df = pd.DataFrame(words, columns=["Word", "Frequency"])
        st.dataframe(word_df, use_container_width=True)
    else:
        st.info("No meaningful words found in the Body column.")

    # Cleanup temporary file
    os.remove(temp_path)

else:
    st.info("👈 Upload a CSV file from the sidebar to begin.")
