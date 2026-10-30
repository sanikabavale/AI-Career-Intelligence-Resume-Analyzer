import streamlit as st
import streamlit.components.v1 as components
from core.graph_engine import build_graph,graph_html

def render():
    st.markdown('<div class="eyebrow">CONNECTED SKILL INTELLIGENCE</div><h1>Knowledge graph</h1><p class="muted">Explore relationships between your detected skills and recommended roles.</p>',unsafe_allow_html=True)
    text=st.session_state.get("resume_text",""); results=st.session_state.get("job_results",[])
    if not text: st.info("Graph तयार करण्यासाठी आधी resume analyze करा."); return
    graph=build_graph(text,results)
    a,b,c=st.columns(3); a.metric("Nodes",graph.number_of_nodes()); b.metric("Relationships",graph.number_of_edges()); c.metric("Job roles",sum(1 for _,d in graph.nodes(data=True) if d.get("kind")=="job"))
    components.html(graph_html(graph),height=650,scrolling=False)
    st.markdown("#### Graph legend")
    st.write("🟢 Candidate · 🔵 Detected skill · 🟣 Job role · 🟠 Missing required skill")
    st.caption("Graph entities are derived from detected resume skills and job-library requirements. Review the extracted profile if the graph looks incomplete.")
