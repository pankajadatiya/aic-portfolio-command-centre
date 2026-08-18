import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="AIC Portfolio Challenge",page_icon="🎯",layout="wide")

@st.cache_data
def make_data():
    rng=np.random.default_rng(20260818)
    faculty=["Geeta Maladkar","Shobha K.B.","Bhawna S.","Rajesh A.","B. Manjunath","Vipanchi V.","Dr. M. Maheswari","Anup A","Srividhya C.","Arun","Purushotham H.C.","Pankaj Adatiya","Additional Faculty"]
    sections=[f"S{i:02d}" for i in range(1,21)]
    sf={s:faculty[i%len(faculty)] for i,s in enumerate(sections)}
    tools=["ChatGPT","Gemini","Microsoft Copilot","Canva","Gamma","Power BI","Excel","ChatGPT + Canva","ChatGPT + Power BI","Gemini + Canva"]
    problems=["Reducing Customer Waiting Time","Improving Student Attendance Tracking","Reducing Food Waste","Improving Inventory Management","Customer Complaint Resolution","Personalized Learning Support","Reducing Paper Usage","Improving Customer Feedback Analysis","Reducing Delivery Delays","Streamlining Event Registration"]
    rows=[]
    for i in range(1,1101):
        sec=sections[(i-1)%20]; fac=sf[sec]
        p1=rng.choice(["Submitted","Pending","In Progress","Revision"],p=[.74,.10,.10,.06])
        p2=rng.choice(["Submitted","Pending","In Progress","Revision"],p=[.61,.15,.17,.07])
        p3=rng.choice(["Submitted","Pending","In Progress","Revision"],p=[.48,.19,.25,.08])
        p4=rng.choice(["Submitted","Pending","In Progress","Revision"],p=[.31,.23,.38,.08])
        p5=rng.choice(["Completed","Pending","In Progress"],p=[.08,.72,.20])
        done=sum(x=="Submitted" for x in [p1,p2,p3,p4])+int(p5=="Completed")
        approval=rng.choice(["Approved","Pending Review","Revision Required"],p=[.72,.18,.10]) if p1=="Submitted" else "Pending Review"
        rows.append({"Student Name":f"Student {i:04d}","USN":f"AIC26-{i:04d}","Section":sec,"Faculty Assigned":fac,"Overall Progress":done*20,"Current Phase":("Phase 5 – Defend" if p5=="Completed" else "Phase 4 – Decide" if p4=="Submitted" else "Phase 3 – Build" if p3=="Submitted" else "Phase 2 – Design" if p2=="Submitted" else "Phase 1 – Discover"),"P1 Status":p1,"P2 Status":p2,"P3 Status":p3,"P4 Status":p4,"P5 Status":p5,"P1 Faculty Approval":approval,"P1 Faculty Remarks":"Problem statement approved by faculty." if approval=="Approved" else "Awaiting faculty review / revision.","P1 Problem Statement":rng.choice(problems),"P1 AI Opportunity":"AI can support analysis, prediction and decision-making.","P2 Selected AI Tool":rng.choice(tools),"P2 Proposed Solution":"AI-enabled solution designed around the identified problem.","P3 Platform":rng.choice(["Power BI","Excel","Streamlit","Canva","Python","Google Workspace"]),"P4 Recommendation":"Use the proposed AI solution to improve the identified process.","P1 Attachment":"Submitted File" if p1=="Submitted" and rng.random()<.78 else "","P2 Attachment":"Submitted File" if p2=="Submitted" and rng.random()<.78 else "","P3 Attachment":"Submitted File" if p3=="Submitted" and rng.random()<.78 else "","P4 Attachment":"Submitted File" if p4=="Submitted" and rng.random()<.78 else "","P5 Attachment":"Submitted File" if p5=="Completed" and rng.random()<.78 else ""})
    return pd.DataFrame(rows)

df=make_data(); total=len(df)

st.markdown('''<style>
#MainMenu,footer,header{visibility:hidden}.block-container{padding:.55rem .8rem}.hero{background:linear-gradient(110deg,#ff1744,#0057ff,#8e24aa);color:#fff;border-radius:16px;padding:14px 18px;margin-bottom:7px}.hero h1{font-size:29px;margin:0;font-weight:900}.hero p{font-size:12px;margin:4px 0 0}.live{float:right;background:#ffffff33;padding:5px 9px;border-radius:20px;font-size:9px;font-weight:900}.section{font-size:17px;font-weight:900;color:#111827;margin:10px 0 6px}.kpi{border:2px solid #dbeafe;border-radius:12px;padding:8px;height:68px;background:#fff}.kpi-label{font-size:9px;font-weight:900;color:#111827}.kpi-value{font-size:24px;font-weight:900;margin-top:4px}.phase{border-radius:13px;padding:10px;height:108px;border:2px solid;box-sizing:border-box;overflow:hidden}.p1{background:#dbeafe;border-color:#0057ff}.p2{background:#f3e8ff;border-color:#8e24aa}.p3{background:#d1fae5;border-color:#00c853}.p4{background:#ffedd5;border-color:#ff6d00}.p5{background:#fce7f3;border-color:#ff2d95}.pcode{font-size:9px;font-weight:900}.pname{font-size:14px;font-weight:900;margin-top:5px}.pct{font-size:23px;font-weight:900;margin-top:7px}.small{font-size:9px;color:#374151}.stButton>button{min-height:48px!important;border-radius:10px!important;font-weight:800!important;font-size:10px!important}.tool{background:#fff3e0;border:2px solid #ff6d00;border-radius:10px;padding:8px;font-weight:900;color:#111827}
</style>''',unsafe_allow_html=True)
st.markdown('<div class="hero"><span class="live">● LIVE</span><h1>🎯 AIC Portfolio Challenge</h1><p>Phase-wise Progress • Faculty Monitoring • Student Submission Tracking</p></div>',unsafe_allow_html=True)

k=[("👥","STUDENTS",total),("👨‍🏫","FACULTY",df["Faculty Assigned"].nunique()),("🏫","SECTIONS",df.Section.nunique()),("🔵","P1 DISCOVER",int((df["P1 Status"]=="Submitted").sum())),("🟣","P2 DESIGN",int((df["P2 Status"]=="Submitted").sum())),("📈","AVG PROGRESS",f'{df["Overall Progress"].mean():.1f}%')]
for c,(i,l,v) in zip(st.columns(6),k): c.markdown(f'<div class="kpi"><div class="kpi-label">{i} {l}</div><div class="kpi-value">{v}</div></div>',unsafe_allow_html=True)

st.markdown('<div class="section">🚀 Portfolio Journey</div>',unsafe_allow_html=True)
ph=[("P1","DISCOVER","P1 Status","p1","Submitted"),("P2","DESIGN","P2 Status","p2","Submitted"),("P3","BUILD","P3 Status","p3","Submitted"),("P4","DECIDE","P4 Status","p4","Submitted"),("P5","DEFEND","P5 Status","p5","Completed")]
for c,(code,name,f,css,good) in zip(st.columns(5),ph):
    n=int((df[f]==good).sum()); c.markdown(f'<div class="phase {css}"><div class="pcode">{code}</div><div class="pname">{name}</div><div class="pct">{n/total*100:.1f}%</div><b>{n:,} {"Completed" if code=="P5" else "Submitted"}</b><div class="small">of {total:,} students</div></div>',unsafe_allow_html=True)

# CHART 1 — grouped vibrant bars
st.markdown('<div class="section">📊 Phase Status</div>',unsafe_allow_html=True)
phases=["Discover","Design","Build","Decide","Defend"]
vals={"Submitted":[(df[f]==g).sum() for f,g in [("P1 Status","Submitted"),("P2 Status","Submitted"),("P3 Status","Submitted"),("P4 Status","Submitted"),("P5 Status","Completed")]],"In Progress":[(df[f]=="In Progress").sum() for f in ["P1 Status","P2 Status","P3 Status","P4 Status","P5 Status"]],"Pending":[(df[f]=="Pending").sum() for f in ["P1 Status","P2 Status","P3 Status","P4 Status","P5 Status"]],"Revision":[(df[f]=="Revision").sum() for f in ["P1 Status","P2 Status","P3 Status","P4 Status"]]+[0]}
fig=go.Figure()
for name,color in [("Submitted","#00c853"),("In Progress","#2979ff"),("Pending","#ff9100"),("Revision","#ff1744")]: fig.add_trace(go.Bar(name=name,x=phases,y=vals[name],text=vals[name],textposition="inside",marker_color=color))
fig.update_layout(barmode="group",height=340,margin=dict(l=35,r=20,t=50,b=35),title="Student Status Across Portfolio Phases",xaxis_title="Phase",yaxis_title="Students",legend=dict(orientation="h",y=1.12),plot_bgcolor="#fff",paper_bgcolor="#fff")
st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

# CHART 2 — funnel
left,right=st.columns(2)
sub=vals["Submitted"]
fig2=go.Figure(go.Funnel(y=phases,x=sub,textinfo="value+percent initial",marker_color=["#0057ff","#8e24aa","#00c853","#ff6d00","#ff2d95"]))
fig2.update_layout(title="🚀 Portfolio Journey Funnel",height=330,margin=dict(l=45,r=25,t=50,b=20),paper_bgcolor="#fff",plot_bgcolor="#fff")
left.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})

# CHART 3 — donut
fig3=go.Figure(go.Pie(labels=phases,values=sub,hole=.55,textinfo="label+percent",marker=dict(colors=["#0057ff","#8e24aa","#00c853","#ff6d00","#ff2d95"],line=dict(color="#fff",width=2))))
fig3.update_layout(title="📌 Submission Mix by Phase",height=330,margin=dict(l=15,r=15,t=50,b=20),paper_bgcolor="#fff",legend=dict(orientation="h",y=-.05))
right.plotly_chart(fig3,use_container_width=True,config={"displayModeBar":False})

# CHART 4 — tools
st.markdown('<div class="section">🤖 AI Tool Adoption</div>',unsafe_allow_html=True)
tools=df["P2 Selected AI Tool"].value_counts().sort_values(); palette=["#0057ff","#ff1744","#00c853","#ff6d00","#8e24aa","#00b8d4","#111111","#ff2d95","#aa00ff","#64dd17"]
fig4=go.Figure(go.Bar(x=tools.values,y=tools.index,orientation="h",text=tools.values,textposition="outside",marker_color=[palette[i%len(palette)] for i in range(len(tools))]))
fig4.update_layout(title="AI Tools Selected by Students",height=360,margin=dict(l=150,r=45,t=50,b=30),xaxis_title="Students",plot_bgcolor="#fff",paper_bgcolor="#fff")
st.plotly_chart(fig4,use_container_width=True,config={"displayModeBar":False})

# CHART 5 — faculty progress
st.markdown('<div class="section">👨‍🏫 Faculty-wise Progress</div>',unsafe_allow_html=True)
fp=df.groupby("Faculty Assigned")["Overall Progress"].mean().sort_values(); fpcolors=["#ff1744","#0057ff","#00c853","#ff6d00","#111111","#ff2d95","#8e24aa","#00b8d4","#aa00ff","#64dd17","#d50000","#2962ff","#00bfa5"]
fig5=go.Figure(go.Bar(x=fp.values,y=fp.index,orientation="h",text=[f"{x:.0f}%" for x in fp.values],textposition="outside",marker_color=[fpcolors[i%len(fpcolors)] for i in range(len(fp))]))
fig5.update_layout(title="Average Portfolio Progress by Faculty",height=430,margin=dict(l=150,r=45,t=50,b=30),xaxis=dict(title="Average Progress %",range=[0,100]),plot_bgcolor="#fff",paper_bgcolor="#fff")
st.plotly_chart(fig5,use_container_width=True,config={"displayModeBar":False})

# FACULTY BUTTONS
st.markdown('<div class="section">👨‍🏫 Faculty Progress — Click a Faculty Name</div>',unsafe_allow_html=True)
if "selected_faculty" not in st.session_state: st.session_state.selected_faculty=None
names=sorted(df["Faculty Assigned"].unique())
for start in range(0,len(names),4):
    for j,fac in enumerate(names[start:start+4]):
        fdf=df[df["Faculty Assigned"]==fac]
        with st.columns(4)[j]:
            if st.button(f"👨‍🏫 {fac}\n{len(fdf)} Students • {fdf['Overall Progress'].mean():.0f}% Progress",key=f"fac_{start}_{j}",use_container_width=True): st.session_state.selected_faculty=fac

if st.session_state.selected_faculty:
    fac=st.session_state.selected_faculty; fdf=df[df["Faculty Assigned"]==fac].copy()
    st.markdown(f'<div class="section">📋 {fac} — Faculty Overview</div>',unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4); c1.metric("Students",len(fdf)); c2.metric("Avg Progress",f'{fdf["Overall Progress"].mean():.1f}%'); c3.metric("P1 Approved",int((fdf["P1 Faculty Approval"]=="Approved").sum())); c4.metric("P1 Revision",int((fdf["P1 Faculty Approval"]=="Revision Required").sum()))
    st.markdown('<div class="section">🔎 Search Student</div>',unsafe_allow_html=True)
    q=st.text_input("Student Name / USN",placeholder="Type name or USN...",key=f"q_{fac}"); choice=st.selectbox("Choose Student",["Select Student"]+sorted(fdf["Student Name"].tolist()),key=f"s_{fac}")
    student=None
    if q.strip():
        ql=q.lower().strip(); m=fdf[fdf["Student Name"].str.lower().str.contains(ql,na=False)|fdf["USN"].str.lower().str.contains(ql,na=False)]
        if len(m): student=m.iloc[0]
    elif choice!="Select Student": student=fdf[fdf["Student Name"]==choice].iloc[0]
    if student is not None:
        st.markdown(f'<div class="section">🧑‍🎓 {student["Student Name"]}</div>',unsafe_allow_html=True)
        a,b,c,d=st.columns(4); a.metric("USN",student["USN"]); b.metric("Section",student["Section"]); c.metric("Progress",f'{student["Overall Progress"]}%'); d.metric("Current Phase",student["Current Phase"])
        st.markdown(f'<div class="tool">🤖 AI TOOL CHOSEN: {student["P2 Selected AI Tool"]}</div>',unsafe_allow_html=True)
        st.info(f'Problem Statement — Faculty Approval: {student["P1 Faculty Approval"]} | {student["P1 Faculty Remarks"]}')
        st.dataframe(pd.DataFrame({"Phase":["Discover","Design","Build","Decide","Defend"],"Status":[student["P1 Status"],student["P2 Status"],student["P3 Status"],student["P4 Status"],student["P5 Status"]],"Attachment":[student["P1 Attachment"] or "No Attachment",student["P2 Attachment"] or "No Attachment",student["P3 Attachment"] or "No Attachment",student["P4 Attachment"] or "No Attachment",student["P5 Attachment"] or "No Attachment"]}),use_container_width=True,hide_index=True)
        st.markdown(f'**Problem Statement:** {student["P1 Problem Statement"]}  \n**AI Opportunity:** {student["P1 AI Opportunity"]}  \n**Proposed Solution:** {student["P2 Proposed Solution"]}  \n**Build Platform:** {student["P3 Platform"]}  \n**Recommendation:** {student["P4 Recommendation"]}')
