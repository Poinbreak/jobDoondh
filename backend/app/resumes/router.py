from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from typing import List
from app.db.client import supabase
from app.auth.dependencies import get_current_user
from app.resumes.parser import parse_pdf, parse_docx, extract_skills_from_text

router = APIRouter(prefix="/resumes", tags=["Resumes"])

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    user = Depends(get_current_user)
):
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and DOCX files are supported"
        )
        
    contents = await file.read()
    
    if file.filename.endswith('.pdf'):
        parsed_text = parse_pdf(contents)
    else:
        parsed_text = parse_docx(contents)
        
    if not parsed_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not extract text from the provided file"
        )
        
    # Extracted skills from the resume text
    extracted_skills = extract_skills_from_text(parsed_text)
    
    # In a real app, upload file_bytes to Supabase Storage and get the public URL
    # For now, we mock the file_url since storage wasn't fully specified
    file_url = f"https://mock-storage.com/{user.id}/{file.filename}"
    
    # Save the resume to DB
    resume_data = {
        "user_id": user.id,
        "file_url": file_url,
        "parsed_text": parsed_text
    }
    resume_response = supabase.table('resumes').insert(resume_data).execute()
    
    if not resume_response.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save resume"
        )
        
    resume_id = resume_response.data[0]['id']
    
    # Save extracted skills to DB
    skills_data = [
        {
            "user_id": user.id,
            "skill_name": skill,
            "source": "resume"
        }
        for skill in extracted_skills
    ]
    if skills_data:
        supabase.table('skills').insert(skills_data).execute()

    return {
        "message": "Resume uploaded and parsed successfully",
        "resume_id": resume_id,
        "extracted_skills": extracted_skills
    }

from app.resume_scorer.scorer import score_resume

@router.get("/{resume_id}/score")
def get_resume_score(
    resume_id: str,
    user = Depends(get_current_user)
):
    """
    Get the rule-based score for a resume.
    """
    # 1. Check if score already exists
    score_resp = supabase.table('resume_scores').select('*').eq('resume_id', resume_id).execute()
    if score_resp.data:
        return score_resp.data[0]
        
    # 2. Fetch the resume
    resume_resp = supabase.table('resumes').select('parsed_text, user_id').eq('id', resume_id).execute()
    if not resume_resp.data:
        raise HTTPException(status_code=404, detail="Resume not found")
        
    resume = resume_resp.data[0]
    if resume['user_id'] != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to score this resume")
        
    # 3. Compute score
    parsed_text = resume.get('parsed_text', '')
    if not parsed_text:
        raise HTTPException(status_code=400, detail="No parsed text found for this resume")
        
    scoring_result = score_resume(parsed_text)
    
    # 4. Save score
    score_data = {
        "resume_id": resume_id,
        "score": scoring_result["score"],
        "feedback": scoring_result["feedback"]
    }
    
    insert_resp = supabase.table('resume_scores').insert(score_data).execute()
    if not insert_resp.data:
        raise HTTPException(status_code=500, detail="Failed to save resume score")
        
    return insert_resp.data[0]
