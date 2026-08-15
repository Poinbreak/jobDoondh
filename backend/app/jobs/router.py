from fastapi import APIRouter, Depends, Query, BackgroundTasks
from typing import List, Optional
from app.db.client import supabase
from app.jobs.scraper_runner import run_scrapers
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.get("/")
def get_jobs(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    # Optional filtering
    title: Optional[str] = None,
    location: Optional[str] = None,
):
    """
    Paginated cached listings, filterable.
    """
    query = supabase.table('job_postings').select('*')
    if title:
        query = query.ilike('title', f'%{title}%')
    if location:
        query = query.ilike('location', f'%{location}%')
        
    query = query.order('posted_at', desc=True).range(offset, offset + limit - 1)
    
    response = query.execute()
    return response.data

@router.post("/internal/refresh-cache")
def refresh_cache(background_tasks: BackgroundTasks):
    """
    Called only by GitHub Actions cron, triggers scraper_runner in the background.
    """
    # In a real app, we'd secure this endpoint with a secret token from GH Actions
    background_tasks.add_task(run_scrapers)
    return {"message": "Cache refresh triggered"}

from app.jobs.matching import compute_match_scores

@router.post("/refresh")
def refresh_matching(user = Depends(get_current_user)):
    """
    User-triggered re-run of matching against the existing cache.
    Rate-limiting to 1 call/minute/user should be implemented in middleware.
    """
    results = compute_match_scores(user.id)
    return {"message": f"Matching refreshed for {len(results)} jobs"}

@router.get("/best")
def get_best_matches(
    limit: int = Query(20, ge=1, le=50),
    user = Depends(get_current_user)
):
    """
    Ranked feed for the current user based on match_scores.
    """
    response = supabase.table('match_scores').select('*, job_postings(*)').eq('user_id', user.id).order('score', desc=True).limit(limit).execute()
    return response.data

@router.get("/{job_id}/match")
def get_job_match(
    job_id: str,
    user = Depends(get_current_user)
):
    """
    Score breakdown for one job.
    """
    response = supabase.table('match_scores').select('*').eq('user_id', user.id).eq('job_id', job_id).execute()
    if not response.data:
        return {"message": "No match score computed yet."}
    return response.data[0]
