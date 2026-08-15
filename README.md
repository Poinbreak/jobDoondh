# JobDoondh (v1)

JobDoondh is an AI-powered job-matching assistant. Users can upload their resumes, define their skills and job goals, and receive matched job postings. The system scores resumes based on heuristics, ranks job postings using TF-IDF and keyword overlap, and uses AI (Anthropic Claude Haiku) to generate tailored cover letter pitches per job.

## Features (v1)

- **Resume Parsing & Scoring**: Upload PDF or DOCX resumes. The system automatically extracts text, performs basic skill extraction, and gives a rule-based score (0-100) based on length, required sections, action verb density, and quantified achievements.
- **Job Source Adapters**: Modular scraping architecture.
  - **Adzuna**: Integrates with the official Adzuna Jobs API for a stable initial job feed.
  - **Naukri**: Uses Playwright to scrape public Naukri search results.
- **Shared Job Cache**: Job scraping is done via a central orchestrated cron job running on GitHub Actions, rather than per-user. This prevents rate limits and reduces compute overhead.
- **Matching Engine**: Ranks all cached jobs against the user's extracted skills and resume content using `scikit-learn` TF-IDF Cosine Similarity (60% weight) and explicit keyword overlap (40% weight).
- **AI Pitch Generator**: Uses Anthropic's Claude 3 Haiku to generate short, tailored pitches (120-150 words) based on the user's resume and the specific job description. API calls are gated behind a hard daily quota (e.g., 5 per day) to control costs.
- **Frontend Dashboard**: A responsive Next.js frontend featuring:
  - Radar charts (via `recharts`) to visualize missing vs. matched skills.
  - Ranked job feed with match scores.
  - Resume upload and feedback visualization interface.

## Tech Stack

- **Backend**: Python 3.11+, FastAPI
- **Database / Auth**: Supabase (PostgreSQL, Supabase Auth)
- **Matching / Data Processing**: `scikit-learn`, `pdfplumber`, `python-docx`
- **Web Scraping**: Playwright
- **AI Integration**: Anthropic API (`claude-3-haiku-20240307`)
- **Frontend**: Next.js (React), Tailwind CSS, Recharts

## Project Structure

```text
├── .github/workflows/       # GitHub Actions (e.g., Cache refresh cron)
├── backend/
│   ├── app/
│   │   ├── auth/            # Supabase Auth middleware
│   │   ├── db/              # DB Client & SQL Migrations
│   │   ├── jobs/            # Job source adapters, scraping runner, and matching engine
│   │   ├── pitch/           # Claude API client, prompt templates, and quota enforcement
│   │   ├── resume_scorer/   # Rule-based heuristic scoring
│   │   ├── resumes/         # PDF/DOCX Parsing and upload routes
│   │   ├── skills/          # Manual skill entry endpoints
│   │   └── main.py          # FastAPI application entrypoint
│   ├── .env.example
│   └── requirements.txt
└── frontend/                # Next.js Application
    ├── app/                 # Next.js App Router pages (Dashboard, Jobs, Resume)
    ├── components/          # Shared React components (Layout)
    └── package.json
```

## Setup & Installation

### 1. Database Setup
1. Create a project on [Supabase](https://supabase.com/).
2. Run the SQL migration located at `backend/app/db/migrations/01_initial_schema.sql` in the Supabase SQL editor to create the tables.

### 2. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Copy the environment variables template and fill in your keys (Supabase, Anthropic, Adzuna):
   ```bash
   cp .env.example .env
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```
   *(Note for Windows users: You may need Microsoft Visual C++ Build Tools installed for `scikit-learn` to build successfully if a pre-compiled wheel isn't available for your architecture.)*
4. Run the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

### 3. Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. Open [http://localhost:3000](http://localhost:3000) to view the application.

## Automations

The repository includes a GitHub Action in `.github/workflows/refresh-cache.yml` that runs every 6 hours to trigger the backend's `/jobs/internal/refresh-cache` endpoint. 

To use this, deploy the backend to a provider like Render or Railway, and update the URL in the GitHub Action file to point to your live backend instance.

## Limitations (v1)
- Scraping is limited to public, non-authenticated pages to prevent account bans and IP blocks.
- Semantic embeddings-based matching (e.g., using `pgvector`) is out-of-scope for v1 and falls back to TF-IDF.
- No LinkedIn scraping module due to aggressive anti-bot protection. 
