from fastapi import APIRouter, Depends, HTTPException, status
from app.db.client import supabase
from app.auth.dependencies import get_current_user
from app.pitch.quota import check_and_increment_quota, get_current_usage
from app.pitch.claude_client import generate_pitch

router = APIRouter(prefix="/pitch", tags=["Pitch"])

@router.get("/usage")
def get_usage(user = Depends(get_current_user)):
    """
    Get current quota status for the user.
    """
    return get_current_usage(user.id)

@router.post("/jobs/{job_id}")
def create_pitch(
    job_id: str,
    user = Depends(get_current_user)
):
    """
    Generate an AI pitch for a specific job, subject to daily quota.
    """
    if not check_and_increment_quota(user.id):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Daily pitch limit reached. Please try again tomorrow."
        )
        
    # Fetch user's latest resume
    resumes_resp = supabase.table('resumes').select('parsed_text').eq('user_id', user.id).order('uploaded_at', desc=True).limit(1).execute()
    if not resumes_resp.data:
        raise HTTPException(status_code=400, detail="Please upload a resume first.")
    resume_summary = resumes_resp.data[0]['parsed_text'][:2000] # Pass first 2k chars as summary
    
    # Fetch job details
    job_resp = supabase.table('job_postings').select('title, description').eq('id', job_id).execute()
    if not job_resp.data:
        raise HTTPException(status_code=404, detail="Job not found.")
    job_title = job_resp.data[0]['title']
    job_description = job_resp.data[0]['description']
    
    # Call Claude
    pitch_content = generate_pitch(resume_summary, job_title, job_description)
    
    # Save draft
    draft_data = {
        "user_id": user.id,
        "job_id": job_id,
        "content": pitch_content
    }
    
    insert_resp = supabase.table('pitch_drafts').insert(draft_data).execute()
    
    if not insert_resp.data:
        # We might want to handle this gracefully, but for now just return the content
        pass
        
    return {
        "message": "Pitch generated successfully",
        "content": pitch_content
    }
