
import streamlit as st
import pandas as pd
from pathlib import Path

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="AIC Coordinator Command Centre",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CSS — ONE SCREEN, COLOURFUL, COMPACT
# ============================================================
st.markdown("""
<style>
    /* Hide Streamlit chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .block-container {
        padding: 1.0rem 1.4rem 0.5rem 1.4rem;
        max-width: 100%;
    }

    /* Main title */
    .title {
        font-size: 2.0rem;
        font-weight: 800;
        color: #172554;
        margin-bottom: 0;
        line-height: 1.1;
    }

    .subtitle {
        color: #64748B;
        font-size: 0.9rem;
        margin-bottom: 0.6rem;
    }

    /* KPI cards */
    .kpi {
        border-radius: 14px;
        padding: 12px 14px;
        min-height: 92px;
        box-shadow: 0 2px 8px rgba(15,23,42,.08);
        border: 1px solid rgba(148,163,184,.18);
    }

    .kpi-label {
        font-size: 0.78rem;
        font-weight: 700;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: .03em;
    }

    .kpi-value {
        font-size: 1.75rem;
        font-weight: 850;
        color: #0F172A;
        line-height: 1.1;
        margin-top: 4px;
    }

    .kpi-blue { background: #EFF6FF; }
    .kpi-green { background: #F0FDF4; }
    .kpi-yellow { background: #FEFCE8; }
    .kpi-red { background: #FEF2F2; }
    .kpi-purple { background: #F5F3FF; }
    .kpi-cyan { background: #ECFEFF; }

    /* Section cards */
    .section-title {
        font-size: 1.0rem;
        font-weight: 800;
        color: #1E293B;
        margin: 0 0 5px 0;
    }

    .mini-card {
        border-radius: 12px;
        padding: 9px 12px;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        margin-bottom: 5px;
    }

    .mini-name {
        font-size: .78rem;
        font-weight: 700;
        color: #334155;
    }

    .mini-number {
        font-size: 1.1rem;
        font-weight: 800;
        color: #0F172A;
    }

    .action {
        border-radius: 12px;
        padding: 9px 12px;
        margin-bottom: 5px;
        font-size: .82rem;
        font-weight: 650;
    }

    .action-red { background:#FEF2F2; color:#991B1B; border-left:5px solid #DC2626; }
    .action-yellow { background:#FFFBEB; color:#92400E; border-left:5px solid #F59E0B; }
    .action-green { background:#F0FDF4; color:#166534; border-left:5px solid #16A34A; }

    /* Compact dataframe */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
    }

    /* Reduce vertical gaps */
    div[data-testid="stVerticalBlock"] > div {
        gap: 0.25rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #F8FAFC;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA
# ============================================================
DEFAULT_FILE = Path(__file__).parent / "data" / "synthetic_problem_data.xlsx"

@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_excel(DEFAULT_FILE)

    df.columns = [str(c).strip() for c in df.columns]

    for col in [
        "Student Name", "USN", "Section", "Faculty", "Problem Title",
        "Selected Task", "Proposed AI Tool(s)", "Submission Status"
    ]:
        if col not in df.columns:
            df[col] = ""

        df[col] = df[col].fillna("").astype(str).str.strip()

    if "Problem ID Progress %" not in df.columns:
        progress = {
            "Submitted": 100,
            "Pending": 0,
            "Revision Required": 60
        }
        df["Problem ID Progress %"] = (
            df["Submission Status"].map(progress).fillna(0)
        )

    df["Problem ID Progress %"] = pd.to_numeric(
        df["Problem ID Progress %"], errors="coerce"
    ).fillna(0).clip(0, 100)

    return df


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## 🎯 AIC Filters")
    uploaded = st.file_uploader(
        "Replace synthetic data",
        type=["xlsx", "xls", "csv"]
    )

df = load_data(uploaded)

with st.sidebar:
    faculties = sorted(df["Faculty"].dropna().unique().tolist())
    sections = sorted(df["Section"].dropna().unique().tolist())

    faculty_filter = st.multiselect("Faculty", faculties)
    section_filter = st.multiselect("Section", sections)

    if st.button("↻ Reset Filters"):
        st.rerun()

filtered = df.copy()

if faculty_filter:
    filtered = filtered[filtered["Faculty"].isin(faculty_filter)]

if section_filter:
    filtered = filtered[filtered["Section"].isin(section_filter)]

# ============================================================
# KPI CALCULATIONS
# ============================================================
total = len(filtered)
submitted = int((filtered["Submission Status"] == "Submitted").sum())
pending = int((filtered["Submission Status"] == "Pending").sum())
revision = int((filtered["Submission Status"] == "Revision Required").sum())

submission_rate = round(submitted / total * 100, 1) if total else 0
avg_progress = round(filtered["Problem ID Progress %"].mean(), 1) if total else 0

faculty_count = filtered["Faculty"].nunique()
section_count = filtered["Section"].nunique()

# ============================================================
# HEADER
# ============================================================
h1, h2 = st.columns([7, 1])

with h1:
    st.markdown(
        '<div class="title">🎯 AIC Portfolio Challenge</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="subtitle">Coordinator Command Centre • Problem Identification</div>',
        unsafe_allow_html=True
    )

with h2:
    st.markdown(
        '<div style="text-align:right;color:#64748B;font-size:.8rem;">LIVE PROTOTYPE<br>'
        '<b style="color:#16A34A;">● ACTIVE</b></div>',
        unsafe_allow_html=True
    )

# ============================================================
# KPI ROW
# ============================================================
kpis = [
    ("👥", "STUDENTS", total, "kpi-blue"),
    ("👨‍🏫", "FACULTY", faculty_count, "kpi-purple"),
    ("🏫", "SECTIONS", section_count, "kpi-cyan"),
    ("📝", "SUBMITTED", submitted, "kpi-green"),
    ("⏳", "PENDING", pending, "kpi-yellow"),
    ("⚠️", "REVISION", revision, "kpi-red"),
]

cols = st.columns(6)

for col, (icon, label, value, colour) in zip(cols, kpis):
    with col:
        st.markdown(
            f"""
            <div class="kpi {colour}">
                <div class="kpi-label">{icon} {label}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ============================================================
# MIDDLE ROW
# ============================================================
left, middle, right = st.columns([1.15, 1.0, 1.15])

# ---------- OVERALL PROGRESS ----------
with left:
    st.markdown('<div class="section-title">📈 Overall Progress</div>',
                unsafe_allow_html=True)

    progress_df = pd.DataFrame({
        "Metric": ["Submission Rate", "Average Progress"],
        "Value": [submission_rate, avg_progress]
    }).set_index("Metric")

    st.bar_chart(
        progress_df,
        height=190,
        use_container_width=True
    )

# ---------- TASK DISTRIBUTION ----------
with middle:
    st.markdown('<div class="section-title">🎯 Task Selection</div>',
                unsafe_allow_html=True)

    task_df = (
        filtered.groupby("Selected Task")
        .size()
        .reset_index(name="Students")
        .sort_values("Students", ascending=False)
    )

    if not task_df.empty:
        st.bar_chart(
            task_df.set_index("Selected Task"),
            height=190,
            use_container_width=True
        )

# ---------- AI TOOLS ----------
with right:
    st.markdown('<div class="section-title">🤖 AI Tool Adoption</div>',
                unsafe_allow_html=True)

    tools = [
        "ChatGPT", "Gemini", "Microsoft Copilot",
        "Canva", "Gamma", "Power BI", "Excel"
    ]

    tool_counts = {
        tool: int(
            filtered["Proposed AI Tool(s)"]
            .str.contains(tool, case=False, na=False)
            .sum()
        )
        for tool in tools
    }

    tool_df = pd.DataFrame.from_dict(
        tool_counts,
        orient="index",
        columns=["Students"]
    ).sort_values("Students", ascending=False)

    st.bar_chart(
        tool_df,
        height=190,
        use_container_width=True
    )

# ============================================================
# BOTTOM ROW
# ============================================================
left2, right2 = st.columns([1.55, 1])

# ---------- FACULTY ----------
with left2:
    st.markdown('<div class="section-title">👨‍🏫 Faculty Status</div>',
                unsafe_allow_html=True)

    faculty_summary = (
        filtered.groupby("Faculty")
        .agg(
            Students=("USN", "count"),
            Submitted=("Submission Status",
                       lambda x: (x == "Submitted").sum()),
            Pending=("Submission Status",
                     lambda x: (x == "Pending").sum()),
            Revision=("Submission Status",
                      lambda x: (x == "Revision Required").sum()),
        )
        .reset_index()
    )

    faculty_summary["Submission %"] = (
        faculty_summary["Submitted"] /
        faculty_summary["Students"] * 100
    ).round(1)

    # Compact top-level view
    faculty_summary["Status"] = faculty_summary["Submission %"].apply(
        lambda x: "🟢" if x >= 85 else ("🟡" if x >= 70 else "🔴")
    )

    st.dataframe(
        faculty_summary[
            ["Status", "Faculty", "Students",
             "Submitted", "Pending", "Revision", "Submission %"]
        ].sort_values("Submission %", ascending=False),
        use_container_width=True,
        height=225,
        hide_index=True
    )

# ---------- ACTION REQUIRED ----------
with right2:
    st.markdown('<div class="section-title">🚨 Action Required</div>',
                unsafe_allow_html=True)

    low_submission = int(
        (faculty_summary["Submission %"] < 70).sum()
    )

    if pending > 0:
        st.markdown(
            f'<div class="action action-red">🔴 <b>{pending}</b> students pending Problem Identification</div>',
            unsafe_allow_html=True
        )

    if revision > 0:
        st.markdown(
            f'<div class="action action-yellow">🟡 <b>{revision}</b> submissions require revision</div>',
            unsafe_allow_html=True
        )

    if low_submission > 0:
        st.markdown(
            f'<div class="action action-red">🔴 <b>{low_submission}</b> faculty groups below 70%</div>',
            unsafe_allow_html=True
        )

    if submission_rate >= 85:
        st.markdown(
            f'<div class="action action-green">🟢 Overall submission rate is <b>{submission_rate}%</b></div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="action action-yellow">🟡 Overall submission rate is <b>{submission_rate}%</b></div>',
            unsafe_allow_html=True
        )

    st.markdown(
        f'<div class="action action-green">📊 Average Problem ID progress: <b>{avg_progress}%</b></div>',
        unsafe_allow_html=True
    )

# ============================================================
# OPTIONAL STUDENT SEARCH — COMPACT, NO LONG TABLE
# ============================================================
st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

search_col, info_col = st.columns([2, 4])

with search_col:
    search = st.text_input(
        "🔎 Search Student / USN",
        placeholder="Enter USN or student name..."
    ).strip().lower()

with info_col:
    st.markdown(
        "<div style='padding-top:28px;color:#64748B;font-size:.8rem;'>"
        "Use the search only when you need individual student details."
        "</div>",
        unsafe_allow_html=True
    )

if search:
    results = filtered[
        filtered["USN"].str.lower().str.contains(search, na=False)
        | filtered["Student Name"].str.lower().str.contains(search, na=False)
    ]

    if results.empty:
        st.warning("No matching student found.")
    else:
        r = results.iloc[0]

        a, b, c, d = st.columns(4)
        a.metric("Student", r["Student Name"])
        b.metric("Section", r["Section"])
        c.metric("Task", r["Selected Task"].replace("Task ", "T"))
        d.metric("Progress", f"{r['Problem ID Progress %']}%")

        st.info(
            f"**Problem:** {r['Problem Title']}  |  "
            f"**Faculty:** {r['Faculty']}  |  "
            f"**Status:** {r['Submission Status']}"
        )

# ============================================================
# FOOTER
# ============================================================
st.markdown(
    """
    <div style="text-align:center;color:#94A3B8;font-size:.7rem;padding-top:5px;">
        AIC Portfolio Challenge • Coordinator Command Centre • Synthetic Prototype
    </div>
    """,
    unsafe_allow_html=True
)
