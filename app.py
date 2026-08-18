import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="AIC Portfolio Challenge",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# STYLE
# =========================================================
st.markdown("""
<style>
#MainMenu, footer, header {visibility:hidden;}
.block-container{padding:.8rem 1rem .5rem 1rem;max-width:100%;}
.title{font-size:2.15rem;font-weight:850;color:#172554;line-height:1.05;}
.subtitle{font-size:.95rem;color:#64748b;margin:3px 0 8px;}
.kpi{border-radius:12px;padding:9px 12px;height:78px;border:1px solid #dbe3ee;}
.kpi-label{font-size:11px;font-weight:800;color:#475569;}
.kpi-value{font-size:28px;font-weight:850;color:#0f172a;margin-top:4px;}
.blue{background:#eff6ff}.purple{background:#f5f3ff}.cyan{background:#ecfeff}
.green{background:#f0fdf4}.yellow{background:#fefce8}.red{background:#fef2f2}
.heading{font-size:16px;font-weight:850;color:#1e293b;margin:6px 0 5px;}
.small{font-size:11px;color:#64748b;}
.task{border:1px solid #dbe3ee;border-radius:9px;padding:8px 10px;margin:5px 0;background:white;}
.task-line{display:flex;justify-content:space-between;align-items:center;}
.task-code{font-size:12px;font-weight:900;color:#1d4ed8;}
.task-name{font-size:12px;font-weight:750;color:#334155;}
.task-count{font-size:18px;font-weight:900;color:#0f172a;}
.progress-box{border:1px solid #dbe3ee;border-radius:9px;padding:8px 10px;margin:5px 0;background:white;}
.progress-line{display:flex;justify-content:space-between;font-size:11px;font-weight:750;color:#475569;}
.bar{height:8px;background:#e2e8f0;border-radius:6px;margin-top:5px;overflow:hidden;}
.fill{height:8px;background:#2563eb;border-radius:6px;}
.action{padding:8px 10px;border-radius:9px;margin:5px 0;font-size:11px;font-weight:750;}
.red{background:#fef2f2;color:#991b1b;border-left:5px solid #dc2626;}
.amber{background:#fffbeb;color:#92400e;border-left:5px solid #f59e0b;}
.good{background:#f0fdf4;color:#166534;border-left:5px solid #16a34a;}
.detail{border:1px solid #dbe3ee;border-radius:12px;padding:12px 14px;background:#fff;margin-top:6px;}
.detail-label{font-size:10px;font-weight:850;color:#64748b;text-transform:uppercase;}
.detail-value{font-size:13px;font-weight:650;color:#1e293b;margin:2px 0 8px;}
</style>
""", unsafe_allow_html=True)

# =========================================================
# SYNTHETIC DATA — NO EXCEL / NO EXTERNAL FILE REQUIRED
# =========================================================
@st.cache_data
def make_data():
    np.random.seed(20260818)

    faculty_sections = {
        "Geeta Maladkar":["D","L","O"],
        "Shobha K.B.":["A","B"],
        "Bhawna S.":["J","K"],
        "Rajesh A.":["Q","R2"],
        "B. Manjunath":["M","S"],
        "Vipanchi V.":["T","P"],
        "Dr. M. Maheswari":["C"],
        "Anup A":["G"],
        "Srividhya C.":["I"],
        "Arun":["E"],
        "Purushotham H.C.":["R"],
        "Pankaj Adatiya":["N"],
        "Additional Faculty (Synthetic)":["SYN"]
    }
    section_faculty = {
        section: faculty
        for faculty, sections in faculty_sections.items()
        for section in sections
    }

    problems = [
        "Reducing Food Waste in College Cafeterias",
        "Improving Student Attendance Tracking",
        "Reducing Queue Time at Campus Cafeteria",
        "Improving Retail Inventory Management",
        "Customer Complaint Resolution",
        "Personalized Learning Support",
        "Reducing Paper Usage in Administration",
        "Improving Small Business Social Media",
        "Optimizing Library Book Availability",
        "Reducing Delivery Delays",
        "Improving Waste Segregation",
        "Streamlining Event Registration",
        "Improving Public Transport Information",
        "Reducing Manual Data Entry",
        "Improving Customer Feedback Analysis"
    ]

    tasks = [
        "Task 2 – AI-Assisted Business Documentation",
        "Task 3 – AI-Assisted Business Presentation",
        "Task 4 – AI-Assisted Data Analytics / ERP"
    ]

    tools = [
        "ChatGPT", "Gemini", "Microsoft Copilot", "Canva",
        "Gamma", "Power BI", "Excel", "ChatGPT; Canva",
        "ChatGPT; Power BI", "Gemini; Canva"
    ]

    statuses = ["Submitted", "Pending", "Revision Required"]

    rows = []
    for i in range(1, 1001):
        section = np.random.choice(list(section_faculty))
        faculty = section_faculty[section]
        status = np.random.choice(statuses, p=[.80, .14, .06])

        progress = {
            "Submitted": np.random.randint(70, 101),
            "Pending": np.random.randint(0, 61),
            "Revision Required": np.random.randint(45, 81)
        }[status]

        attachment = (
            "Submitted – synthetic evidence"
            if status == "Submitted" and np.random.random() < .72
            else ""
        )

        rows.append({
            "Submission ID": f"AIC-SUB-{i:04d}",
            "Student Name": f"Synthetic Student {i:04d}",
            "USN": f"SYN-AIC26-{i:04d}",
            "Section": section,
            "Faculty": faculty,
            "Problem Title": np.random.choice(problems),
            "Problem Description":
                "Synthetic problem statement for dashboard testing.",
            "Who is Affected": np.random.choice([
                "Students",
                "Faculty and students",
                "Customers",
                "Small business owners",
                "College administration"
            ]),
            "How AI Can Help": np.random.choice([
                "Analyse patterns and generate recommendations",
                "Automate repetitive documentation and communication",
                "Summarise feedback and identify recurring issues",
                "Predict demand and support better decisions",
                "Create dashboards and visual insights"
            ]),
            "Selected Task": np.random.choice(tasks, p=[.30, .28, .42]),
            "Expected Final Outcome":
                "AI-enabled solution, documented output and evidence of application.",
            "Proposed AI Tool(s)": np.random.choice(tools),
            "Submission Status": status,
            "Progress": progress,
            "Faculty Review": (
                "Under Review" if status == "Submitted"
                else "Revision Required" if status == "Revision Required"
                else "Not Submitted"
            ),
            "Attachment": attachment,
            "Submission Date": (
                pd.Timestamp("2026-08-01") +
                pd.Timedelta(days=int(np.random.randint(0, 18)))
                if status == "Submitted" else None
            )
        })

    return pd.DataFrame(rows)

df = make_data()

# =========================================================
# HEADER
# =========================================================
st.markdown('<div class="title">🎯 AIC Portfolio Challenge</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Portfolio Progress Dashboard • Faculty-wise Monitoring • Student Submission Review</div>',
    unsafe_allow_html=True
)

# =========================================================
# FACULTY SELECTION — MAIN CONTROL
# =========================================================
faculty_list = sorted(df["Faculty"].unique().tolist())

selected_faculty = st.selectbox(
    "👨‍🏫 Select Faculty",
    faculty_list,
    index=0
)

faculty_df = df[df["Faculty"] == selected_faculty].copy()

# =========================================================
# FACULTY OVERVIEW
# =========================================================
total = len(faculty_df)
submitted = int((faculty_df["Submission Status"] == "Submitted").sum())
pending = int((faculty_df["Submission Status"] == "Pending").sum())
revision = int((faculty_df["Submission Status"] == "Revision Required").sum())
rate = round(submitted / total * 100, 1) if total else 0
avg_progress = round(faculty_df["Progress"].mean(), 1) if total else 0

st.markdown(
    f'<div class="heading">👨‍🏫 {selected_faculty} — Faculty Overview</div>',
    unsafe_allow_html=True
)

kpis = [
    ("👥", "STUDENTS", total, "blue"),
    ("📝", "SUBMITTED", submitted, "green"),
    ("⏳", "PENDING", pending, "yellow"),
    ("⚠️", "REVISION", revision, "red"),
    ("📈", "SUBMISSION %", f"{rate:.1f}%", "purple"),
    ("🎯", "AVG PROGRESS", f"{avg_progress:.1f}%", "cyan")
]

cols = st.columns(6)
for col, (icon, label, value, colour) in zip(cols, kpis):
    with col:
        st.markdown(
            f'<div class="kpi {colour}">'
            f'<div class="kpi-label">{icon} {label}</div>'
            f'<div class="kpi-value">{value}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

# =========================================================
# FACULTY ANALYTICS
# =========================================================
left, middle, right = st.columns([1, 1.15, 1])

with left:
    st.markdown('<div class="heading">📈 Submission Progress</div>', unsafe_allow_html=True)

    for label, value, colour in [
        ("Submitted", submitted, "#16a34a"),
        ("Pending", pending, "#f59e0b"),
        ("Revision Required", revision, "#dc2626")
    ]:
        pct = round(value / total * 100, 1) if total else 0
        st.markdown(
            f'<div class="progress-box">'
            f'<div class="progress-line"><span>{label}</span><span>{value} ({pct:.1f}%)</span></div>'
            f'<div class="bar"><div class="fill" style="width:{pct}%;background:{colour};"></div></div>'
            f'</div>',
            unsafe_allow_html=True
        )

with middle:
    st.markdown('<div class="heading">🎯 Tasks Selected</div>', unsafe_allow_html=True)

    task_counts = faculty_df["Selected Task"].value_counts()

    for code, task_name in [
        ("T2", "AI-Assisted Business Documentation"),
        ("T3", "AI-Assisted Business Presentation"),
        ("T4", "AI-Assisted Data Analytics / ERP")
    ]:
        count = int(next(
            (v for k, v in task_counts.items()
             if k.startswith(f"Task {code[1:]}")),
            0
        ))

        st.markdown(
            f'<div class="task">'
            f'<div class="task-line">'
            f'<span><span class="task-code">{code}</span>&nbsp;&nbsp;'
            f'<span class="task-name">{task_name}</span></span>'
            f'<span class="task-count">{count}</span>'
            f'</div></div>',
            unsafe_allow_html=True
        )

with right:
    st.markdown('<div class="heading">🤖 AI Tool Adoption</div>', unsafe_allow_html=True)

    tool_names = [
        "ChatGPT", "Gemini", "Microsoft Copilot",
        "Canva", "Gamma", "Power BI", "Excel"
    ]

    tool_counts = {
        tool: int(
            faculty_df["Proposed AI Tool(s)"]
            .str.contains(tool, case=False, na=False)
            .sum()
        )
        for tool in tool_names
    }

    max_tool = max(tool_counts.values()) if tool_counts else 1

    for tool, count in sorted(
        tool_counts.items(),
        key=lambda x: x[1],
        reverse=True
    ):
        pct = count / max_tool * 100 if max_tool else 0
        st.markdown(
            f'<div class="progress-box">'
            f'<div class="progress-line"><span>{tool}</span><span>{count}</span></div>'
            f'<div class="bar"><div class="fill" style="width:{pct}%;"></div></div>'
            f'</div>',
            unsafe_allow_html=True
        )

# =========================================================
# STUDENT SEARCH
# =========================================================
st.markdown('<div class="heading">🔎 Find a Student</div>', unsafe_allow_html=True)

search_col, select_col = st.columns([1.15, 1])

with search_col:
    search_text = st.text_input(
        "Search by Student Name or USN",
        placeholder="Type student name or USN..."
    )

with select_col:
    student_options = ["Select Student"] + sorted(
        faculty_df["Student Name"].tolist()
    )
    selected_student = st.selectbox(
        "Or choose a student",
        student_options
    )

# Search has priority if entered.
student_record = None

if search_text.strip():
    q = search_text.strip().lower()
    matches = faculty_df[
        faculty_df["Student Name"].str.lower().str.contains(q, na=False) |
        faculty_df["USN"].str.lower().str.contains(q, na=False)
    ]

    if len(matches) == 1:
        student_record = matches.iloc[0]
    elif len(matches) > 1:
        st.info(f"{len(matches)} students found. Choose one from the dropdown.")
        options = matches["Student Name"].tolist()
        chosen = st.selectbox("Matching Students", options)
        student_record = matches[
            matches["Student Name"] == chosen
        ].iloc[0]
    else:
        st.warning("No student found in the selected faculty.")

elif selected_student != "Select Student":
    student_record = faculty_df[
        faculty_df["Student Name"] == selected_student
    ].iloc[0]

# =========================================================
# STUDENT SUBMISSION DETAIL
# =========================================================
if student_record is not None:

    r = student_record

    st.markdown(
        f'<div class="heading">📋 Submission — {r["Student Name"]}</div>',
        unsafe_allow_html=True
    )

    a, b, c, d, e = st.columns(5)

    a.metric("Student", r["Student Name"])
    b.metric("USN", r["USN"])
    c.metric("Section", r["Section"])
    d.metric("Status", r["Submission Status"])
    e.metric("Progress", f'{r["Progress"]}%')

    st.markdown('<div class="detail">', unsafe_allow_html=True)

    d1, d2 = st.columns(2)

    with d1:
        st.markdown('<div class="detail-label">Problem Identified</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="detail-value">{r["Problem Title"]}</div>', unsafe_allow_html=True)

        st.markdown('<div class="detail-label">Problem Description</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="detail-value">{r["Problem Description"]}</div>', unsafe_allow_html=True)

        st.markdown('<div class="detail-label">Who is Affected?</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="detail-value">{r["Who is Affected"]}</div>', unsafe_allow_html=True)

        st.markdown('<div class="detail-label">How Can AI Help?</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="detail-value">{r["How AI Can Help"]}</div>', unsafe_allow_html=True)

    with d2:
        st.markdown('<div class="detail-label">Selected Task</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="detail-value">{r["Selected Task"]}</div>', unsafe_allow_html=True)

        st.markdown('<div class="detail-label">Proposed AI Tool(s)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="detail-value">{r["Proposed AI Tool(s)"]}</div>', unsafe_allow_html=True)

        st.markdown('<div class="detail-label">Expected Final Outcome</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="detail-value">{r["Expected Final Outcome"]}</div>', unsafe_allow_html=True)

        attachment = str(r["Attachment"]).strip()
        if attachment and attachment.lower() not in {"nan", "none", "null", "-"}:
            attachment_text = attachment
        else:
            attachment_text = "No Attachment"

        st.markdown('<div class="detail-label">Attachment</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="detail-value">📎 {attachment_text}</div>',
            unsafe_allow_html=True
        )

        st.markdown('<div class="detail-label">Faculty Review</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="detail-value">{r["Faculty Review"]}</div>', unsafe_allow_html=True)

        submission_date = r["Submission Date"]
        date_text = (
            submission_date.strftime("%d %b %Y")
            if pd.notna(submission_date)
            else "Not Submitted"
        )

        st.markdown('<div class="detail-label">Submission Date</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="detail-value">{date_text}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("Select a student or search by Student Name / USN to view the complete submission.")

st.markdown(
    '<div style="text-align:center;color:#94a3b8;font-size:9px;margin-top:5px;">'
    'AIC Portfolio Challenge • Portfolio Progress Dashboard • Synthetic Data Demo'
    '</div>',
    unsafe_allow_html=True
)
