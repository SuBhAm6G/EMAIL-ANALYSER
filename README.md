# 📧 Email Analyzer — Interactive Dashboard (Plotly + Streamlit)

A modern, fully-interactive email intelligence dashboard built using **Streamlit**, **Plotly**, **Pandas**, and a custom **Email Analyzer Engine**. Upload any email CSV dataset—Gmail Takeout, Outlook export, or custom logs—or use built-in, realistic sample data to explore trends instantly.

---

## 🚀 Features

### **✔ Smart Data Processing**

* Automatic column normalization (`From`, `To`, `Date`, `Subject`, `Body`, `Labels`)
* CSV auto-correction and cleanup
* Date parsing and email body text cleaning

### **🎨 Elegant Modern UI**

* Custom CSS design system (dark mode optimized)
* Animated metric cards & section titles
* Responsive for desktop, tablet & mobile

### **📊 Interactive Visual Analytics (Plotly)**

* **Top Senders** — horizontal interactive bar chart
* **Email Labels** — donut chart showing label distribution
* **Timeline Analysis** — zoomable email-frequency line chart
* **Most Frequent Words** — table-based word frequency extraction
* **Key Insights** — total emails, average per day, busiest day

### **🧪 Realistic Sample Dataset Generator**

* Generates believable email traffic patterns
* Includes Senders, Labels, Subjects, Timestamps, etc.
* Great for demos or testing

---

## 📁 Project Structure

```
EMAIL-ANALYSER/
│
├── email_analyzer/
│ ├── __init__.py
│ ├── analysis.py
│ ├── cli.py
│ ├── features.py
│ ├── loader.py
│ ├── plots.py
│ ├── preprocess.py
│ └── __pycache__/
│
├── scripts/
│ └── fix_csv.py
│
├── tests/
│
├── data/ # optional sample/input data
│
├── app.py # Streamlit entrypoint
├── dashboard.py # Main dashboard UI
├── requirements.txt
└── README.md
```

---

## 🚀 Live Demo

You can access the fully deployed version of the Email Analyzer here:

👉 **[https://email-analyser-8aecxk7y8pcqi5eng4gyal.streamlit.app/](https://email-analyser-8aecxk7y8pcqi5eng4gyal.streamlit.app/)**

No installation required — everything runs in the cloud.

---

## 📂 CSV Format Requirements

The system automatically normalizes column names. Your file *may* use any of these variants:

| Accepted Names             | Interpreted As |
| -------------------------- | -------------- |
| date, datetime, timestamp  | Date           |
| from, sender, from_address | From           |
| to, recipient, cc, bcc     | To             |
| subject, title             | Subject        |
| body, message, content     | Body           |
| labels, category, tags     | Labels         |

Missing columns are auto-created.

---


## 🔧 Extending the Project

You can easily add:

* Email threading detection
* Sentiment analysis (NLTK/TextBlob)
* Spam classification (ML)
* Attachment parsing
* Category prediction
* User segmentation & communication scoring

If you want any of these modules, just ask & you're free to fork!

---

## 📝 License

MIT License — free for personal & commercial use.

---

Built with ❤️ by **Subham Dhar**
