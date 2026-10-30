def build_roadmap(job_result, hours_per_week=5):
    missing=job_result.get("missing_required",[])+job_result.get("missing_preferred",[])
    missing=list(dict.fromkeys(missing))
    if not missing:
        return [{"week":"Week 1","focus":"Strengthen evidence","tasks":["Add measurable, truthful project outcomes to the resume.","Prepare interview explanations for your strongest matched skills.","Compare your resume with a specific current job description."]}]
    roadmap=[]
    for i in range(0,len(missing),2):
        chunk=missing[i:i+2]
        week_num=i//2+1
        roadmap.append({"week":f"Week {week_num}","focus":" + ".join(chunk),"tasks":[f"Learn the fundamentals of {skill} and complete a small guided exercise." for skill in chunk]+[f"Build or improve a small project that demonstrates {', '.join(chunk)}." ]})
    roadmap.append({"week":f"Week {len(roadmap)+1}","focus":"Portfolio and interview preparation","tasks":["Document project architecture and your contribution.","Practice role-specific questions and explain technical trade-offs.","Update the resume only with skills and outcomes you can support with evidence."]})
    return roadmap
