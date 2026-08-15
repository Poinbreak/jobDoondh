import re
from typing import Dict, Any

ACTION_VERBS = {
    "achieved", "improved", "trained", "managed", "resolved",
    "created", "developed", "led", "increased", "decreased",
    "designed", "implemented", "launched", "optimized", "spearheaded"
}

def score_resume(parsed_text: str) -> Dict[str, Any]:
    score = 0
    feedback = []
    
    text_lower = parsed_text.lower()
    words = text_lower.split()
    word_count = len(words)
    
    # 1. Length Check (20 points max)
    if 300 <= word_count <= 800:
        score += 20
        feedback.append("Good resume length (300-800 words).")
    elif word_count < 300:
        score += 10
        feedback.append("Resume is a bit short. Try to add more details about your experience.")
    else:
        score += 10
        feedback.append("Resume is quite long. Consider condensing it to highlight key achievements.")
        
    # 2. Required Sections (20 points max, 5 each)
    sections = {
        "education": ["education", "academic"],
        "experience": ["experience", "employment", "work history"],
        "skills": ["skills", "technologies", "core competencies"],
        "projects": ["projects", "personal projects"]
    }
    
    section_score = 0
    missing_sections = []
    for sec, keywords in sections.items():
        found = any(kw in text_lower for kw in keywords)
        if found:
            section_score += 5
        else:
            missing_sections.append(sec)
            
    score += section_score
    if not missing_sections:
        feedback.append("All core sections (Education, Experience, Skills, Projects) are present.")
    else:
        feedback.append(f"Consider adding missing sections: {', '.join(missing_sections).title()}.")
        
    # 3. Action Verb Density (20 points max)
    verb_count = sum(1 for word in words if word in ACTION_VERBS)
    verb_density = verb_count / word_count if word_count > 0 else 0
    
    if verb_density > 0.02:
        score += 20
        feedback.append("Strong use of action verbs.")
    elif verb_density > 0.01:
        score += 10
        feedback.append("Good use of action verbs, but could use more impactful words.")
    else:
        score += 5
        feedback.append("Try starting bullet points with strong action verbs (e.g., Achieved, Developed).")
        
    # 4. Quantified Achievements (20 points max)
    # Looking for % or $ or numbers near action verbs
    quantified_matches = re.findall(r'(\d+%|\$\d+|\d+\s*(?:users|clients|revenue|sales))', text_lower)
    if len(quantified_matches) >= 3:
        score += 20
        feedback.append("Excellent use of quantified achievements (numbers, metrics).")
    elif len(quantified_matches) > 0:
        score += 10
        feedback.append("Some quantified achievements found. Try to add more numbers to prove your impact.")
    else:
        score += 0
        feedback.append("No quantified achievements found. Use numbers and metrics to show impact.")

    # 5. Formatting / Bullet structure (20 points max)
    lines = parsed_text.split('\n')
    bullet_lines = [l for l in lines if l.strip().startswith(('-', '•', '*'))]
    if len(bullet_lines) >= 5:
        score += 20
        feedback.append("Good use of bullet points for readability.")
    else:
        score += 10
        feedback.append("Consider using more bullet points to make the resume easier to read.")
        
    return {
        "score": score,
        "feedback": feedback
    }
