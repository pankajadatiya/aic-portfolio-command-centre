
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="AIC Coordinator Command Centre",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- STYLE ----------
st.markdown("""
<style>
#MainMenu, footer, header {visibility:hidden;}
.block-container {padding: 1rem 1.2rem 0.5rem 1.2rem; max-width:100%;}
h1 {color:#172554; margin-bottom:0;}
.subtitle {color:#64748b; margin-bottom:8px;}
.kpi {border-radius:14px;padding:12px 14px;height:88px;border:1px solid #e2e8f0;}
.kpi-label {font-size:12px;font-weight:700;color:#475569;}
.kpi-value {font-size:27px;font-weight:800;color:#0f172a;margin-top:5px;}
.blue{background:#eff6ff}.purple{background:#f5f3ff}.cyan{background:#ecfeff}
.green{background:#f0fdf4}.yellow{background:#fefce8}.red{background:#fef2f2}
.section-title{font-size:17px;font-weight:800;color:#1e293b;margin:3px 0;}
.action{padding:9px 11px;border-radius:10px;margin:5px 0;font-size:13px;font-weight:650;}
.action-red{background:#fef2f2;color:#991b1b;border-left:5px solid #dc2626;}
.action-yellow{background:#fffbeb;color:#92400e;border-left:5px solid #f59e0b;}
.action-green{background:#f0fdf4;color:#166534;border-left:5px solid #16a34a;}
</style>
""", unsafe_allow_html=True)

# ---------- SYNTHETIC DATA ----------
@st.cache_data
def make_data():
    np.random.seed(42)

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
    }

    section_faculty = {
        s:f for f, ss in faculty_sections.items() for s in ss
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
        "Reducing Manual Data Entry",
        "Improving Customer Feedback Analysis"
    ]

    tasks = [
        "Task 2 – Documentation",
        "Task 3 – Presentation",
        "Task 4 – Data Analytics / ERP"
    ]

    tools = [
        "ChatGPT","Gemini","Microsoft Copilot","Canva",
        "Gamma","Power BI","Excel","ChatGPT; Canva",
        "ChatGPT; Power BI","Gemini; Canva"
    ]

    statuses = ["Submitted","Pending","Revision Required"]

    rows=[]
    sections=list(section_faculty.keys())

    for i in range(1,51):
        sec=np.random.choice(sections)
        faculty=section_faculty[sec]
        status=np.random.choice(statuses,p=[.76,.16,.08])
        progress={
            "Submitted":np.random.randint(70,101),
            "Pending":np.random.randint(0,61),
            "Revision Required":np.random.randint(45,81)
        }[status]

        rows.append({
            "USN":f"SYN-AIC26-{i:03d}",
            "Student":f"Synthetic Student {i:02d}",
            "Section":sec,
            "Faculty":faculty,
            "Problem":np.random.choice(problems),
            "Task":np.random.choice(tasks,p=[.30,.28,.42]),
            "AI Tool":np.random.choice(tools),
            "Status":status,
            "Progress":progress
        })

    return pd.DataFrame(rows)

df=make_data()

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## 🎯 Filters")
    faculty_filter=st.multiselect("Faculty",sorted(df.Faculty.unique()))
    section_filter=st.multiselect("Section",sorted(df.Section.unique()))

filtered=df.copy()

if faculty_filter:
    filtered=filtered[filtered.Faculty.isin(faculty_filter)]
if section_filter:
    filtered=filtered[filtered.Section.isin(section_filter)]

# ---------- HEADER ----------
c1,c2=st.columns([7,1])
with c1:
    st.markdown("<h1>🎯 AIC Portfolio Challenge</h1>",unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Coordinator Command Centre • Problem Identification • Synthetic Demo</div>',
        unsafe_allow_html=True)
with c2:
    st.markdown(
        '<div style="text-align:right;color:#16a34a;font-weight:700;">● ACTIVE</div>',
        unsafe_allow_html=True)

# ---------- KPIs ----------
total=len(filtered)
submitted=int((filtered.Status=="Submitted").sum())
pending=int((filtered.Status=="Pending").sum())
revision=int((filtered.Status=="Revision Required").sum())
rate=round(submitted/total*100,1) if total else 0
avg=round(filtered.Progress.mean(),1) if total else 0

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
            f'<div class="kpi-value">{value}</div></div>',
            unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>",unsafe_allow_html=True)

# ---------- THREE PANELS ----------
a,b,c=st.columns([1,1,1])

with a:
    st.markdown('<div class="section-title">📈 Overall Progress</div>',unsafe_allow_html=True)
    p=pd.DataFrame({"Value":[rate,avg]},index=["Submission Rate","Avg Progress"])
    st.bar_chart(p,height=170)

with b:
    st.markdown('<div class="section-title">🎯 Task Selection</div>',unsafe_allow_html=True)
    t=filtered.Task.value_counts()
    st.bar_chart(t,height=170)

with c:
    st.markdown('<div class="section-title">🤖 AI Tool Adoption</div>',unsafe_allow_html=True)
    tool_counts={}
    for tool in ["ChatGPT","Gemini","Microsoft Copilot","Canva","Gamma","Power BI","Excel"]:
        tool_counts[tool]=int(filtered["AI Tool"].str.contains(tool,case=False,na=False).sum())
    st.bar_chart(pd.Series(tool_counts).sort_values(ascending=False),height=170)

# ---------- LOWER PANELS ----------
left,right=st.columns([1.65,1])

with left:
    st.markdown('<div class="section-title">👨‍🏫 Faculty Status</div>',unsafe_allow_html=True)
    fs=filtered.groupby("Faculty").agg(
        Students=("USN","count"),
        Submitted=("Status",lambda x:(x=="Submitted").sum()),
        Pending=("Status",lambda x:(x=="Pending").sum()),
        Revision=("Status",lambda x:(x=="Revision Required").sum())
    ).reset_index()
    fs["Submission %"]=(fs.Submitted/fs.Students*100).round(1)
    fs["Status"]=fs["Submission %"].apply(lambda x:"🟢" if x>=85 else ("🟡" if x>=70 else "🔴"))
    st.dataframe(
        fs[["Status","Faculty","Students","Submitted","Pending","Revision","Submission %"]]
        .sort_values("Submission %",ascending=False),
        use_container_width=True,height=205,hide_index=True)

with right:
    st.markdown('<div class="section-title">🚨 Action Required</div>',unsafe_allow_html=True)
    if pending:
        st.markdown(f'<div class="action action-red">🔴 <b>{pending}</b> students pending</div>',unsafe_allow_html=True)
    if revision:
        st.markdown(f'<div class="action action-yellow">🟡 <b>{revision}</b> revisions required</div>',unsafe_allow_html=True)
    low=int((fs["Submission %"]<70).sum())
    if low:
        st.markdown(f'<div class="action action-red">🔴 <b>{low}</b> faculty groups below 70%</div>',unsafe_allow_html=True)
    colour="green" if rate>=85 else "yellow"
    icon="🟢" if rate>=85 else "🟡"
    st.markdown(f'<div class="action action-{colour}">{icon} Overall submission: <b>{rate}%</b></div>',unsafe_allow_html=True)
    st.markdown(f'<div class="action action-green">📊 Average progress: <b>{avg}%</b></div>',unsafe_allow_html=True)

# ---------- SEARCH ----------
st.markdown("<div style='height:3px'></div>",unsafe_allow_html=True)
search=st.text_input("🔎 Search student / USN",placeholder="e.g. SYN-AIC26-001")

if search:
    r=filtered[
        filtered.USN.str.contains(search,case=False,na=False) |
        filtered.Student.str.contains(search,case=False,na=False)
    ]
    if len(r):
        x=r.iloc[0]
        q1,q2,q3,q4=st.columns(4)
        q1.metric("Student",x.Student)
        q2.metric("Section",x.Section)
        q3.metric("Task",x.Task)
        q4.metric("Progress",f"{x.Progress}%")
        st.info(f"**Problem:** {x.Problem}  |  **Faculty:** {x.Faculty}  |  **Status:** {x.Status}")
    else:
        st.warning("Student not found.")

st.markdown(
    '<div style="text-align:center;color:#94a3b8;font-size:11px;padding-top:2px;">'
    'AIC Portfolio Challenge • Coordinator Command Centre • Synthetic Data</div>',
    unsafe_allow_html=True)
