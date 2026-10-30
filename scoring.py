import re
from .job_catalog import JOBS, ALIASES

SKILL_TERMS = sorted({s for j in JOBS for s in j["required"] + j["preferred"]} | {
 "Python","Java","C++","C#","C","JavaScript","TypeScript","HTML","CSS","SQL","NoSQL","Git","Linux","Excel","Pandas","NumPy","Scikit-learn","PyTorch","TensorFlow","LangChain","RAG","FAISS","NetworkX","PyVis","Streamlit","Flask","FastAPI","Django","React","Node.js","AWS","Azure","GCP","Docker","Kubernetes","Power BI","Tableau","Figma","Selenium","Playwright","Pytest","OpenCV","NLP","LLMs","Embeddings","Vector Search","Prompt Engineering","Machine Learning","Deep Learning","Statistics","Data Analysis","Data Visualization","OOP","DSA","REST APIs","CI/CD","Networking","TCP/IP","Cybersecurity","Computer Vision","Blockchain","QGIS","PostgreSQL","MySQL","MongoDB","PHP","WordPress","Spring Boot","Flutter","Kotlin","Swift","Terraform","Airflow","Spark","Pandas","ETL","Data Modeling","Microcontrollers","Verilog/VHDL","Digital Electronics","Troubleshooting","Testing","Manual Testing","Figma","Wireframing","Prototyping","User Research","Accessibility","Authentication","Deployment","Debugging","Security Fundamentals","SIEM","Incident Response","Cloud Fundamentals","Monitoring","Scripting","Test Cases","Bug Reporting","SDLC","DAX","Data Warehouse","Model Evaluation","Transformers","API Testing","OWASP","SAST","DAST","Threat Modeling","Routing and Switching","DNS","DHCP","Firewalls","VPN","Windows Server","Backup and Recovery","Virtualization","MQTT","Sensors","RTOS","Embedded Linux","FPGA","ASIC Design","Spatial Data","Web Mapping","Communication","Ticketing Tools","Operating Systems","Hardware Support","Design Patterns","Maven","Express","Laravel","ASP.NET","Accessibility","SEO","Plugin Development","Jetpack Compose","Unity","Unreal Engine","3D Mathematics","Cryptography Basics","Smart Contracts","Web3","ETL","Database Administration","Performance Tuning","Data Modeling","Cloud","Authentication","REST APIs","Programming","User Interface","User Experience"})


def canonicalize(text):
    t=text.lower()
    for alias, canonical in sorted(ALIASES.items(), key=lambda x: len(x[0]), reverse=True):
        t=re.sub(r"(?<![a-z0-9])"+re.escape(alias)+r"(?![a-z0-9])", canonical.lower(), t)
    return t


def extract_skills(text):
    norm=canonicalize(text)
    found=[]
    for skill in SKILL_TERMS:
        if re.search(r"(?<![a-z0-9])"+re.escape(skill.lower())+r"(?![a-z0-9])", norm, flags=re.I):
            if skill not in found: found.append(skill)
    return sorted(found, key=str.lower)


def score_job(resume_text, job):
    """Transparent heuristic score. Returns category-level scores and evidence."""
    resume_skills=set(extract_skills(resume_text))
    required=list(dict.fromkeys(job.get("required", [])))
    preferred=list(dict.fromkeys(job.get("preferred", [])))
    all_skills=list(dict.fromkeys(required+preferred))
    matched_req=[s for s in required if s in resume_skills]
    missing_req=[s for s in required if s not in resume_skills]
    matched_pref=[s for s in preferred if s in resume_skills]
    missing_pref=[s for s in preferred if s not in resume_skills]
    req_score=(len(matched_req)/len(required)*100) if required else 0
    pref_score=(len(matched_pref)/len(preferred)*100) if preferred else 0
    # Main score combines core skill coverage and supporting resume evidence.
    skills_score = 0.75*req_score + 0.25*pref_score
    text=canonicalize(resume_text)
    # Evidence signals are deliberately conservative and do not infer years from vague text.
    exp_terms=["experience","internship","employment","worked","developer","engineer"]
    experience_score= min(100, sum(1 for term in exp_terms if term in text)*17)
    project_score=100 if re.search(r"\b(project|projects|built|developed|implemented)\b", text) else 25
    education_score=100 if re.search(r"\b(bachelor|b\.tech|btech|b\.e\.|degree|college|university|diploma|bsc|msc|education)\b", text) else 45
    keyword_hits=sum(1 for term in all_skills if term.lower() in text)
    keyword_score=(keyword_hits/len(all_skills)*100) if all_skills else 0
    total=0.55*skills_score + 0.15*experience_score + 0.15*project_score + 0.08*education_score + 0.07*keyword_score
    total=round(max(0,min(100,total)))
    return {"title":job["title"],"category":job["category"],"level":job["level"],"score":total,
            "skills_score":round(skills_score),"required_score":round(req_score),"preferred_score":round(pref_score),
            "experience_score":round(experience_score),"project_score":round(project_score),"education_score":round(education_score),"keyword_score":round(keyword_score),
            "matched_required":matched_req,"missing_required":missing_req,"matched_preferred":matched_pref,"missing_preferred":missing_pref,
            "matched_skills":matched_req+matched_pref,"missing_skills":missing_req+missing_pref,
            "description":job.get("description","")}


def rank_jobs(resume_text, jobs=None, limit=None):
    jobs=jobs or JOBS
    results=[score_job(resume_text,job) for job in jobs]
    results.sort(key=lambda x:(x["score"],len(x["matched_required"])), reverse=True)
    return results[:limit] if limit else results
