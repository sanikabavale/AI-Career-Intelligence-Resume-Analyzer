import streamlit as st
import pandas as pd
from core.resume_parser import extract_text, normalize_text
from core.scoring import extract_skills, rank_jobs
from core.job_catalog import JOBS
from database.db import save_analysis

def render():
    st.markdown('<div class="eyebrow">PROFILE INTELLIGENCE</div><h1>Resume analyzer</h1><p class="muted">Upload a resume, review extracted skills, then inspect explainable job matches.</p>',unsafe_allow_html=True)
    uploaded=st.file_uploader("Upload resume",type=["pdf","docx","txt","png","jpg","jpeg","tiff","webp"],help="PDF, DOCX, TXT or image. Scanned PDF OCR needs Tesseract installed.")
    if uploaded and st.button("Analyze resume",type="primary",use_container_width=True):
        try:
            with st.spinner("Reading resume and matching skills…"):
                text=normalize_text(extract_text(uploaded))
                if len(text)<30: st.error("Resume मधून पुरेसा text मिळाला नाही."); st.stop()
                skills=extract_skills(text)
                results=rank_jobs(text)
                st.session_state.resume_text=text; st.session_state.resume_skills=skills; st.session_state.job_results=results; st.session_state.resume_filename=uploaded.name
                save_analysis(st.session_state.user_id,uploaded.name,skills,results[:15])
            st.success("Resume analysis complete.")
        except Exception as e: st.error(f"Resume process करता आला नाही: {e}")
    text=st.session_state.get("resume_text","")
    if text:
        skills=st.session_state.get("resume_skills",[]); results=st.session_state.get("job_results",[])
        st.markdown("### Extracted profile")
        a,b,c=st.columns(3); a.metric("Skills detected",len(skills)); b.metric("Roles compared",len(results)); c.metric("Resume characters",len(text))
        if skills: st.write(" · ".join(f"`{s}`" for s in skills))
        else: st.warning("Known skills सापडल्या नाहीत. Extracted text तपासा.")
        with st.expander("Review extracted text",expanded=False): st.text_area("Extracted resume text",text,height=260,disabled=True)
        st.markdown("### Best-matching roles")
        for r in results[:10]:
            with st.container(border=True):
                left,right=st.columns([3,1]); left.subheader(r["title"]); left.caption(f"{r['category']} · {r['level']}"); right.metric("Match",f"{r['score']}%")
                st.progress(r["score"]/100)
                st.caption(f"Matched required: {', '.join(r['matched_required']) or 'None detected'}")
                st.caption(f"Missing required: {', '.join(r['missing_required']) or 'None detected'}")
                with st.expander("Why this score?"):
                    st.write({"Skills":r["skills_score"],"Experience signal":r["experience_score"],"Project signal":r["project_score"],"Education signal":r["education_score"],"Keywords":r["keyword_score"]})
                    st.write("Preferred skills found:",", ".join(r["matched_preferred"]) or "None detected")
        df=pd.DataFrame([{k:r[k] for k in ["title","category","level","score","matched_required","missing_required","matched_preferred","missing_preferred"]} for r in results])
        st.download_button("Download job match results (CSV)",df.to_csv(index=False).encode("utf-8-sig"),file_name="career_job_matches.csv",mime="text/csv")
        st.caption("Scores are heuristic compatibility estimates, not hiring probabilities. Parsing may miss skills depending on resume formatting; review the extracted text.")
