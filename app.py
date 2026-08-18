import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="AIC Portfolio Command Centre",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# COMPACT ONE-SCREEN STYLE
# ============================================================
st.markdown("""
<style>
#MainMenu, footer, header {visibility:hidden;}
.block-container{padding:.55rem .75rem .25rem .75rem;max-width:100%;}
.title{font-size:1.65rem;font-weight:850;color:#172554;line-height:1;margin:0;}
.subtitle{font-size:.72rem;color:#64748b;margin:2px 0 5px 0;}
.kpi{border-radius:10px;padding:7px 9px;height:65px;border:1px solid #e2e8f0;}
.kpi-label{font-size:9px;font-weight:800;color:#475569;white-space:nowrap;}
.kpi-value{font-size:21px;font-weight:850;color:#0f172a;line-height:1.05;margin-top:3px;}
.blue{background:#eff6ff}.purple{background:#f5f3ff}.cyan{background:#ecfeff}
.green{background:#f0fdf4}.yellow{background:#fefce8}.red{background:#fef2f2}
.section-title{font-size:12px;font-weight:850;color:#1e293b;margin:2px 0 3px 0;}
.progress-box{border:1px solid #e2e8f0;border-radius:8px;padding:5px 7px;margin:3px 0;background:#fff;}
.progress-head{display:flex;justify-content:space-between;font-size:9px;font-weight:750;color:#475569;}
.bar-bg{height:7px;background:#e2e8f0;border-radius:6px;margin-top:3px;overflow:hidden;}
.bar-fill{height:7px;border-radius:6px;background:#2563eb;}
.task-row{display:grid;grid-template-columns:35px 1fr 38px;align-items:center;gap:5px;border:1px solid #e2e8f0;border-radius:7px;padding:4px 6px;margin:3px 0;background:#fff;}
.task-code{font-size:10px;font-weight:900;color:#1d4ed8;}
.task-name{font-size:9px;font-weight:700;color:#334155;white-space:nowrap;}
.task-count{font-size:14px;font-weight:900;text-align:right;color:#0f172a;}
.tool-row{display:grid;grid-template-columns:76px 1fr 25px;align-items:center;gap:5px;margin:3px 0;}
.tool-name{font-size:8.5px;font-weight:700;color:#475569;white-space:nowrap;}
.tool-bg{height:8px;background:#e2e8f0;border-radius:5px;overflow:hidden;}
.tool-fill{height:8px;background:#2563eb;border-radius:5px;}
.tool-count{font-size:9px;font-weight:850;text-align:right;}
.faculty-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:4px;}
.faculty-card{border:1px solid #e2e8f0;border-radius:7px;padding:4px 5px;background:#fff;min-height:37px;}
.faculty-name{font-size:8px;font-weight:800;color:#334155;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.faculty-line{font-size:8px;color:#64748b;}
.faculty-pct{font-size:9px;font-weight:900;}
.action{padding:5px 7px;border-radius:7px;margin:3px 0;font-size:9px;font-weight:750;}
.action-red{background:#fef2f2;color:#991b1b;border-left:4px solid #dc2626}
.action-yellow{background:#fffbeb;color:#92400e;border-left:4px solid #f59e0b}
.action-green{background:#f0fdf4;color:#166534;border-left:4px solid #16a34a}
.detail-box{border:1px solid #e2e8f0;border-radius:10px;padding:10px;background:#fff;margin-top:5px;}
div[data-testid="stVerticalBlock"] > div {gap:.15rem;}

.stButton > button{
    font-size:12px !important;
    font-weight:800 !important;
    padding:9px 6px !important;
    border-radius:9px !important;
    min-height:48px !important;
    white-space:pre-line !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 1000 SYNTHETIC STUDENTS — NO FILE REQUIRED
# ============================================================
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
    section_faculty = {s:f for f,ss in faculty_sections.items() for s in ss}

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
        "ChatGPT","Gemini","Microsoft Copilot","Canva","Gamma",
        "Power BI","Excel","ChatGPT; Canva","ChatGPT; Power BI","Gemini; Canva"
    ]
    statuses = ["Submitted","Pending","Revision Required"]

    rows=[]
    sections=list(section_faculty.keys())

    for i in range(1,1001):
        sec=np.random.choice(sections)
        fac=section_faculty[sec]
        status=np.random.choice(statuses,p=[.80,.14,.06])
        progress={
            "Submitted":np.random.randint(70,101),
            "Pending":np.random.randint(0,61),
            "Revision Required":np.random.randint(45,81)
        }[status]

        attachment = (
            "Submitted – synthetic evidence"
            if status == "Submitted" and np.random.random() < .72
            else ""
        )

        rows.append({
            "Submission ID":f"AIC-SUB-{i:04d}",
            "Timestamp":pd.Timestamp("2026-08-01")+pd.Timedelta(days=int(np.random.randint(0,18))),
            "Student Name":f"Synthetic Student {i:04d}",
            "USN":f"SYN-AIC26-{i:04d}",
            "Section":sec,
            "Faculty":fac,
            "Problem Title":np.random.choice(problems),
            "Problem Description":"Synthetic problem statement for dashboard testing.",
            "Who is Affected":np.random.choice([
                "Students","Faculty and students","Customers",
                "Small business owners","College administration"
            ]),
            "How AI Can Help":np.random.choice([
                "Analyse patterns and generate recommendations",
                "Automate repetitive documentation and communication",
                "Summarise feedback and identify recurring issues",
                "Predict demand and support better decisions",
                "Create dashboards and visual insights"
            ]),
            "Selected Task":np.random.choice(tasks,p=[.30,.28,.42]),
            "Expected Final Outcome":"AI-enabled solution, documented output and evidence of application.",
            "Proposed AI Tool(s)":np.random.choice(tools),
            "Submission Status":status,
            "Problem ID Progress %":progress,
            "Faculty Review Status":(
                "Under Review" if status=="Submitted"
                else "Revision Required" if status=="Revision Required"
                else "Not Submitted"
            ),
            "Evidence / File":attachment
        })
    return pd.DataFrame(rows)

df = make_data()

# ============================================================
# FILTERS
# ============================================================
with st.sidebar:
    st.markdown("## 🎯 AIC Filters")
    faculty_filter=st.multiselect("Faculty",sorted(df.Faculty.unique()))
    section_filter=st.multiselect("Section",sorted(df.Section.unique()))
    status_filter=st.multiselect("Status",sorted(df["Submission Status"].unique()))

filtered=df.copy()
if faculty_filter:
    filtered=filtered[filtered.Faculty.isin(faculty_filter)]
if section_filter:
    filtered=filtered[filtered.Section.isin(section_filter)]
if status_filter:
    filtered=filtered[filtered["Submission Status"].isin(status_filter)]

# ============================================================
# HEADER
# ============================================================
h1,h2=st.columns([8,1])
with h1:
    st.markdown('<div class="title">🎯 AIC Portfolio Challenge</div>',unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Coordinator Command Centre • 1,000 Students • Student-level Submission Monitoring</div>',
        unsafe_allow_html=True
    )
with h2:
    st.markdown('<div style="text-align:right;font-size:9px;color:#16a34a;font-weight:850;">● ACTIVE</div>',unsafe_allow_html=True)

# ============================================================
# KPIs
# ============================================================
total=len(filtered)
submitted=int((filtered["Submission Status"]=="Submitted").sum())
pending=int((filtered["Submission Status"]=="Pending").sum())
revision=int((filtered["Submission Status"]=="Revision Required").sum())
submission_rate=round(submitted/total*100,1) if total else 0
avg_progress=round(filtered["Problem ID Progress %"].mean(),1) if total else 0

cards=[
    ("👥","STUDENTS",total,"blue"),
    ("👨‍🏫","FACULTY",filtered.Faculty.nunique(),"purple"),
    ("🏫","SECTIONS",filtered.Section.nunique(),"cyan"),
    ("📝","SUBMITTED",submitted,"green"),
    ("⏳","PENDING",pending,"yellow"),
    ("⚠️","REVISION",revision,"red")
]
cols=st.columns(6)
for col,(icon,label,value,colour) in zip(cols,cards):
    with col:
        st.markdown(
            f'<div class="kpi {colour}"><div class="kpi-label">{icon} {label}</div>'
            f'<div class="kpi-value">{value:,}</div></div>',
            unsafe_allow_html=True
        )

# ============================================================
# MAIN ANALYTICS
# ============================================================
p1,p2,p3=st.columns([1,1.05,1])

with p1:
    st.markdown('<div class="section-title">📈 Progress — Data Labels</div>',unsafe_allow_html=True)
    for label,val in [("Submission Rate",submission_rate),("Average Progress",avg_progress)]:
        st.markdown(
            f'<div class="progress-box"><div class="progress-head"><span>{label}</span><span>{val:.1f}%</span></div>'
            f'<div class="bar-bg"><div class="bar-fill" style="width:{min(val,100)}%"></div></div></div>',
            unsafe_allow_html=True
        )
    for label,count,fill in [
        ("Submitted",submitted,"#16a34a"),
        ("Pending",pending,"#f59e0b"),
        ("Revision Required",revision,"#dc2626")
    ]:
        pct=round(count/total*100,1) if total else 0
        st.markdown(
            f'<div class="progress-box"><div class="progress-head"><span>{label} ({pct:.1f}%)</span><span>{count}</span></div>'
            f'<div class="bar-bg"><div class="bar-fill" style="width:{pct}%;background:{fill}"></div></div></div>',
            unsafe_allow_html=True
        )

with p2:
    st.markdown('<div class="section-title">🎯 Task Selection — Data Labels</div>',unsafe_allow_html=True)
    counts=filtered["Selected Task"].value_counts()
    for code,name in [
        ("T2","AI-Assisted Business Documentation"),
        ("T3","AI-Assisted Business Presentation"),
        ("T4","AI-Assisted Data Analytics / ERP")
    ]:
        n=int(next((v for k,v in counts.items() if k.startswith(f"Task {code[1:]}")),0))
        pct=round(n/total*100,1) if total else 0
        st.markdown(
            f'<div class="task-row"><div class="task-code">{code}</div>'
            f'<div><div class="task-name">{name}</div>'
            f'<div class="bar-bg"><div class="bar-fill" style="width:{pct}%;height:6px"></div></div></div>'
            f'<div class="task-count">{n}</div></div>',
            unsafe_allow_html=True
        )

with p3:
    st.markdown('<div class="section-title">🤖 AI Tool Adoption — Data Labels</div>',unsafe_allow_html=True)
    tool_names=["ChatGPT","Gemini","Microsoft Copilot","Canva","Gamma","Power BI","Excel"]
    tool_counts={t:int(filtered["Proposed AI Tool(s)"].str.contains(t,case=False,na=False).sum()) for t in tool_names}
    max_tool=max(tool_counts.values()) if tool_counts else 1
    for tool,n in sorted(tool_counts.items(),key=lambda x:x[1],reverse=True):
        pct=n/max_tool*100 if max_tool else 0
        st.markdown(
            f'<div class="tool-row"><div class="tool-name">{tool}</div>'
            f'<div class="tool-bg"><div class="tool-fill" style="width:{pct}%"></div></div>'
            f'<div class="tool-count">{n}</div></div>',
            unsafe_allow_html=True
        )

# ============================================================
# ============================================================
# FACULTY BUTTONS + FACULTY DETAILS
# ============================================================
st.markdown('<div class="section-title">👨‍🏫 Faculty Status — Click a Faculty Name</div>', unsafe_allow_html=True)
st.markdown(
    '<div style="font-size:11px;color:#64748b;margin-bottom:5px;">'
    'Click any Faculty Name to open that faculty\'s details and then search/select a student.'
    '</div>',
    unsafe_allow_html=True
)

if "selected_faculty" not in st.session_state:
    st.session_state.selected_faculty = None

faculty_names = sorted(filtered["Faculty"].unique().tolist())

# Clickable faculty buttons — 4 per row
for row_start in range(0, len(faculty_names), 4):
    row_names = faculty_names[row_start:row_start + 4]
    cols = st.columns(4)
    for j, faculty_name in enumerate(row_names):
        with cols[j]:
            fdf = filtered[filtered["Faculty"] == faculty_name]
            fsubmitted = int((fdf["Submission Status"] == "Submitted").sum())
            ftotal = len(fdf)
            fpct = round(fsubmitted / ftotal * 100, 1) if ftotal else 0
            icon = "🟢" if fpct >= 85 else ("🟡" if fpct >= 70 else "🔴")
            if st.button(
                f"{icon} {faculty_name}\n{fsubmitted}/{ftotal} Submitted ({fpct:.1f}%)",
                key=f"faculty_click_{faculty_name}",
                use_container_width=True
            ):
                st.session_state.selected_faculty = faculty_name

# ------------------------------------------------------------
# Selected faculty details
# ------------------------------------------------------------
if st.session_state.selected_faculty:
    selected_faculty = st.session_state.selected_faculty
    faculty_df = filtered[filtered["Faculty"] == selected_faculty].copy()

    st.markdown(
        f'<div class="section-title">📋 {selected_faculty} — Faculty Details</div>',
        unsafe_allow_html=True
    )

    ftotal = len(faculty_df)
    fsubmitted = int((faculty_df["Submission Status"] == "Submitted").sum())
    fpending = int((faculty_df["Submission Status"] == "Pending").sum())
    frevision = int((faculty_df["Submission Status"] == "Revision Required").sum())
    fsubmission = round(fsubmitted / ftotal * 100, 1) if ftotal else 0
    favg = round(faculty_df["Problem ID Progress %"].mean(), 1) if ftotal else 0

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Students", ftotal)
    c2.metric("Submitted", fsubmitted)
    c3.metric("Pending", fpending)
    c4.metric("Revision", frevision)
    c5.metric("Submission %", f"{fsubmission}%")

    detail_left, detail_mid, detail_right = st.columns([1,1,1])

    with detail_left:
        st.markdown('<div class="section-title">🎯 Tasks</div>', unsafe_allow_html=True)
        task_counts = faculty_df["Selected Task"].value_counts()
        for code, name in [
            ("T2","AI-Assisted Business Documentation"),
            ("T3","AI-Assisted Business Presentation"),
            ("T4","AI-Assisted Data Analytics / ERP")
        ]:
            n = int(next((v for k,v in task_counts.items() if k.startswith(f"Task {code[1:]}")),0))
            st.markdown(
                f'<div class="task-row"><div class="task-code">{code}</div>'
                f'<div class="task-name">{name}</div>'
                f'<div class="task-count">{n}</div></div>',
                unsafe_allow_html=True
            )

    with detail_mid:
        st.markdown('<div class="section-title">📈 Progress</div>', unsafe_allow_html=True)
        for label,count,fill in [
            ("Submitted",fsubmitted,"#16a34a"),
            ("Pending",fpending,"#f59e0b"),
            ("Revision",frevision,"#dc2626")
        ]:
            pct=round(count/ftotal*100,1) if ftotal else 0
            st.markdown(
                f'<div class="progress-box"><div class="progress-head">'
                f'<span>{label}</span><span>{count} ({pct:.1f}%)</span></div>'
                f'<div class="bar-bg"><div class="bar-fill" style="width:{pct}%;background:{fill}"></div></div></div>',
                unsafe_allow_html=True
            )
        st.markdown(
            f'<div class="progress-box"><div class="progress-head">'
            f'<span>Average Progress</span><span>{favg:.1f}%</span></div>'
            f'<div class="bar-bg"><div class="bar-fill" style="width:{favg}%;"></div></div></div>',
            unsafe_allow_html=True
        )

    with detail_right:
        st.markdown('<div class="section-title">🤖 AI Tools</div>', unsafe_allow_html=True)
        for tool in ["ChatGPT","Gemini","Microsoft Copilot","Canva","Gamma","Power BI","Excel"]:
            n=int(faculty_df["Proposed AI Tool(s)"].str.contains(tool,case=False,na=False).sum())
            if n:
                st.markdown(
                    f'<div class="progress-box"><div class="progress-head">'
                    f'<span>{tool}</span><span>{n}</span></div></div>',
                    unsafe_allow_html=True
                )

    # --------------------------------------------------------
    # Search a student inside selected faculty
    # --------------------------------------------------------
    st.markdown(
        f'<div class="section-title">🔎 Search Student — {selected_faculty}</div>',
        unsafe_allow_html=True
    )

    s1,s2 = st.columns([1.15,1])
    with s1:
        search_text = st.text_input(
            "Student Name / USN",
            placeholder="Type student name or USN...",
            key="faculty_student_search"
        )
    with s2:
        student_options = ["Select Student"] + sorted(
            faculty_df["Student Name"].tolist()
        )
        selected_student = st.selectbox(
            "Choose Student",
            student_options,
            key="faculty_student_dropdown"
        )

    student_record = None

    if search_text.strip():
        q=search_text.strip().lower()
        matches=faculty_df[
            faculty_df["Student Name"].str.lower().str.contains(q,na=False) |
            faculty_df["USN"].str.lower().str.contains(q,na=False)
        ]
        if len(matches)==1:
            student_record=matches.iloc[0]
        elif len(matches)>1:
            chosen=st.selectbox(
                "Matching Students",
                matches["Student Name"].tolist(),
                key="faculty_matching_students"
            )
            student_record=matches[matches["Student Name"]==chosen].iloc[0]
        else:
            st.warning("No student found under this faculty.")
    elif selected_student!="Select Student":
        student_record=faculty_df[
            faculty_df["Student Name"]==selected_student
        ].iloc[0]

    if student_record is not None:
        r=student_record
        st.markdown(
            f'<div class="section-title">📝 What {r["Student Name"]} Submitted</div>',
            unsafe_allow_html=True
        )

        a,b,c,d = st.columns(4)
        a.metric("Student",r["Student Name"])
        b.metric("USN",r["USN"])
        c.metric("Status",r["Submission Status"])
        d.metric("Progress",f'{r["Problem ID Progress %"]}%')

        st.markdown(
            f'<div class="detail-box">'
            f'<b>💡 Problem Identified:</b> {r["Problem Title"]}<br><br>'
            f'<b>📝 Problem Description:</b> {r.get("Problem Description","Not Provided")}<br><br>'
            f'<b>👥 Who is Affected:</b> {r.get("Who is Affected","Not Provided")}<br><br>'
            f'<b>🤖 How AI Can Help:</b> {r.get("How AI Can Help","Not Provided")}<br><br>'
            f'<b>🎯 Selected Task:</b> {r["Selected Task"]}<br><br>'
            f'<b>🛠 AI Tool(s):</b> {r["Proposed AI Tool(s)"]}<br><br>'
            f'<b>🎯 Expected Outcome:</b> {r.get("Expected Final Outcome","Not Provided")}<br><br>',
            unsafe_allow_html=True
        )

        attachment=str(r.get("Evidence / File","")).strip()
        if attachment and attachment.lower() not in {"nan","none","null","-"}:
            st.markdown(f'**📎 Attachment:** {attachment}')
        else:
            st.markdown('**📎 Attachment:** No Attachment')

        st.markdown(
            f'**👨‍🏫 Faculty Review:** {r["Faculty Review Status"]}  |  '
            f'**Section:** {r["Section"]}'
        )
        st.markdown('</div>',unsafe_allow_html=True)
    else:
        st.info("Select or search a student to see exactly what the student submitted.")

else:
    st.info("👆 Click a Faculty Name above to open its details.")

st.markdown(
    '<div style="text-align:center;color:#94a3b8;font-size:9px;margin-top:5px;">'
    'AIC Portfolio Challenge • Portfolio Progress Dashboard • Synthetic Demo'
    '</div>',
    unsafe_allow_html=True
)
