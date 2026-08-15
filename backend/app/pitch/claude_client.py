import anthropic
from app.config import settings
from app.pitch.templates import PITCH_PROMPT

# Singleton client
client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

def generate_pitch(resume_summary: str, job_title: str, job_description: str) -> str:
    if not settings.anthropic_api_key:
        return "AI Pitch generation is currently disabled due to missing API key."
        
    prompt = PITCH_PROMPT.format(
        resume_summary=resume_summary,
        job_title=job_title,
        job_description=job_description
    )
    
    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=300,
            temperature=0.7,
            system="You are a helpful career assistant.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    except Exception as e:
        print(f"Error calling Claude: {e}")
        return f"Error generating pitch: {str(e)}"
