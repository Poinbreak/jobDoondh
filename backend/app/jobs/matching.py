import re
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.db.client import supabase

def compute_match_scores(user_id: str):
    """
    Computes match scores for all job postings for a given user.
    Uses TF-IDF + cosine similarity (60%) and explicit skill keyword overlap (40%).
    Upserts into match_scores table.
    """
    # 1. Fetch user skills
    skills_resp = supabase.table('skills').select('skill_name').eq('user_id', user_id).execute()
    user_skills = [s['skill_name'].lower() for s in skills_resp.data] if skills_resp.data else []
    
    # 2. Fetch user resume text
    resumes_resp = supabase.table('resumes').select('parsed_text').eq('user_id', user_id).order('uploaded_at', desc=True).limit(1).execute()
    resume_text = resumes_resp.data[0]['parsed_text'] if resumes_resp.data else ""
    
    # User document for TF-IDF
    user_doc = " ".join(user_skills) + " " + resume_text
    if not user_doc.strip():
        # Nothing to match against
        return []

    # 3. Fetch all job postings
    jobs_resp = supabase.table('job_postings').select('id, description, extracted_skills').execute()
    jobs = jobs_resp.data
    
    if not jobs:
        return []
        
    job_docs = [j['description'] or "" for j in jobs]
    job_ids = [j['id'] for j in jobs]
    
    # 4. TF-IDF Cosine Similarity
    vectorizer = TfidfVectorizer(stop_words='english')
    # Fit transform on all docs (user + jobs)
    all_docs = [user_doc] + job_docs
    tfidf_matrix = vectorizer.fit_transform(all_docs)
    
    # First row is user, rest are jobs
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    # 5. Compute scores and keyword overlaps
    match_results = []
    
    for idx, job in enumerate(jobs):
        job_id = job_ids[idx]
        job_desc_lower = job_docs[idx].lower()
        
        # Calculate skill overlap ratio
        matched_skills = []
        missing_skills = []
        
        if user_skills:
            for skill in user_skills:
                # Basic check if skill exists in job description
                if re.search(r'\b' + re.escape(skill) + r'\b', job_desc_lower):
                    matched_skills.append(skill)
                else:
                    missing_skills.append(skill)
                    
            overlap_ratio = len(matched_skills) / len(user_skills)
        else:
            overlap_ratio = 0.0
            
        # Weighted blend
        score = (0.6 * cosine_similarities[idx]) + (0.4 * overlap_ratio)
        # Normalize to 0-100
        final_score = round(score * 100, 2)
        
        match_data = {
            "user_id": user_id,
            "job_id": job_id,
            "score": final_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        }
        
        try:
            supabase.table('match_scores').upsert(match_data, on_conflict='user_id,job_id').execute()
            match_results.append(match_data)
        except Exception as e:
            print(f"Failed to upsert match score for job {job_id}: {e}")
            
    return match_results
