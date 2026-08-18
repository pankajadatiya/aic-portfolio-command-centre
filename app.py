import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="AIC Portfolio Challenge", page_icon="🎯", layout="wide")

@st.cache_data
def make_data():
    np.random.seed(20260818)
    faculty_sections = {
        "Geeta Maladkar":["D","L","O"], "Shobha K.B.":["A","B"],
        "Bhawna S.":["J","K"], "Rajesh A.":["Q","R2"],
        "B. Manjunath":["M","S"], "Vipanchi V.":["T","P"],
        "Dr. M. Maheswari":["C"], "Anup A":["G"], "Srividhya C.":["I"],
        "Arun":["E"], "Purushotham H.C.":["R"], "Pankaj Adatiya":["N"],
        "Additional Faculty (Synthetic)":["SYN"]
    }
    sf={s:f for f,ss in faculty_sections.items() for s in ss}
    problems=[
        "Reducing Food Waste in College Cafeterias","Improving Student Attendance Tracking",
        "Reducing Queue Time at Campus Cafeteria","Improving Retail Inventory Management",
        "Customer Complaint Resolution","Personalized Learning Support",
        "Reducing Paper Usage in Administration","Improving Small Business Social Media",
        "Optimizing Library Book Availability","Reducing Delivery Delays"
    ]
    tools=["ChatGPT","Gemini","Microsoft Copilot","Canva","Gamma","Power BI","Excel"]
    rows=[]
    for i in range(1,1001):
        sec=np.random.choice(list(sf)); fac=sf[sec]
        p1=np.random.choice(["Submitted","Pending","Revision"],p=[.82,.12,.06])
        p2=np.random.choice(["Submitted","Pending","Revision","Not Started"],p=[.68,.18,.08,.06])
        p3=np.random.choice(["Submitted","Pending","Revision","Not Started"],p=[.54,.22,.10,.14])
        p4=np.random.choice(["Submitted","Pending","Revision","Not Started"],p=[.36,.25,.08,.31])
        p5=np.random.choice(["Completed","Pending"],p=[.08,.92])
        done=sum(x=="Submitted" for x in [p1,p2,p3,p4])+(p5=="Completed")
        rows.append({
            "Student Name":f"Synthetic Student {i:04d}","USN":f"SYN-AIC26-{i:04d}",
            "Faculty":fac,"Section":sec,"Problem":np.random.choice(problems),
            "AI Tool":np.random.choice(tools),"Overall Progress":round(done/5*100),
            "P1":p1,"P2":p2,"P3":p3,"P4":p4,"P5":p5,
            "P1 Attachment":"Submitted – synthetic evidence" if p1=="Submitted" and np.random.rand()<.72 else "",
            "P2 Attachment":"Submitted – synthetic evidence" if p2=="Submitted" and np.random.rand()<.72 else "",
            "P3 Attachment":"Submitted – synthetic evidence" if p3=="Submitted" and np.random.rand()<.72 else "",
            "P4 Attachment":"Submitted – synthetic evidence" if p4=="Submitted" and np.random.rand()<.72 else "",
            "P5 Attachment":"Submitted – synthetic evidence" if p5=="Completed" and np.random.rand()<.72 else "",
            "Problem Description":"Synthetic problem statement for dashboard demonstration.",
            "Who is Affected":np.random.choice(["Students","Faculty and students","Customers","College administration"]),
            "How AI Can Help":np.random.choice(["Analyse patterns and generate recommendations.","Automate repetitive documentation and communication.","Summarise feedback and identify recurring issues.","Predict demand and support better decisions."])
        })
    return pd.DataFrame(rows)

df=make_data()

st.markdown("""
<style>
#MainMenu,footer,header{visibility:hidden}
.block-container{padding:.6rem .9rem .4rem}
.hero{background:linear-gradient(135deg,#172554,#2563eb,#7c3aed);border-radius:18px;padding:17px 22px;color:white;box-shadow:0 7px 22px #dbeafe}
.hero-title{font-size:30px;font-weight:900}.hero-sub{font-size:13px;margin-top:4px;opacity:.9}
.active{float:right;background:#ffffff22;padding:6px 11px;border-radius:20px;font-size:11px;font-weight:800}
.kpi{border-radius:13px;padding:9px 11px;height:76px;border:1px solid #dbe3ee;box-shadow:0 3px 12px #e2e8f055}
.kpi-label{font-size:10px;font-weight:850;color:#475569}.kpi-value{font-size:27px;font-weight:900;margin-top:4px}
.k1{background:linear-gradient(135deg,#dbeafe,#f8fbff)}.k2{background:linear-gradient(135deg,#ede9fe,#faf9ff)}
.k3{background:linear-gradient(135deg,#dcfce7,#f8fff9)}.k4{background:linear-gradient(135deg,#fef3c7,#fffdf5)}
.k5{background:linear-gradient(135deg,#fee2e2,#fffafa)}.k6{background:linear-gradient(135deg,#cffafe,#f7ffff)}
.section{font-size:16px;font-weight:900;color:#172554;margin:9px 0 5px}
.phase{border-radius:14px;padding:10px;min-height:100px;border:1px solid #dbe3ee;box-shadow:0 3px 12px #e2e8f055}
.p1{background:linear-gradient(135deg,#dbeafe,#eff6ff)}.p2{background:linear-gradient(135deg,#ede9fe,#f5f3ff)}
.p3{background:linear-gradient(135deg,#ccfbf1,#f0fdfa)}.p4{background:linear-gradient(135deg,#fef3c7,#fffbeb)}
.p5{background:linear-gradient(135deg,#fce7f3,#fff1f2)}
.pno{font-size:10px;font-weight:900;color:#475569}.pname{font-size:14px;font-weight:900}.big{font-size:22px;font-weight:900}
.stButton>button{min-height:48px!important;border-radius:11px!important;font-size:11px!important;font-weight:800!important;white-space:pre-line!important;border:1px solid #dbe3ee!important;background:white!important}
.stButton>button:hover{border-color:#2563eb!important;background:#eff6ff!important;color:#1d4ed8!important}
.detail{border:1px solid #dbe3ee;border-radius:14px;padding:13px;background:linear-gradient(135deg,#fff,#f8fbff)}
.status{padding:7px 9px;border-radius:9px;margin:3px 0;font-size:11px;font-weight:800}
.green{background:#dcfce7;color:#166534}.amber{background:#fef3c7;color:#92400e}.red{background:#fee2e2;color:#991b1b}.grey{background:#f1f5f9;color:#475569}
</style>
""",unsafe_allow_html=True)

st.markdown('<div class="hero"><span class="active">● LIVE TRACKING</span><div class="hero-title">🎯 AIC Portfolio Challenge</div><div class="hero-sub">Portfolio Progress Dashboard • Faculty-wise Monitoring • Phase-wise Student Progress</div></div>',unsafe_allow_html=True)

total=len(df)
kpis=[
("👥","STUDENTS",f"{total:,}","k1"),
("👨‍🏫","FACULTY",df.Faculty.nunique(),"k2"),
("🏫","SECTIONS",df.Section.nunique(),"k3"),
("🔵","P1 DISCOVER",int((df.P1=="Submitted").sum()),"k4"),
("🟣","P2 DESIGN",int((df.P2=="Submitted").sum()),"k5"),
("📈","AVG PROGRESS",f'{df["Overall Progress"].mean():.1f}%',"k6")]
cols=st.columns(6)
for c,(ic,l,v,cl) in zip(cols,kpis):
    c.markdown(f'<div class="kpi {cl}"><div class="kpi-label">{ic} {l}</div><div class="kpi-value">{v}</div></div>',unsafe_allow_html=True)

st.markdown('<div class="section">🚀 Portfolio Journey — Phase-wise Progress</div>',unsafe_allow_html=True)
phase_defs=[("P1","DISCOVER","P1","p1"),("P2","DESIGN","P2","p2"),("P3","BUILD","P3","p3"),("P4","DECIDE","P4","p4"),("P5","DEFEND","P5","p5")]
cols=st.columns(5)
for c,(code,name,field,cl) in zip(cols,phase_defs):
    done=int((df[field]=="Completed").sum()) if field=="P5" else int((df[field]=="Submitted").sum())
    pct=done/total*100
    label="Completed" if field=="P5" else "Submitted"
    c.markdown(f'<div class="phase {cl}"><div class="pno">{code}</div><div class="pname">{name}</div><div class="big">{pct:.1f}%</div><div style="font-size:11px;font-weight:750">{done:,} {label}</div><div style="font-size:10px;color:#64748b">of {total:,} students</div></div>',unsafe_allow_html=True)

st.markdown('<div class="section">👨‍🏫 Faculty Progress — Click a Faculty Name</div>',unsafe_allow_html=True)
if "selected_faculty" not in st.session_state: st.session_state.selected_faculty=None

faculty_names=sorted(df.Faculty.unique())
for start in range(0,len(faculty_names),4):
    cols=st.columns(4)
    for j,fac in enumerate(faculty_names[start:start+4]):
        f=df[df.Faculty==fac]
        prog=f["Overall Progress"].mean()
        with cols[j]:
            if st.button(f"👨‍🏫 {fac}\n{len(f)} Students • {prog:.0f}% Progress",key=f"fac_{start}_{j}",use_container_width=True):
                st.session_state.selected_faculty=fac

if st.session_state.selected_faculty:
    fac=st.session_state.selected_faculty
    fdf=df[df.Faculty==fac].copy()
    st.markdown(f'<div class="section">📋 {fac} — Faculty Overview</div>',unsafe_allow_html=True)
    cols=st.columns(5)
    for c,(code,name,field) in zip(cols,phase_defs):
        done=int((fdf[field]=="Completed").sum()) if field=="P5" else int((fdf[field]=="Submitted").sum())
        pct=done/len(fdf)*100
        c.markdown(f'<div class="phase {code.lower() if code.lower() in ["p1","p2","p3","p4","p5"] else ""}" style="min-height:80px"><div class="pno">{code}</div><div class="pname">{name}</div><div class="big">{pct:.0f}%</div><div style="font-size:10px;font-weight:750">{done} {"Completed" if field=="P5" else "Submitted"}</div></div>',unsafe_allow_html=True)

    st.markdown('<div class="section">🔎 Find a Student</div>',unsafe_allow_html=True)
    c1,c2=st.columns([1.1,1])
    query=c1.text_input("Student Name / USN",placeholder="Type student name or USN...",key=f"q_{fac}")
    choice=c2.selectbox("Choose Student",["Select Student"]+sorted(fdf["Student Name"].tolist()),key=f"s_{fac}")
    student=None
    if query.strip():
        q=query.lower().strip()
        m=fdf[fdf["Student Name"].str.lower().str.contains(q,na=False)|fdf["USN"].str.lower().str.contains(q,na=False)]
        if len(m)==1: student=m.iloc[0]
        elif len(m)>1:
            nm=st.selectbox("Matching Students",m["Student Name"].tolist(),key=f"m_{fac}")
            student=m[m["Student Name"]==nm].iloc[0]
        else: st.warning("No student found under this faculty.")
    elif choice!="Select Student":
        student=fdf[fdf["Student Name"]==choice].iloc[0]

    if student is not None:
        st.markdown(f'<div class="section">🧑‍🎓 {student["Student Name"]} — Portfolio Progress</div>',unsafe_allow_html=True)
        a,b,c,d=st.columns(4)
        a.metric("USN",student.USN); b.metric("Section",student.Section); c.metric("Progress",f'{student["Overall Progress"]}%'); d.metric("Faculty",student.Faculty)
        st.markdown('<div class="detail">',unsafe_allow_html=True)
        for label,field,att in [
            ("Phase 1 – Discover","P1","P1 Attachment"),("Phase 2 – Design","P2","P2 Attachment"),
            ("Phase 3 – Build","P3","P3 Attachment"),("Phase 4 – Decide","P4","P4 Attachment"),
            ("Phase 5 – Defend","P5","P5 Attachment")]:
            status=student[field]
            cls="green" if status in ["Submitted","Completed"] else ("red" if status=="Revision" else ("amber" if status=="Pending" else "grey"))
            icon="🟢" if cls=="green" else ("🔴" if cls=="red" else ("🟡" if cls=="amber" else "⚪"))
            attachment=str(student[att]).strip() or "No Attachment"
            st.markdown(f'<div class="status {cls}">{icon} <b>{label}</b> — {status}<span style="float:right">📎 {attachment}</span></div>',unsafe_allow_html=True)
        st.markdown(f'<br><b>Problem Identified:</b> {student.Problem}<br><b>Who is affected:</b> {student["Who is Affected"]}<br><b>How AI can help:</b> {student["How AI Can Help"]}',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)
    else:
        st.info("Select or search a student to see the complete phase-wise progress.")
else:
    st.info("👆 Click a Faculty Name above to open faculty-wise phase tracking.")

st.markdown('<div style="text-align:center;color:#94a3b8;font-size:9px;margin-top:6px">AIC Portfolio Challenge • Phase-wise Progress Dashboard • Synthetic Demo • No marks displayed</div>',unsafe_allow_html=True)
