from supabase import create_client, Client
from app.config import settings

# Since we might need admin access for some backend tasks, we use the service key
supabase: Client = create_client(settings.supabase_url, settings.supabase_service_key)
