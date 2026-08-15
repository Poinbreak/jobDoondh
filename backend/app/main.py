from fastapi import FastAPI, Depends
from app.auth.dependencies import get_current_user
from app.jobs.router import router as jobs_router
from app.resumes.router import router as resumes_router
from app.skills.router import router as skills_router
from app.pitch.router import router as pitch_router

app = FastAPI(title="Jobfinder v1 API")

app.include_router(jobs_router)
app.include_router(resumes_router)
app.include_router(skills_router)
app.include_router(pitch_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/profile")
def get_profile(user = Depends(get_current_user)):
    return {"message": "Profile data", "user_id": user.id}

# Additional routes will be added in subsequent phases
