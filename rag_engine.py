import re
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

KNOWLEDGE = [
 ("Frontend development", "Frontend developers build user interfaces. Core skills commonly include HTML, CSS, JavaScript, responsive design, accessibility and a framework such as React or Angular. Practice by building accessible, responsive projects."),
 ("Backend development", "Backend developers build APIs, business logic, authentication and database integrations. Common skills include a programming language, REST APIs, SQL, testing, security and deployment."),
 ("Data analyst", "Data analysts work with SQL, spreadsheets, data cleaning, statistics and visualization. Common portfolio projects include dashboards, exploratory analysis and clear business recommendations."),
 ("Machine learning", "Machine learning roles often require Python, data preparation, model selection, evaluation and communicating limitations. Relevant projects should show baselines, metrics and reproducible experiments."),
 ("Generative AI and RAG", "RAG systems retrieve relevant passages from a knowledge base and provide them as context to a language model. A reliable system cites retrieved sources, evaluates retrieval quality and avoids claims unsupported by the evidence."),
 ("Cybersecurity", "Cybersecurity roles commonly require networking, operating-system fundamentals, logs, security concepts, incident handling and careful documentation. Practice should take place only in authorized labs."),
 ("Cloud and DevOps", "Cloud and DevOps roles commonly use Linux, Git, scripting, CI/CD, containers, monitoring and a cloud platform. Portfolio projects should document deployment, reliability and security choices."),
 ("Resume projects", "A strong technical project explains the problem, personal contribution, technologies, implementation, results and trade-offs. Include measurable outcomes only when they can be substantiated."),
 ("Interview preparation", "Prepare to explain technical decisions, trade-offs, debugging steps, project architecture and what you would improve. Practice coding and role-specific fundamentals relevant to the job description."),
 ("Skill gap planning", "Prioritize skills that are both required by the target role and missing from the current profile. Learn prerequisites first, then build a small project that demonstrates the skill."),
]


def retrieve(query, extra_text="", k=4):
    docs=[{"source":name,"text":text} for name,text in KNOWLEDGE]
    if extra_text.strip(): docs.append({"source":"Uploaded resume/job description","text":extra_text[:18000]})
    corpus=[d["source"]+". "+d["text"] for d in docs]
    try:
        vec=TfidfVectorizer(stop_words="english",ngram_range=(1,2),max_features=12000)
        matrix=vec.fit_transform(corpus+[query])
        sims=cosine_similarity(matrix[-1],matrix[:-1]).ravel()
        order=sims.argsort()[::-1][:k]
        return [{**docs[i],"similarity":float(sims[i])} for i in order if sims[i]>0]
    except ValueError:
        return docs[:k]


def answer_question(question, resume_text="", job_context=""):
    context="\n\n".join(f"Source: {d['source']}\n{d['text']}" for d in retrieve(question, resume_text+"\n"+job_context,k=4))
    if not context.strip(): return "मला उपलब्ध career knowledge मध्ये यासाठी पुरेसा संदर्भ सापडला नाही. अधिक specific प्रश्न विचारा किंवा job description द्या.", []
    try:
        from dotenv import load_dotenv
        import os
        load_dotenv()
        if os.getenv("OPENAI_API_KEY"):
            from langchain_openai import ChatOpenAI
            from langchain_core.messages import SystemMessage, HumanMessage
            model=ChatOpenAI(model=os.getenv("OPENAI_MODEL","gpt-4o-mini"),temperature=0.1,timeout=30)
            response=model.invoke([SystemMessage(content="You are a careful career assistant. Answer only from the supplied context where possible. Clearly say when information is insufficient. Do not invent resume facts. Cite source labels in square brackets."),HumanMessage(content=f"Context:\n{context}\n\nQuestion: {question}")])
            return response.content, retrieve(question,resume_text+"\n"+job_context,k=4)
    except Exception as e:
        return f"AI API सध्या उपलब्ध नाही ({type(e).__name__}). खाली retrieved context वर आधारित उत्तर दिले आहे.\n\n{context}", retrieve(question,resume_text+"\n"+job_context,k=4)
    return "API key configured नाही; म्हणून हे offline retrieval-based उत्तर आहे. खालील sources तपासा:\n\n"+context, retrieve(question,resume_text+"\n"+job_context,k=4)
