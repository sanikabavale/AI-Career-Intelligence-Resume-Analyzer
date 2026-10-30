from core.scoring import extract_skills, score_job, rank_jobs
from core.job_catalog import JOBS

def test_extract_skills_finds_known_terms():
    skills=extract_skills("Built a Python project using Pandas and SQL. Used JavaScript for a small web UI.")
    assert "Python" in skills and "SQL" in skills and "JavaScript" in skills

def test_score_is_bounded():
    result=score_job("Python SQL Pandas projects education", JOBS[0])
    assert 0 <= result["score"] <= 100

def test_rank_jobs_sorted():
    results=rank_jobs("Python SQL Pandas Machine Learning projects education", limit=8)
    assert len(results)==8
    assert results[0]["score"] >= results[-1]["score"]
