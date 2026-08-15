from datetime import datetime, timezone
from app.db.client import supabase
from app.config import settings

def check_and_increment_quota(user_id: str) -> bool:
    """
    Checks if user is under their daily pitch limit.
    If yes, increments usage and returns True. Otherwise False.
    """
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Count rows in api_usage for today
    resp = supabase.table('api_usage').select('id', count='exact').eq('user_id', user_id).eq('endpoint', 'pitch').gte('created_at', today_start.isoformat()).execute()
    
    usage_count = resp.count if resp.count is not None else 0
    
    if usage_count >= settings.daily_pitch_limit:
        return False
        
    # Increment quota by inserting a new row
    # Actual token counting will happen after the Claude call, so we insert 0 tokens for now, 
    # or just insert the row to represent 1 API call.
    usage_data = {
        "user_id": user_id,
        "endpoint": "pitch",
        "tokens_used": 0
    }
    supabase.table('api_usage').insert(usage_data).execute()
    
    return True

def get_current_usage(user_id: str) -> dict:
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    resp = supabase.table('api_usage').select('id', count='exact').eq('user_id', user_id).eq('endpoint', 'pitch').gte('created_at', today_start.isoformat()).execute()
    usage_count = resp.count if resp.count is not None else 0
    
    return {
        "used": usage_count,
        "limit": settings.daily_pitch_limit,
        "remaining": max(0, settings.daily_pitch_limit - usage_count)
    }
