from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.db.client import supabase
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/skills", tags=["Skills"])

class SkillCreate(BaseModel):
    skill_name: str

@router.post("/")
def add_skill(
    skill: SkillCreate,
    user = Depends(get_current_user)
):
    """
    Add a manual skill.
    """
    skill_data = {
        "user_id": user.id,
        "skill_name": skill.skill_name.lower(),
        "source": "manual"
    }
    
    response = supabase.table('skills').insert(skill_data).execute()
    
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add skill"
        )
        
    return response.data[0]

@router.delete("/{skill_id}")
def delete_skill(
    skill_id: str,
    user = Depends(get_current_user)
):
    """
    Remove a skill. Ensure it belongs to the user.
    """
    # Delete skill where id = skill_id and user_id = user.id
    response = supabase.table('skills').delete().match({
        "id": skill_id,
        "user_id": user.id
    }).execute()
    
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found or you don't have permission to delete it"
        )
        
    return {"message": "Skill deleted successfully"}
