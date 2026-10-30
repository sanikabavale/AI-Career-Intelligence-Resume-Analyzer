import streamlit as st
from core.rag_engine import answer_question

def render():
    st.markdown('<div class="eyebrow">RETRIEVAL-GROUNDED GUIDANCE</div><h1>Career assistant</h1><p class="muted">Ask about your skills, target roles, projects or learning priorities.</p>',unsafe_allow_html=True)
    resume=st.session_state.get("resume_text","")
    results=st.session_state.get("job_results",[])
    selected=st.selectbox("Job context",["General career advice"]+[r["title"] for r in results[:15]])
    context=""
    if selected!="General career advice":
        r=next((x for x in results if x["title"]==selected),None)
        if r: context=f"Job: {r['title']}\nMatched skills: {r['matched_skills']}\nMissing skills: {r['missing_skills']}\nDescription: {r['description']}"
    question=st.text_area("Your question",placeholder="Which skills should I learn next for this role?",height=100)
    if st.button("Generate answer",type="primary"):
        if not question.strip(): st.warning("आधी प्रश्न लिहा.")
        else:
            with st.spinner("Retrieving relevant career knowledge…"):
                answer,sources=answer_question(question,resume,context)
            st.markdown("### Answer"); st.write(answer)
            if sources:
                st.markdown("### Retrieved sources")
                for s in sources: st.markdown(f"**{s['source']}** · retrieval similarity {s['similarity']:.2f}"); st.caption(s['text'][:600])
    st.caption("Without an API key, the assistant uses local retrieval and does not generate a full LLM response. With an API key, LangChain ChatOpenAI is used where configured.")
