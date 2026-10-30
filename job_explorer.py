import streamlit as st
import pandas as pd
from core.job_catalog import JOBS
from core.scoring import rank_jobs

def render():
    st.markdown('<div class="eyebrow">ROLE DISCOVERY</div><h1>Job explorer</h1><p class="muted">Browse the built-in IT job library or match your resume against a custom job description.</p>',unsafe_allow_html=True)
    resume=st.session_state.get("resume_text","")
    categories=sorted({j["category"] for j in JOBS})
    selected=st.multiselect("Filter by category",categories,default=categories)
    level=st.selectbox("Experience level",["All levels"]+sorted({j["level"] for j in JOBS}))
    filtered=[j for j in JOBS if j["category"] in selected and (level=="All levels" or j["level"]==level)]
    custom=st.text_area("Optional: paste a specific job description",height=150,placeholder="Paste responsibilities, required skills and preferred qualifications here…")
    if custom.strip():
        from core.scoring import score_job
        custom_job={"title":"Custom job description","category":"Custom","level":"User supplied","required":[],"preferred":[],"description":custom}
        # Extract requirements from text by matching known skill terms. This is transparent and can be reviewed.
        from core.scoring import extract_skills
        found=extract_skills(custom)
        custom_job["required"]=found[:min(8,len(found))]
        custom_job["preferred"]=found[8:]
        if st.button("Analyze custom job description"):
            if not resume: st.warning("पहिले Resume Analyzer मध्ये resume upload करा.")
            elif not found: st.warning("Known skills extract झाल्या नाहीत. Job description अधिक specific करा.")
            else:
                result=score_job(resume,custom_job); st.session_state.custom_job_result=result
        if st.session_state.get("custom_job_result"):
            r=st.session_state.custom_job_result; st.metric("Custom job compatibility",f"{r['score']}%"); st.write("Matched skills:",", ".join(r["matched_skills"]) or "None"); st.write("Missing skills:",", ".join(r["missing_skills"]) or "None")
    st.markdown(f"### Job library · {len(filtered)} roles")
    query=st.text_input("Search job titles or skills",placeholder="e.g. React, Python, cybersecurity")
    if query:
        filtered=[j for j in filtered if query.lower() in (j["title"]+" "+j["description"]+" "+" ".join(j["required"]+j["preferred"])).lower()]
    rows=[]
    for j in filtered:
        rows.append({"Job role":j["title"],"Category":j["category"],"Level":j["level"],"Required skills":", ".join(j["required"]),"Preferred skills":", ".join(j["preferred"])})
    st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
    if resume and filtered:
        results=rank_jobs(resume,filtered)
        st.markdown("### Matches in selected categories")
        st.dataframe(pd.DataFrame([{"Role":r["title"],"Match":f"{r['score']}%","Matched required":", ".join(r["matched_required"]),"Missing required":", ".join(r["missing_required"])} for r in results]),use_container_width=True,hide_index=True)
    st.caption("The starter job catalog is extensible, not an exhaustive list of every title used by every employer.")
