
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

st.set_page_config(
    page_title="AIC Coordinator Command Centre",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# CONFIG
# -----------------------------
DEFAULT_FILE = Path(__file__).parent / "data" / "synthetic_problem_data.xlsx"

TASK_COLORS = {
    "Task 2 – AI-Assisted Business Documentation": "#4F46E5",
    "Task 3 – AI-Assisted Business Presentation": "#0891B2",
    "Task 4 – AI-Assisted Data Analytics / ERP": "#16A34A",
}

# -----------------------------
# DATA LOADING
# -----------------------------
@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
    elif DEFAULT_FILE.exists():
        df = pd.read_excel(DEFAULT_FILE)
    else:
        return pd.DataFrame()

    df.columns = [str(c).strip() for c in df.columns]

    required = [
        "Timestamp", "Student Name", "USN", "Section", "Faculty",
        "Problem Title", "Problem Description", "Who is Affected",
        "How AI Can Help", "Selected Task", "Expected Final Outcome",
        "Proposed AI Tool(s)", "Own Problem?"
    ]

    for col in required:
        if col not in df.columns:
            df[col] = ""

    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    for col in required:
        if col != "Timestamp":
            df[col] = df[col].fillna("").astype(str).str.strip()

    # If synthetic/real data has no status, assume submitted.
    if "Submission Status" not in df.columns:
        df["Submission Status"] = "Submitted"
    df["Submission Status"] = (
        df["Submission Status"].fillna("Submitted").astype(str).str.strip()
    )

    if "Problem ID Progress %" not in df.columns:
        progress_map = {
            "Submitted": 100,
            "Pending": 0,
            "Revision Required": 60
        }
        df["Problem ID Progress %"] = df["Submission Status"].map(progress_map).fillna(0)

    df["Problem ID Progress %"] = pd.to_numeric(
        df["Problem ID Progress %"], errors="coerce"
    ).fillna(0).clip(0, 100)

    return df


def safe_pct(numerator, denominator):
    return round((numerator / denominator) * 100, 1) if denominator else 0


def make_risk(row):
    status = row.get("Submission Status", "")
    progress = row.get("Problem ID Progress %", 0)

    if status == "Revision Required":
        return "🔴 Revision"
    if status == "Pending":
        return "🔴 Pending"
    if progress < 50:
        return "🟡 At Risk"
    return "🟢 On Track"


# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("🎯 AIC Command Centre")
st.sidebar.caption("Coordinator Dashboard")

uploaded = st.sidebar.file_uploader(
    "Upload Problem Identification responses",
    type=["xlsx", "xls", "csv"]
)

df = load_data(uploaded)

if df.empty:
    st.error("No data available. Upload the Google Form response Excel file.")
    st.stop()

# Filters
st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

faculty_values = sorted([x for x in df["Faculty"].unique() if x])
section_values = sorted([x for x in df["Section"].unique() if x])
task_values = sorted([x for x in df["Selected Task"].unique() if x])
status_values = sorted([x for x in df["Submission Status"].unique() if x])

faculty_filter = st.sidebar.multiselect("Faculty", faculty_values)
section_filter = st.sidebar.multiselect("Section", section_values)
task_filter = st.sidebar.multiselect("Selected Task", task_values)
status_filter = st.sidebar.multiselect("Status", status_values)

filtered = df.copy()

if faculty_filter:
    filtered = filtered[filtered["Faculty"].isin(faculty_filter)]
if section_filter:
    filtered = filtered[filtered["Section"].isin(section_filter)]
if task_filter:
    filtered = filtered[filtered["Selected Task"].isin(task_filter)]
if status_filter:
    filtered = filtered[filtered["Submission Status"].isin(status_filter)]

# -----------------------------
# HEADER
# -----------------------------
st.title("🎯 AIC Portfolio Challenge")
st.subheader("Coordinator Command Centre — Problem Identification")

st.caption(
    "Prototype using synthetic data. Replace the data source with the live Google Form response sheet when ready."
)

# -----------------------------
# KPI CARDS
# -----------------------------
total = len(filtered)
submitted = int((filtered["Submission Status"] == "Submitted").sum())
pending = int((filtered["Submission Status"] == "Pending").sum())
revision = int((filtered["Submission Status"] == "Revision Required").sum())
submission_rate = safe_pct(submitted, total)
avg_progress = round(filtered["Problem ID Progress %"].mean(), 1) if total else 0

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric("Students", total)
c2.metric("Submitted", submitted)
c3.metric("Pending", pending)
c4.metric("Revision", revision)
c5.metric("Submission Rate", f"{submission_rate}%")
c6.metric("Avg Progress", f"{avg_progress}%")

st.divider()

# -----------------------------
# PROGRESS + TASK DISTRIBUTION
# -----------------------------
left, right = st.columns(2)

with left:
    st.markdown("### 📈 Problem Identification Progress")

    progress_data = pd.DataFrame({
        "Metric": ["Submission Rate", "Average Progress"],
        "Percentage": [submission_rate, avg_progress]
    }).set_index("Metric")

    st.bar_chart(progress_data, y="Percentage")

with right:
    st.markdown("### 🎯 Task Selection")

    task_summary = (
        filtered.groupby("Selected Task")
        .size()
        .reset_index(name="Students")
        .sort_values("Students", ascending=False)
    )

    if not task_summary.empty:
        st.bar_chart(task_summary.set_index("Selected Task"))

st.divider()

# -----------------------------
# FACULTY MONITORING
# -----------------------------
st.markdown("### 👨‍🏫 Faculty Monitoring")

faculty_summary = (
    filtered.groupby("Faculty")
    .agg(
        Students=("USN", "count"),
        Submitted=("Submission Status", lambda x: (x == "Submitted").sum()),
        Pending=("Submission Status", lambda x: (x == "Pending").sum()),
        Revision=("Submission Status", lambda x: (x == "Revision Required").sum()),
        Avg_Progress=("Problem ID Progress %", "mean")
    )
    .reset_index()
)

if not faculty_summary.empty:
    faculty_summary["Submission %"] = (
        faculty_summary["Submitted"] / faculty_summary["Students"] * 100
    ).round(1)
    faculty_summary["Avg Progress %"] = faculty_summary["Avg_Progress"].round(1)

    display_cols = [
        "Faculty", "Students", "Submitted", "Pending",
        "Revision", "Submission %", "Avg Progress %"
    ]
    st.dataframe(
        faculty_summary[display_cols].sort_values("Submission %"),
        use_container_width=True,
        hide_index=True
    )

st.divider()

# -----------------------------
# SECTION MONITORING
# -----------------------------
st.markdown("### 🏫 Section Monitoring")

section_summary = (
    filtered.groupby(["Section", "Faculty"])
    .agg(
        Students=("USN", "count"),
        Submitted=("Submission Status", lambda x: (x == "Submitted").sum()),
        Pending=("Submission Status", lambda x: (x == "Pending").sum()),
        Revision=("Submission Status", lambda x: (x == "Revision Required").sum()),
        Avg_Progress=("Problem ID Progress %", "mean")
    )
    .reset_index()
)

if not section_summary.empty:
    section_summary["Submission %"] = (
        section_summary["Submitted"] / section_summary["Students"] * 100
    ).round(1)
    section_summary["Avg Progress %"] = section_summary["Avg_Progress"].round(1)

    st.dataframe(
        section_summary[
            ["Section", "Faculty", "Students", "Submitted",
             "Pending", "Revision", "Submission %", "Avg Progress %"]
        ].sort_values("Submission %"),
        use_container_width=True,
        hide_index=True
    )

st.divider()

# -----------------------------
# AI TOOL ADOPTION
# -----------------------------
st.markdown("### 🤖 Proposed AI Tool Adoption")

tool_counts = {}
tools = [
    "ChatGPT", "Gemini", "Microsoft Copilot", "Canva",
    "Gamma", "Power BI", "Excel"
]

for tool in tools:
    tool_counts[tool] = int(
        filtered["Proposed AI Tool(s)"]
        .str.contains(tool, case=False, na=False)
        .sum()
    )

tool_df = pd.DataFrame.from_dict(
    tool_counts, orient="index", columns=["Students"]
).sort_values("Students", ascending=False)

st.bar_chart(tool_df)

st.divider()

# -----------------------------
# ACTION REQUIRED
# -----------------------------
st.markdown("### 🚨 Action Required")

action_cols = st.columns(4)

action_cols[0].metric(
    "Pending",
    pending,
    help="Students without a submitted Problem Identification"
)

action_cols[1].metric(
    "Revision",
    revision,
    help="Students whose Problem Identification needs revision"
)

low_progress = int((filtered["Problem ID Progress %"] < 50).sum())
action_cols[2].metric(
    "Below 50%",
    low_progress
)

no_problem = int(
    (filtered["Problem Title"].fillna("").str.strip() == "").sum()
)
action_cols[3].metric(
    "Missing Problem",
    no_problem
)

# Action table
action_df = filtered.copy()
action_df["Risk"] = action_df.apply(make_risk, axis=1)

action_df = action_df[
    action_df["Risk"].isin(["🔴 Revision", "🔴 Pending", "🟡 At Risk"])
]

if not action_df.empty:
    st.dataframe(
        action_df[
            ["USN", "Student Name", "Section", "Faculty",
             "Selected Task", "Submission Status",
             "Problem ID Progress %", "Risk"]
        ].sort_values(["Risk", "Faculty"]),
        use_container_width=True,
        hide_index=True
    )
else:
    st.success("No immediate action required for the current filter selection.")

st.divider()

# -----------------------------
# STUDENT SEARCH
# -----------------------------
st.markdown("### 🔎 Student Search")

search = st.text_input(
    "Search by USN, student name, problem title or section"
).strip().lower()

if search:
    mask = (
        filtered["USN"].str.lower().str.contains(search, na=False)
        | filtered["Student Name"].str.lower().str.contains(search, na=False)
        | filtered["Problem Title"].str.lower().str.contains(search, na=False)
        | filtered["Section"].str.lower().str.contains(search, na=False)
    )

    results = filtered[mask]

    if results.empty:
        st.warning("No matching student found.")
    else:
        for _, r in results.iterrows():
            with st.expander(f"{r['Student Name']} — {r['USN']}"):
                a, b, c = st.columns(3)
                a.write(f"**Section:** {r['Section']}")
                b.write(f"**Faculty:** {r['Faculty']}")
                c.write(f"**Task:** {r['Selected Task']}")

                st.write(f"**Problem:** {r['Problem Title']}")
                st.write(f"**Affected:** {r['Who is Affected']}")
                st.write(f"**How AI can help:** {r['How AI Can Help']}")
                st.write(f"**Proposed AI tool(s):** {r['Proposed AI Tool(s)']}")
                st.write(f"**Status:** {r['Submission Status']}")
                st.progress(int(r["Problem ID Progress %"]) / 100)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption(
    "AIC Portfolio Challenge | Coordinator prototype | Synthetic data only"
)
