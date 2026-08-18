import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="AIC Portfolio Challenge", page_icon="🎯", layout="wide")

@st.cache_data
def make_data():
    rng=np.random.default_rng(20260818)

    faculty_sections = {
        'B. Manjunath': ['M', 'S'],
        'Pankaj Adatiya': ['N'],
        'Purushotham H.C.': ['R'],
        'Rajesh A.': ['Q', 'R2'],
        'Bhawna S.': ['J', 'K'],
        'Shobha K.B.': ['A', 'B'],
        'Srividhya C.': ['I'],
        'Dr. M. Maheswari': ['C'],
        'Geeta Maladkar': ['D', 'L', 'O'],
        'Vipanchi V.': ['T', 'P'],
        'Anup A': ['G'],
        'Arun': ['E'],
        'Geeta M.': [],
        'Faculty 14 – To Confirm': []
    }

    section_to_faculty = {s:f for f,sections in faculty_sections.items() for s in sections}
    real_sections=list(section_to_faculty.keys())

    section_sizes={'M': 45, 'S': 25, 'N': 18, 'R': 45, 'Q': 36, 'J': 43, 'K': 67, 'R2': 43, 'A': 60, 'B': 60, 'I': 51, 'C': 58, 'D': 70, 'L': 69, 'O': 16, 'T': 32, 'P': 32, 'G': 58, 'E': 46}
    weights=np.array([section_sizes.get(s,1) for s in real_sections],dtype=float)
    weights=weights/weights.sum()

    tools=["ChatGPT","Gemini","Microsoft Copilot","Canva","Gamma","Power BI","Excel",
           "ChatGPT + Canva","ChatGPT + Power BI","Gemini + Canva"]
    problems=["Reducing Customer Waiting Time","Improving Student Attendance Tracking",
              "Reducing Food Waste","Improving Inventory Management","Customer Complaint Resolution",
              "Personalized Learning Support","Reducing Paper Usage","Improving Customer Feedback Analysis",
              "Reducing Delivery Delays","Streamlining Event Registration"]
    domains=["Retail","Education","Healthcare","Banking","Insurance","Hospitality","Logistics",
             "Manufacturing","Marketing","Sustainability"]

    rows=[]
    for i in range(1,1101):
        section=rng.choice(real_sections,p=weights)
        faculty=section_to_faculty[section]

        p1=rng.choice(["Submitted","Pending","In Progress","Revision"],p=[.75,.08,.11,.06])
        p2=rng.choice(["Submitted","Pending","In Progress","Revision"],p=[.62,.14,.17,.07])
        p3=rng.choice(["Submitted","Pending","In Progress","Revision"],p=[.49,.18,.24,.09])
        p4=rng.choice(["Submitted","Pending","In Progress","Revision"],p=[.33,.22,.37,.08])
        p5=rng.choice(["Completed","Pending","In Progress"],p=[.08,.72,.20])

        done=sum(x=="Submitted" for x in [p1,p2,p3,p4])+int(p5=="Completed")
        progress=round(done/5*100)

        approval=(rng.choice(["Approved","Pending Review","Revision Required"],p=[.72,.18,.10])
                  if p1=="Submitted" else "Pending Review")

        rows.append({
            "Portfolio ID":f"AIC26-{i:04d}",
            "Student Name":f"Student {i:04d}",
            "USN":f"AIC26-{i:04d}",
            "Email":f"student{i:04d}@aic-demo.edu",
            "Section":section,
            "Faculty Assigned":faculty,
            "Domain":rng.choice(domains),
            "Current Phase":("Phase 5 – Defend" if p5=="Completed" else
                             "Phase 4 – Decide" if p4=="Submitted" else
                             "Phase 3 – Build" if p3=="Submitted" else
                             "Phase 2 – Design" if p2=="Submitted" else
                             "Phase 1 – Discover"),
            "Overall Progress":progress,
            "P1 Status":p1,"P2 Status":p2,"P3 Status":p3,"P4 Status":p4,"P5 Status":p5,
            "P1 Faculty Approval":approval,
            "P1 Faculty Remarks":("Problem statement approved by faculty."
                                  if approval=="Approved" else "Awaiting faculty review / revision."),
            "Problem Statement":rng.choice(problems),
            "AI Tool":rng.choice(tools),
            "P1 AI Opportunity":"AI can support analysis, prediction and decision-making.",
            "P2 Proposed Solution":"AI-enabled solution designed around the identified problem.",
            "P3 Platform":rng.choice(["Power BI","Excel","Streamlit","Canva","Python","Google Workspace"]),
            "P4 Recommendation":"Use the proposed AI solution to improve the identified process.",
            "P1 Attachment":"Submitted File" if p1=="Submitted" and rng.random()<.78 else "",
            "P2 Attachment":"Submitted File" if p2=="Submitted" and rng.random()<.78 else "",
            "P3 Attachment":"Submitted File" if p3=="Submitted" and rng.random()<.78 else "",
            "P4 Attachment":"Submitted File" if p4=="Submitted" and rng.random()<.78 else "",
            "P5 Attachment":"Submitted File" if p5=="Completed" and rng.random()<.78 else ""
        })
    return pd.DataFrame(rows)

df=make_data()
TOTAL=len(df)
PLANNED_FACULTY=14
PLANNED_SECTIONS=21

st.markdown("""
<style>
#MainMenu,footer,header{visibility:hidden}
.block-container{padding:.55rem .8rem 1rem;max-width:100%}
.hero{background:linear-gradient(100deg,#111827,#0037FF,#FF1493);color:white;border-radius:18px;padding:15px 20px;margin-bottom:8px}
.hero-title{font-size:30px;font-weight:900}.hero-sub{font-size:12px;margin-top:5px}.live{float:right;background:#ffffff2a;border-radius:20px;padding:6px 10px;font-size:9px;font-weight:900}
.section{font-size:17px;font-weight:900;color:#111827;margin:12px 0 6px}
.kpi{border-radius:13px;padding:8px 10px;height:72px;box-sizing:border-box;border:2px solid}
.k1{background:#DBEAFE;border-color:#2563EB}.k2{background:#FCE7F3;border-color:#EC4899}.k3{background:#DCFCE7;border-color:#16A34A}
.k4{background:#FFEDD5;border-color:#F97316}.k5{background:#FEE2E2;border-color:#EF4444}.k6{background:#EDE9FE;border-color:#7C3AED}
.kpi-label{font-size:9px;font-weight:900;color:#111827}.kpi-value{font-size:25px;font-weight:900;color:#111827;margin-top:5px}
.phase{height:112px;box-sizing:border-box;border-radius:14px;padding:10px 11px;border:2px solid;overflow:hidden}
.p1{background:#DBEAFE;border-color:#0057FF}.p2{background:#F3E8FF;border-color:#8E24AA}.p3{background:#D1FAE5;border-color:#00C853}.p4{background:#FFEDD5;border-color:#FF6D00}.p5{background:#FCE7F3;border-color:#FF1493}
.pcode{font-size:9px;font-weight:900}.pname{font-size:14px;font-weight:900;margin-top:5px}.pct{font-size:25px;font-weight:900;margin-top:7px}.psub{font-size:10px;font-weight:750;margin-top:3px}
.note{font-size:10px;color:#4B5563}
.stButton>button{min-height:52px!important;border-radius:10px!important;font-size:10px!important;font-weight:850!important;white-space:pre-line!important;border:2px solid #E5E7EB!important;background:white!important}
.stButton>button:hover{background:#EFF6FF!important;border-color:#2563EB!important}
.detail{border:2px solid #E5E7EB;border-radius:13px;padding:12px;background:white}
.pill{display:inline-block;padding:4px 8px;border-radius:999px;font-size:9px;font-weight:900}.green{background:#DCFCE7;color:#166534}.orange{background:#FFEDD5;color:#C2410C}.red{background:#FEE2E2;color:#B91C1C}
</style>
""",unsafe_allow_html=True)

st.markdown('<div class="hero"><span class="live">● LIVE TRACKING</span><div class="hero-title">🎯 AIC Portfolio Challenge</div><div class="hero-sub">Phase-wise Portfolio Progress • Faculty Monitoring • Student Submission Review</div></div>',unsafe_allow_html=True)

avg=df["Overall Progress"].mean()
kpis=[("👥","STUDENTS",f"{TOTAL:,}","k1"),("👨‍🏫","FACULTY",PLANNED_FACULTY,"k2"),("🏫","SECTIONS",PLANNED_SECTIONS,"k3"),
      ("🔵","P1 DISCOVER",int((df["P1 Status"]=="Submitted").sum()),"k4"),("🟣","P2 DESIGN",int((df["P2 Status"]=="Submitted").sum()),"k5"),
      ("📈","AVG PROGRESS",f"{avg:.1f}%","k6")]
cols=st.columns(6)
for c,(ic,lbl,val,cl) in zip(cols,kpis):
    c.markdown(f'<div class="kpi {cl}"><div class="kpi-label">{ic} {lbl}</div><div class="kpi-value">{val}</div></div>',unsafe_allow_html=True)

st.markdown('<div class="section">🚀 Portfolio Journey</div>',unsafe_allow_html=True)
phase_defs=[("P1","DISCOVER","P1 Status","p1","Submitted"),("P2","DESIGN","P2 Status","p2","Submitted"),
            ("P3","BUILD","P3 Status","p3","Submitted"),("P4","DECIDE","P4 Status","p4","Submitted"),
            ("P5","DEFEND","P5 Status","p5","Completed")]
cols=st.columns(5)
for c,(code,name,field,cl,good) in zip(cols,phase_defs):
    n=int((df[field]==good).sum()); pct=n/TOTAL*100
    c.markdown(f'<div class="phase {cl}"><div class="pcode">{code}</div><div class="pname">{name}</div><div class="pct">{pct:.1f}%</div><div class="psub">{n:,} {"Completed" if code=="P5" else "Submitted"}</div><div class="psub">of {TOTAL:,} students</div></div>',unsafe_allow_html=True)

st.markdown('<div class="section">📊 Portfolio Analytics</div>',unsafe_allow_html=True)
phases=["Discover","Design","Build","Decide","Defend"]
submitted=[int((df["P1 Status"]=="Submitted").sum()),int((df["P2 Status"]=="Submitted").sum()),int((df["P3 Status"]=="Submitted").sum()),int((df["P4 Status"]=="Submitted").sum()),int((df["P5 Status"]=="Completed").sum())]
pending=[int((df["P1 Status"]=="Pending").sum()),int((df["P2 Status"]=="Pending").sum()),int((df["P3 Status"]=="Pending").sum()),int((df["P4 Status"]=="Pending").sum()),int((df["P5 Status"]=="Pending").sum())]
inprog=[int((df["P1 Status"]=="In Progress").sum()),int((df["P2 Status"]=="In Progress").sum()),int((df["P3 Status"]=="In Progress").sum()),int((df["P4 Status"]=="In Progress").sum()),int((df["P5 Status"]=="In Progress").sum())]
revision=[int((df["P1 Status"]=="Revision").sum()),int((df["P2 Status"]=="Revision").sum()),int((df["P3 Status"]=="Revision").sum()),int((df["P4 Status"]=="Revision").sum()),0]

fig=go.Figure()
for name,vals,color in [("Submitted",submitted,"#00C853"),("In Progress",inprog,"#2979FF"),("Pending",pending,"#FF9100"),("Revision",revision,"#FF1744")]:
    fig.add_trace(go.Bar(name=name,x=phases,y=vals,text=vals,textposition="inside",marker_color=color))
fig.update_layout(title="Student Status by Phase",barmode="group",height=345,margin=dict(l=40,r=20,t=55,b=45),
                  xaxis_title="Portfolio Phase",yaxis_title="Students",legend=dict(orientation="h",y=1.08),plot_bgcolor="white",paper_bgcolor="white")
st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

c1,c2,c3=st.columns(3)
completion=[round(x/TOTAL*100,1) for x in submitted]
fig2=go.Figure(go.Bar(x=phases,y=completion,text=[f"{x}%" for x in completion],textposition="outside",marker_color=["#0057FF","#8E24AA","#00C853","#FF6D00","#FF1493"]))
fig2.update_layout(title="Phase Completion Rate",height=300,margin=dict(l=25,r=15,t=55,b=35),yaxis=dict(range=[0,100],title="%"),plot_bgcolor="white",paper_bgcolor="white")
c1.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})

fig3=go.Figure(go.Pie(labels=phases,values=submitted,hole=.55,textinfo="label+percent",marker_colors=["#0057FF","#8E24AA","#00C853","#FF6D00","#FF1493"]))
fig3.update_layout(title="Submission Mix",height=300,margin=dict(l=5,r=5,t=55,b=25),showlegend=False,plot_bgcolor="white",paper_bgcolor="white")
c2.plotly_chart(fig3,use_container_width=True,config={"displayModeBar":False})

tools=df["AI Tool"].value_counts().sort_values()
tool_colors=["#0057FF","#FF1744","#00C853","#FF6D00","#8E24AA","#00B8D4","#111111","#FF1493","#AA00FF","#64DD17"]
fig4=go.Figure(go.Bar(x=tools.values,y=tools.index,orientation="h",text=tools.values,textposition="outside",marker_color=tool_colors[:len(tools)]))
fig4.update_layout(title="AI Tools Selected",height=300,margin=dict(l=130,r=25,t=55,b=30),xaxis_title="Students",plot_bgcolor="white",paper_bgcolor="white")
c3.plotly_chart(fig4,use_container_width=True,config={"displayModeBar":False})

fac_prog=df.groupby("Faculty Assigned")["Overall Progress"].mean().sort_values()
fac_colors=["#FF1744","#0057FF","#00C853","#FF6D00","#111111","#FF1493","#8E24AA","#00B8D4","#AA00FF","#64DD17","#D50000","#2962FF","#00BFA5","#FF6F00"]
fig5=go.Figure(go.Bar(x=fac_prog.values,y=fac_prog.index,orientation="h",text=[f"{x:.0f}%" for x in fac_prog.values],textposition="outside",marker_color=fac_colors[:len(fac_prog)]))
fig5.update_layout(title="Faculty-wise Portfolio Progress",height=450,margin=dict(l=145,r=40,t=55,b=30),xaxis=dict(range=[0,100],title="Average Progress %"),plot_bgcolor="white",paper_bgcolor="white")
st.plotly_chart(fig5,use_container_width=True,config={"displayModeBar":False})

st.markdown('<div class="section">👨‍🏫 Faculty Progress — Click a Faculty</div>',unsafe_allow_html=True)
st.markdown('<div class="note">14 faculty are included. The allocation file has 20 populated sections; the 21st section is shown as “SECTION TO CONFIRM” instead of inventing a section code.</div>',unsafe_allow_html=True)

if "selected_faculty" not in st.session_state: st.session_state.selected_faculty=None
faculty_names=sorted(df["Faculty Assigned"].unique())

for start in range(0,len(faculty_names),4):
    cols=st.columns(4)
    for j,fac in enumerate(faculty_names[start:start+4]):
        fdf=df[df["Faculty Assigned"]==fac]; prog=fdf["Overall Progress"].mean()
        with cols[j]:
            if st.button(f"👨‍🏫 {fac}\n{len(fdf)} students • {prog:.0f}% progress",key=f"fac_{start}_{j}",use_container_width=True):
                st.session_state.selected_faculty=fac

if st.session_state.selected_faculty:
    fac=st.session_state.selected_faculty; fdf=df[df["Faculty Assigned"]==fac].copy()
    st.markdown(f'<div class="section">📋 {fac}</div>',unsafe_allow_html=True)
    m1,m2,m3,m4=st.columns(4)
    m1.metric("Students",len(fdf));m2.metric("Avg Progress",f'{fdf["Overall Progress"].mean():.1f}%')
    m3.metric("P1 Submitted",int((fdf["P1 Status"]=="Submitted").sum()))
    m4.metric("P1 Approved",int((fdf["P1 Faculty Approval"]=="Approved").sum()))

    fc=[(fdf["P1 Status"]=="Submitted").mean()*100,(fdf["P2 Status"]=="Submitted").mean()*100,(fdf["P3 Status"]=="Submitted").mean()*100,(fdf["P4 Status"]=="Submitted").mean()*100,(fdf["P5 Status"]=="Completed").mean()*100]
    figf=go.Figure(go.Scatter(x=phases,y=fc,mode="lines+markers+text",text=[f"{x:.0f}%" for x in fc],textposition="top center",line=dict(color="#FF1744",width=4),marker=dict(size=11,color=["#0057FF","#8E24AA","#00C853","#FF6D00","#FF1493"],line=dict(color="white",width=2)),fill="tozeroy",fillcolor="rgba(255,23,68,.08)"))
    figf.update_layout(title=f"{fac} — Phase Journey",height=275,margin=dict(l=35,r=20,t=55,b=35),yaxis=dict(range=[0,100],title="Completion %"),plot_bgcolor="white",paper_bgcolor="white")
    st.plotly_chart(figf,use_container_width=True,config={"displayModeBar":False})

    st.markdown('<div class="section">🔎 Find a Student</div>',unsafe_allow_html=True)
    q=st.text_input("Student Name / USN",placeholder="Type student name or USN...",key=f"q_{fac}")
    choice=st.selectbox("Choose Student",["Select Student"]+sorted(fdf["Student Name"].tolist()),key=f"s_{fac}")
    student=None
    if q.strip():
        ql=q.lower().strip(); m=fdf[fdf["Student Name"].str.lower().str.contains(ql,na=False)|fdf["USN"].str.lower().str.contains(ql,na=False)]
        if len(m)==1: student=m.iloc[0]
        elif len(m)>1:
            nm=st.selectbox("Matching Students",m["Student Name"].tolist(),key=f"m_{fac}"); student=m[m["Student Name"]==nm].iloc[0]
        else: st.warning("No student found.")
    elif choice!="Select Student": student=fdf[fdf["Student Name"]==choice].iloc[0]

    if student is not None:
        st.markdown(f'<div class="section">🧑‍🎓 {student["Student Name"]}</div>',unsafe_allow_html=True)
        a,b,c,d=st.columns(4);a.metric("USN",student["USN"]);b.metric("Section",student["Section"]);c.metric("Progress",f'{student["Overall Progress"]}%');d.metric("Current Phase",student["Current Phase"])
        ac="green" if student["P1 Faculty Approval"]=="Approved" else "orange" if student["P1 Faculty Approval"]=="Pending Review" else "red"
        st.markdown(f'<div class="detail"><span class="pill {ac}">Problem Statement: {student["P1 Faculty Approval"]}</span> {student["P1 Faculty Remarks"]}<br><br><b>🤖 AI Tool:</b> {student["AI Tool"]}<br><b>💡 Problem:</b> {student["Problem Statement"]}</div>',unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({"Phase":["Discover","Design","Build","Decide","Defend"],"Status":[student["P1 Status"],student["P2 Status"],student["P3 Status"],student["P4 Status"],student["P5 Status"]],"Attachment":[student["P1 Attachment"] or "No Attachment",student["P2 Attachment"] or "No Attachment",student["P3 Attachment"] or "No Attachment",student["P4 Attachment"] or "No Attachment",student["P5 Attachment"] or "No Attachment"]}),use_container_width=True,hide_index=True)

st.markdown('<div class="note" style="text-align:center;margin-top:8px;">AIC Portfolio Challenge • Synthetic Demo • No marks displayed</div>',unsafe_allow_html=True)