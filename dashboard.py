import streamlit as st
from database.db import get_history

def render():
    st.markdown('<div class="eyebrow">YOUR WORKSPACE</div><h1>Career overview</h1><p class="muted">A clearer view of your skills, target roles and next steps.</p>',unsafe_allow_html=True)
    results=st.session_state.get("job_results",[]); skills=st.session_state.get("resume_skills",[]); resume=st.session_state.get("resume_text","")
    history=get_history(st.session_state.user_id)
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Resume status","Analyzed" if resume else "Not uploaded")
    c2.metric("Skills detected",len(skills))
    c3.metric("Roles evaluated",len(results))
    c4.metric("Saved analyses",len(history))
    st.markdown("### Recommended next actions")
    a,b,c=st.columns(3)
    with a:
        st.markdown('<div class="card"><h3>01 · Analyze resume</h3><p class="muted">Extract skills and experience from a PDF or DOCX.</p></div>',unsafe_allow_html=True)
        if st.button("Open Resume Analyzer",use_container_width=True): st.info("Choose Resume Analyzer in the sidebar.")
    with b:
        st.markdown('<div class="card"><h3>02 · Explore roles</h3><p class="muted">Compare your profile with software and IT careers.</p></div>',unsafe_allow_html=True)
        if st.button("Explore job matches",use_container_width=True): st.info("Choose Job Explorer in the sidebar.")
    with c:
        st.markdown('<div class="card"><h3>03 · Build a roadmap</h3><p class="muted">Turn missing skills into a prioritized learning plan.</p></div>',unsafe_allow_html=True)
        if st.button("Open roadmap",use_container_width=True): st.info("Choose Career Roadmap in the sidebar.")
    if results:
        st.markdown("### Your current top matches")
        for r in results[:5]:
            st.write(f"**{r['title']}** · {r['category']}")
            st.progress(r["score"]/100,text=f"{r['score']}% match")
    else: st.info("Start with Resume Analyzer to generate personalized results.")
