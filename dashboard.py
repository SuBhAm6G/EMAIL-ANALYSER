# email_analyzer/dashboard.py
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
    page_title="📧 Email Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================== MODERN DESIGN SYSTEM ========================
st.markdown(
    """
    <style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    :root {
        --primary: #3b82f6;
        --primary-dark: #1e40af;
        --secondary: #06b6d4;
        --accent: #f59e0b;
        --success: #10b981;
        --danger: #ef4444;
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-tertiary: #334155;
        --surface: #1e293b;
        --surface-light: #334155;
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --border: #475569;
        --shadow-sm: 0 2px 8px rgba(0,0,0,0.12);
        --shadow-md: 0 8px 24px rgba(0,0,0,0.15);
        --shadow-lg: 0 16px 48px rgba(0,0,0,0.2);
    }
    
    .stApp {
        background: linear-gradient(135deg, var(--bg-primary) 0%, #1a1f35 100%);
        color: var(--text-primary);
    }
    
    .main {
        background: transparent;
        padding-top: 2rem;
    }
    
    .stSidebar {
        background: linear-gradient(180deg, var(--surface) 0%, var(--bg-secondary) 100%);
        border-right: 1px solid var(--border);
    }
    
    [data-testid="stSidebarNav"] {
        padding: 1.5rem 0;
    }
    
    /* ===== HEADER & TITLE ===== */
    .header-container {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(6, 182, 212, 0.05) 100%);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 16px;
        padding: 2.5rem;
        margin-bottom: 2.5rem;
        backdrop-filter: blur(10px);
        animation: fadeIn 0.6s ease-out;
    }
    
    .header-container h1 {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .header-container p {
        color: var(--text-secondary);
        font-size: 1.05rem;
        font-weight: 500;
    }
    
    /* ===== METRIC CARDS ===== */
    .metric-card {
        background: linear-gradient(135deg, var(--surface) 0%, rgba(59, 130, 246, 0.05) 100%);
        border: 1px solid rgba(59, 130, 246, 0.15);
        border-radius: 14px;
        padding: 1.75rem;
        backdrop-filter: blur(8px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: rgba(59, 130, 246, 0.4);
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
    }
    
    .metric-card:hover::before {
        opacity: 1;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.75rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary);
        line-height: 1.2;
    }
    
    .metric-delta {
        font-size: 0.85rem;
        color: var(--text-secondary);
        margin-top: 0.5rem;
    }
    
    /* ===== SECTION TITLES ===== */
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        position: relative;
        padding-bottom: 1rem;
    }
    
    .section-title::after {
        content: '';
        height: 3px;
        width: 40px;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        border-radius: 3px;
    }
    
    /* ===== CARDS & CONTAINERS ===== */
    .stDataFrame {
        background: transparent !important;
    }
    
    [data-testid="stDataFrame"] {
        background: var(--surface) !important;
        border-radius: 12px !important;
        border: 1px solid var(--border) !important;
        overflow: hidden;
    }
    
    [data-testid="stDataFrame"] thead {
        background: rgba(59, 130, 246, 0.1) !important;
    }
    
    [data-testid="stDataFrame"] th {
        color: var(--primary) !important;
        font-weight: 700 !important;
        border-color: var(--border) !important;
    }
    
    [data-testid="stDataFrame"] td {
        border-color: var(--border) !important;
        color: var(--text-primary) !important;
    }
    
    [data-testid="stDataFrame"] tbody tr:hover {
        background: rgba(59, 130, 246, 0.05) !important;
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: var(--shadow-sm);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* ===== FILE UPLOADER ===== */
    [data-testid="stFileUploadDropzone"] {
        border: 2px dashed rgba(59, 130, 246, 0.4) !important;
        border-radius: 12px !important;
        background: rgba(59, 130, 246, 0.02) !important;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploadDropzone"]:hover {
        border-color: var(--primary) !important;
        background: rgba(59, 130, 246, 0.05) !important;
    }
    
    /* ===== SLIDERS & SELECTBOX ===== */
    .stSlider {
        padding: 1.5rem 0;
    }
    
    .stSlider > label {
        color: var(--text-primary) !important;
        font-weight: 600;
    }
    
    .stSelectbox label {
        color: var(--text-primary) !important;
        font-weight: 600;
    }
    
    /* ===== ALERTS & INFO ===== */
    [data-testid="stAlert"] {
        background: rgba(59, 130, 246, 0.1) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
    }
    
    /* ===== DIVIDERS ===== */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border), transparent);
        margin: 2rem 0;
    }
    
    /* ===== ANIMATIONS ===== */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .stPlotlyChart {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(59, 130, 246, 0.6);
    }
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .header-container {
            padding: 1.5rem;
        }
        
        .header-container h1 {
            font-size: 2rem;
        }
        
        .metric-card {
            padding: 1.25rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Fix metric text colors specifically
st.markdown(
    """
    <style>
    div[data-testid="stMetricValue"] { color: var(--primary) !important; }
    div[data-testid="stMetricLabel"] { color: var(--text-secondary) !important; }
    div[data-testid="stMetricDelta"] { color: var(--success) !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ======================== APP CONTENT ========================

# Header
st.markdown(
    """
    <div class="header-container">
        <h1>📧 Email Intelligence Dashboard</h1>
        <p>Deep dive into your email patterns with AI-powered analytics</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    st.markdown("<h3 style='color: var(--primary); margin-bottom: 1.5rem;'>⚙️ Configuration</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("📂 Upload your email CSV", type=["csv"], label_visibility="collapsed")
    
    st.markdown("<hr style='margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    st.markdown("<p style='color: var(--text-secondary); font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1rem;'>Display Settings</p>", unsafe_allow_html=True)
    
    top_n = st.slider("📊 Top N items", min_value=5, max_value=30, value=10, label_visibility="collapsed")
    color_map = st.selectbox(
        "🎨 Color palette",
        ["tab10", "tab20", "Set2", "Set3", "viridis", "plasma", "cividis"],
        index=1,
        label_visibility="collapsed"
    )

if uploaded_file is not None:
    # Save and process file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    st.sidebar.success("✅ File processed successfully!")

    corrected_path = auto_correct_csv(temp_path)
    df = load_csv(corrected_path)
    df = basic_clean(df)

    # Key Statistics
    total = total_emails(df)
    avg_day = avg_emails_per_day(df)
    date_most, count_most = date_with_most_emails(df)

    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">📬 Total Emails</div>
                <div class="metric-value">{total:,}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">📈 Avg Per Day</div>
                <div class="metric-value">{avg_day:.1f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">🔥 Peak Day</div>
                <div class="metric-value">{count_most}</div>
                <div class="metric-delta">{date_most.date() if date_most else 'N/A'}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Top Senders
    st.markdown("<h2 class='section-title'>👥 Top Senders</h2>", unsafe_allow_html=True)
    senders = top_n_senders(df, n=top_n)
    if senders:
        col1, col2 = st.columns([1, 1.5])
        with col1:
            sender_df = pd.DataFrame(senders, columns=["Sender", "Count"])
            st.dataframe(sender_df, use_container_width=True, hide_index=True)
        with col2:
            fig = plot_top_senders(df, n=top_n, cmap=color_map)
            if fig is not None:
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("📭 No sender data available")

    st.markdown("---")

    # Top Labels
    st.markdown("<h2 class='section-title'>🏷️ Email Labels</h2>", unsafe_allow_html=True)
    labels = most_repetitive_label(df, top_n=top_n)
    if labels:
        col1, col2 = st.columns([1, 1.5])
        with col1:
            label_df = pd.DataFrame(labels, columns=["Label", "Count"])
            st.dataframe(label_df, use_container_width=True, hide_index=True)
        with col2:
            fig = plot_top_labels(df, n=top_n, cmap=color_map)
            if fig is not None:
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("🷷 No label data available")

    st.markdown("---")

    # Timeline
    st.markdown("<h2 class='section-title'>📅 Activity Timeline</h2>", unsafe_allow_html=True)
    fig = plot_emails_per_day(df, cmap=color_map)
    if fig is not None:
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown("---")

    # Word Frequency
    st.markdown("<h2 class='section-title'>💬 Most Frequent Words</h2>", unsafe_allow_html=True)
    words = most_frequent_word(df, column="Body", top_n=top_n)
    if words:
        word_df = pd.DataFrame(words, columns=["Word", "Frequency"])
        st.dataframe(word_df, use_container_width=True, hide_index=True)
    else:
        st.info("📖 No meaningful words found")

    os.remove(temp_path)

else:
    st.markdown(
        """
        <div style='
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 60vh;
            text-align: center;
        '>
            <div>
                <div style='font-size: 4rem; margin-bottom: 1.5rem;'>📧</div>
                <h2 style='color: var(--text-primary); margin-bottom: 0.5rem; font-size: 1.75rem;'>Ready to Analyze?</h2>
                <p style='color: var(--text-secondary); font-size: 1.1rem; margin-bottom: 2rem;'>Upload your email CSV file from the sidebar to get started</p>
                <div style='display: flex; gap: 1rem; justify-content: center;'>
                    <div style='background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 10px; padding: 1rem; flex: 1; max-width: 200px;'>
                        <div style='font-size: 2rem; margin-bottom: 0.5rem;'>📊</div>
                        <div style='font-weight: 600; color: var(--primary);'>Analytics</div>
                    </div>
                    <div style='background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 10px; padding: 1rem; flex: 1; max-width: 200px;'>
                        <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🎨</div>
                        <div style='font-weight: 600; color: var(--primary);'>Insights</div>
                    </div>
                    <div style='background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 10px; padding: 1rem; flex: 1; max-width: 200px;'>
                        <div style='font-size: 2rem; margin-bottom: 0.5rem;'>⚡</div>
                        <div style='font-weight: 600; color: var(--primary);'>Speed</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )