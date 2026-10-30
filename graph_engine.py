import networkx as nx
from .scoring import extract_skills


def build_graph(resume_text, job_results=None, max_jobs=8):
    graph=nx.Graph()
    graph.add_node("Candidate", kind="candidate", color="#67E8C0", size=32)
    skills=extract_skills(resume_text)
    for skill in skills:
        graph.add_node(skill, kind="skill", color="#46B7D4", size=18)
        graph.add_edge("Candidate",skill,relation="has_skill")
    for result in (job_results or [])[:max_jobs]:
        role=result["title"]
        graph.add_node(role,kind="job",color="#A78BFA",size=24,score=result["score"])
        for skill in result.get("matched_skills",[]):
            if skill in graph: graph.add_edge(skill,role,relation="supports_match")
        for skill in result.get("missing_required",[]):
            if skill not in graph:
                graph.add_node(skill,kind="missing_skill",color="#F59E0B",size=14)
            graph.add_edge(role,skill,relation="skill_gap")
    return graph


def graph_html(graph):
    from pyvis.network import Network
    net=Network(height="620px",width="100%",bgcolor="#08111F",font_color="#E8F0F7",directed=False,notebook=False)
    net.barnes_hut()
    for node,data in graph.nodes(data=True):
        title=f"{node}\nType: {data.get('kind','entity')}"
        if "score" in data: title+=f"\nMatch score: {data['score']}%"
        net.add_node(node,label=node,title=title,color=data.get("color","#67E8C0"),size=data.get("size",16))
    for a,b,data in graph.edges(data=True): net.add_edge(a,b,title=data.get("relation","related"),label=data.get("relation",""))
    return net.generate_html()
