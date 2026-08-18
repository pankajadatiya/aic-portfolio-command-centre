import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ============================================================
# AIC PORTFOLIO CHALLENGE — 1,100 STUDENTS
# Clean management dashboard: charts BEFORE faculty buttons
# ============================================================

st.set_page_config(
    page_title="AIC Portfolio Challenge",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- DATA --------------------
@st.cache_data
def make_data():
    rng = np.random.default_rng(20260818)

    faculty = [
        "Geeta Maladkar", "Shobha K.B.", "Bhawna S.", "Rajesh A.",
        "B. Manjunath", "Vipanchi V.", "Dr. M. Maheswari", "Anup A",
        "Srividhya C.", "Arun", "Purushotham H.C.", "Pankaj Adatiya",
        "Additional Faculty"
    ]

    sections = [f"S{i:02d}" for i in range(1, 21)]
    section_faculty = {s: faculty[i % len(faculty)] for i, s in enumerate(sections)}

    tools = [
        "ChatGPT", "Gemini", "Microsoft Copilot", "Canva", "Gamma",
        "Power BI", "Excel", "ChatGPT + Canva", "ChatGPT + Power BI",
        "Gemini + Canva"
    ]

    domains = [
        "Retail", "Education", "Healthcare", "Banking", "Insurance",
        "Hospitality", "Logistics", "Manufacturing", "Marketing",
        "Sustainability"
    ]

    problems = [
        "Reducing Customer Waiting Time",
        "Improving Student Attendance Tracking",
        "Reducing Food Waste",
        "Improving Inventory Management",
        "Customer Complaint Resolution",
        "Personalized Learning Support",
        "Reducing Paper Usage",
        "Improving Customer Feedback Analysis",
        "Reducing Delivery Delays",
        "Streamlining Event Registration"
    ]

    rows = []

    for i in range(1, 1101):
        section = sections[(i - 1) % len(sections)]
        fac = section_faculty[section]

        p1 = rng.choice(["Submitted", "Pending", "In Progress", "Revision"],
                        p=[.74, .10, .10, .06])
        p2 = rng.choice(["Submitted", "Pending", "In Progress", "Revision"],
                        p=[.61, .15, .17, .07])
        p3 = rng.choice(["Submitted", "Pending", "In Progress", "Revision"],
                        p=[.48, .19, .25, .08])
        p4 = rng.choice(["Submitted", "Pending", "In Progress", "Revision"],
                        p=[.31, .23, .38, .08])
        p5 = rng.choice(["Completed", "Pending", "In Progress"],
                        p=[.08, .72, .20])

        submitted_count = sum(x == "Submitted" for x in [p1, p2, p3, p4])
        completed_count = submitted_count + (p5 == "Completed")
        progress = round(completed_count / 5 * 100)

        if p5 == "Completed":
            current_phase = "Phase 5 – Defend"
        elif p4 == "Submitted":
            current_phase = "Phase 4 – Decide"
        elif p3 == "Submitted":
            current_phase = "Phase 3 – Build"
        elif p2 == "Submitted":
            current_phase = "Phase 2 – Design"
        else:
            current_phase = "Phase 1 – Discover"

        approval = (
            rng.choice(["Approved", "Pending Review", "Revision Required"],
                       p=[.72, .18, .10])
            if p1 == "Submitted"
            else "Pending Review"
        )

        rows.append({
            "Portfolio ID": f"AIC26-{i:04d}",
            "Student Name": f"Student {i:04d}",
            "USN": f"AIC26-{i:04d}",
            "Email": f"student{i:04d}@aic-demo.edu",
            "Section": section,
            "Faculty Assigned": fac,
            "Team ID": f"TEAM-{((i-1)//4)+1:04d}",
            "Domain": rng.choice(domains),
            "Current Phase": current_phase,
            "Overall Progress": progress,
            "P1 Status": p1,
            "P2 Status": p2,
            "P3 Status": p3,
            "P4 Status": p4,
            "P5 Status": p5,
            "P1 Faculty Approval": approval,
            "P1 Faculty Remarks": (
                "Problem statement approved by faculty."
                if approval == "Approved"
                else "Awaiting faculty review / revision."
            ),
            "P1 Problem Statement": rng.choice(problems),
            "P1 AI Opportunity": "AI can support analysis, prediction and decision-making.",
            "P2 Selected AI Tool": rng.choice(tools),
            "P2 Proposed Solution": "AI-enabled solution designed around the identified problem.",
            "P3 Platform": rng.choice(["Power BI", "Excel", "Streamlit", "Canva", "Python", "Google Workspace"]),
            "P3 Prototype Link": "https://example.com/prototype" if p3 == "Submitted" else "",
            "P4 Recommendation": "Use the proposed AI solution to improve the identified process.",
            "P4 Final Artefact": "https://example.com/final" if p4 == "Submitted" else "",
            "P5 Viva Status": "Completed" if p5 == "Completed" else "Pending",
            "P1 Attachment": "Submitted File" if p1 == "Submitted" and rng.random() < .78 else "",
            "P2 Attachment": "Submitted File" if p2 == "Submitted" and rng.random() < .78 else "",
            "P3 Attachment": "Submitted File" if p3 == "Submitted" and rng.random() < .78 else "",
            "P4 Attachment": "Submitted File" if p4 == "Submitted" and rng.random() < .78 else "",
            "P5 Attachment": "Submitted File" if p5 == "Completed" and rng.random() < .78 else "",
        })

    return pd.DataFrame(rows)

df = make_data()
TOTAL = len(df)

# -------------------- STYLE --------------------
st.markdown("""
<style>
#MainMenu, footer, header {visibility:hidden;}
.block-container{padding:.45rem .75rem .7rem;max-width:100%;}
.hero{
 background:linear-gradient(110deg,#172554,#2563eb,#7c3aed);
 color:white;border-radius:18px;padding:14px 20px;margin-bottom:6px;
}
.hero h1{font-size:28px;margin:0;font-weight:900;}
.hero p{font-size:11px;margin:4px 0 0;}
.live{float:right;background:rgba(255,255,255,.16);padding:5px 9px;border-radius:20px;font-size:9px;font-weight:900;}
.section{font-size:16px;font-weight:900;color:#172554;margin:7px 0 4px;}
.kpi{border:1px solid #dbe3ee;border-radius:12px;padding:7px 10px;height:67px;}
.kpi-label{font-size:9px;font-weight:900;color:#475569;}
.kpi-value{font-size:24px;font-weight:900;color:#0f172a;margin-top:4px;}
.phase{border-radius:13px;padding:8px 10px;height:91px;border:1px solid #dbe3ee;}
.p1{background:#eff6ff}.p2{background:#f5f3ff}.p3{background:#ecfdf5}
.p4{background:#fffbeb}.p5{background:#fff1f2}
.pcode{font-size:9px;font-weight:900;color:#64748b}
.pname{font-size:13px;font-weight:900;color:#172554}
.pct{font-size:22px;font-weight:900}
.small{font-size:9px;color:#64748b}
.tool{background:#eef2ff;border:1px solid #c7d2fe;border-radius:8px;padding:5px 8px;font-size:10px;font-weight:800;color:#3730a3}
.stButton>button{border-radius:9px!important;font-size:10px!important;font-weight:800!important;min-height:45px!important;}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown("""
<div class="hero">
 <span class="live">● LIVE TRACKING</span>
 <h1>🎯 AIC Portfolio Challenge</h1>
 <p>Portfolio Progress Dashboard • Faculty-wise Monitoring • Phase-wise Student Progress</p>
</div>
""", unsafe_allow_html=True)

# -------------------- KPI ROW --------------------
avg_progress = df["Overall Progress"].mean()
kpi_data = [
    ("👥", "STUDENTS", f"{TOTAL:,}"),
    ("👨‍🏫", "FACULTY", df["Faculty Assigned"].nunique()),
    ("🏫", "SECTIONS", df["Section"].nunique()),
    ("🔵", "P1 DISCOVER", int((df["P1 Status"]=="Submitted").sum())),
    ("🟣", "P2 DESIGN", int((df["P2 Status"]=="Submitted").sum())),
    ("📈", "AVG PROGRESS", f"{avg_progress:.1f}%")
]
cols = st.columns(6)
for c,(icon,label,value) in zip(cols,kpi_data):
    c.markdown(
        f'<div class="kpi"><div class="kpi-label">{icon} {label}</div>'
        f'<div class="kpi-value">{value}</div></div>',
        unsafe_allow_html=True
    )

# -------------------- PHASE CARDS --------------------
st.markdown('<div class="section">🚀 Portfolio Journey — Phase-wise Progress</div>', unsafe_allow_html=True)

phase_info = [
    ("P1","DISCOVER","P1 Status","p1","Submitted"),
    ("P2","DESIGN","P2 Status","p2","Submitted"),
    ("P3","BUILD","P3 Status","p3","Submitted"),
    ("P4","DECIDE","P4 Status","p4","Submitted"),
    ("P5","DEFEND","P5 Status","p5","Completed")
]

cols = st.columns(5)
for c,(code,name,field,css,good) in zip(cols,phase_info):
    n = int((df[field]==good).sum())
    pct = n/TOTAL*100
    c.markdown(
        f'<div class="phase {css}"><div class="pcode">{code}</div>'
        f'<div class="pname">{name}</div><div class="pct">{pct:.1f}%</div>'
        f'<b>{n:,} {"Completed" if code=="P5" else "Submitted"}</b>'
        f'<div class="small">of {TOTAL:,} students</div></div>',
        unsafe_allow_html=True
    )

# ============================================================
# REAL CHARTS — INTENTIONALLY BEFORE FACULTY BUTTONS
# ============================================================
st.markdown('<div class="section">📊 Phase-wise Analytics</div>', unsafe_allow_html=True)

phases = ["Discover","Design","Build","Decide","Defend"]

submitted = [
    (df["P1 Status"]=="Submitted").sum(),
    (df["P2 Status"]=="Submitted").sum(),
    (df["P3 Status"]=="Submitted").sum(),
    (df["P4 Status"]=="Submitted").sum(),
    (df["P5 Status"]=="Completed").sum()
]
pending = [
    (df["P1 Status"]=="Pending").sum(),
    (df["P2 Status"]=="Pending").sum(),
    (df["P3 Status"]=="Pending").sum(),
    (df["P4 Status"]=="Pending").sum(),
    (df["P5 Status"]=="Pending").sum()
]
inprog = [
    (df["P1 Status"]=="In Progress").sum(),
    (df["P2 Status"]=="In Progress").sum(),
    (df["P3 Status"]=="In Progress").sum(),
    (df["P4 Status"]=="In Progress").sum(),
    (df["P5 Status"]=="In Progress").sum()
]
revision = [
    (df["P1 Status"]=="Revision").sum(),
    (df["P2 Status"]=="Revision").sum(),
    (df["P3 Status"]=="Revision").sum(),
    (df["P4 Status"]=="Revision").sum(),
    0
]

# Chart 1: stacked phase status
fig = go.Figure()
for name,vals in [
    ("Submitted",submitted),
    ("In Progress",inprog),
    ("Pending",pending),
    ("Revision",revision)
]:
    fig.add_trace(go.Bar(
        name=name,x=phases,y=vals,
        text=vals,textposition="inside",
        hovertemplate=f"%{{x}}<br>{name}: %{{y}}<extra></extra>"
    ))

fig.update_layout(
    title="Student Status Across All Portfolio Phases",
    barmode="stack",
    height=330,
    margin=dict(l=25,r=20,t=55,b=35),
    xaxis_title="Phase",
    yaxis_title="Students",
    legend=dict(orientation="h",y=1.12),
    plot_bgcolor="white",
    paper_bgcolor="white"
)
st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

# Charts 2 + 3
left,right = st.columns(2)

completion = [round(x/TOTAL*100,1) for x in submitted]
fig2 = go.Figure(go.Bar(
    x=phases,y=completion,
    text=[f"{x}%" for x in completion],
    textposition="outside"
))
fig2.update_layout(
    title="Phase Completion Rate",
    height=290,
    margin=dict(l=25,r=20,t=55,b=35),
    yaxis=dict(title="Completion %",range=[0,100]),
    xaxis_title="",
    plot_bgcolor="white",paper_bgcolor="white"
)
with left:
    st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})

tools = df["P2 Selected AI Tool"].value_counts().sort_values()
fig3 = go.Figure(go.Bar(
    x=tools.values,y=tools.index,orientation="h",
    text=tools.values,textposition="outside"
))
fig3.update_layout(
    title="🤖 AI Tools Selected by Students",
    height=290,
    margin=dict(l=125,r=25,t=55,b=30),
    xaxis_title="Students",
    plot_bgcolor="white",paper_bgcolor="white"
)
with right:
    st.plotly_chart(fig3,use_container_width=True,config={"displayModeBar":False})

# Faculty chart
faculty_progress = df.groupby("Faculty Assigned")["Overall Progress"].mean().sort_values()
fig4 = go.Figure(go.Bar(
    x=faculty_progress.values,
    y=faculty_progress.index,
    orientation="h",
    text=[f"{x:.0f}%" for x in faculty_progress.values],
    textposition="outside"
))
fig4.update_layout(
    title="👨‍🏫 Faculty-wise Average Portfolio Progress",
    height=390,
    margin=dict(l=135,r=30,t=55,b=30),
    xaxis=dict(title="Average Progress %",range=[0,100]),
    plot_bgcolor="white",paper_bgcolor="white"
)
st.plotly_chart(fig4,use_container_width=True,config={"displayModeBar":False})

# -------------------- FACULTY BUTTONS --------------------
st.markdown('<div class="section">👨‍🏫 Faculty Progress — Click a Faculty Name</div>', unsafe_allow_html=True)

if "selected_faculty" not in st.session_state:
    st.session_state.selected_faculty = None

names = sorted(df["Faculty Assigned"].unique())
for start in range(0,len(names),4):
    cols=st.columns(4)
    for j,fac in enumerate(names[start:start+4]):
        fdf=df[df["Faculty Assigned"]==fac]
        prog=fdf["Overall Progress"].mean()
        with cols[j]:
            if st.button(
                f"👨‍🏫 {fac}\n{len(fdf)} Students • {prog:.0f}% Progress",
                key=f"fac_{start}_{j}",
                use_container_width=True
            ):
                st.session_state.selected_faculty=fac

# -------------------- FACULTY DETAIL --------------------
if st.session_state.selected_faculty:
    fac=st.session_state.selected_faculty
    fdf=df[df["Faculty Assigned"]==fac].copy()

    st.markdown(f'<div class="section">📋 {fac} — Faculty Overview</div>',unsafe_allow_html=True)

    c1,c2,c3,c4=st.columns(4)
    c1.metric("Students",len(fdf))
    c2.metric("Avg Progress",f'{fdf["Overall Progress"].mean():.1f}%')
    c3.metric("P1 Approved",int((fdf["P1 Faculty Approval"]=="Approved").sum()))
    c4.metric("P1 Revision",int((fdf["P1 Faculty Approval"]=="Revision Required").sum()))

    st.markdown('<div class="section">📈 Faculty Phase Progress</div>',unsafe_allow_html=True)

    fac_completion=[
        (fdf["P1 Status"]=="Submitted").mean()*100,
        (fdf["P2 Status"]=="Submitted").mean()*100,
        (fdf["P3 Status"]=="Submitted").mean()*100,
        (fdf["P4 Status"]=="Submitted").mean()*100,
        (fdf["P5 Status"]=="Completed").mean()*100
    ]
    figf=go.Figure(go.Bar(
        x=phases,y=fac_completion,
        text=[f"{x:.0f}%" for x in fac_completion],
        textposition="outside"
    ))
    figf.update_layout(
        height=270,
        title=f"{fac} — Phase Completion",
        yaxis=dict(range=[0,100],title="Completion %"),
        plot_bgcolor="white",paper_bgcolor="white"
    )
    st.plotly_chart(figf,use_container_width=True,config={"displayModeBar":False})

    st.markdown('<div class="section">🔎 Search Student</div>',unsafe_allow_html=True)
    q=st.text_input("Student Name / USN",placeholder="Type name or USN...",key=f"q_{fac}")
    choices=["Select Student"]+sorted(fdf["Student Name"].tolist())
    choice=st.selectbox("Choose Student",choices,key=f"s_{fac}")

    student=None
    if q.strip():
        ql=q.lower().strip()
        m=fdf[
            fdf["Student Name"].str.lower().str.contains(ql,na=False) |
            fdf["USN"].str.lower().str.contains(ql,na=False)
        ]
        if len(m):
            student=m.iloc[0] if len(m)==1 else m.iloc[0]
    elif choice!="Select Student":
        student=fdf[fdf["Student Name"]==choice].iloc[0]

    if student is not None:
        st.markdown(f'<div class="section">🧑‍🎓 {student["Student Name"]}</div>',unsafe_allow_html=True)

        a,b,c,d=st.columns(4)
        a.metric("USN",student["USN"])
        b.metric("Section",student["Section"])
        c.metric("Progress",f'{student["Overall Progress"]}%')
        d.metric("Current Phase",student["Current Phase"])

        st.markdown(
            f'<div class="tool">🤖 AI TOOL CHOSEN: {student["P2 Selected AI Tool"]}</div>',
            unsafe_allow_html=True
        )

        approval=student["P1 Faculty Approval"]
        st.info(
            f"Problem Statement — Faculty Approval: {approval} | "
            f"{student['P1 Faculty Remarks']}"
        )

        st.dataframe(pd.DataFrame({
            "Phase": ["Discover","Design","Build","Decide","Defend"],
            "Status": [
                student["P1 Status"],student["P2 Status"],student["P3 Status"],
                student["P4 Status"],student["P5 Status"]
            ],
            "Attachment": [
                student["P1 Attachment"] or "No Attachment",
                student["P2 Attachment"] or "No Attachment",
                student["P3 Attachment"] or "No Attachment",
                student["P4 Attachment"] or "No Attachment",
                student["P5 Attachment"] or "No Attachment"
            ]
        }),use_container_width=True,hide_index=True)

        st.markdown(f"""
**Problem Statement:** {student["P1 Problem Statement"]}  
**AI Opportunity:** {student["P1 AI Opportunity"]}  
**Proposed Solution:** {student["P2 Proposed Solution"]}  
**Build Platform:** {student["P3 Platform"]}  
**Recommendation:** {student["P4 Recommendation"]}
""")

st.markdown(
    '<div class="small" style="text-align:center;margin-top:6px;">'
    'AIC Portfolio Challenge • 1,100 Synthetic Students • No Marks Displayed'
    '</div>',
    unsafe_allow_html=True
)
