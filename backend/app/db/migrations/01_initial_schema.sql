create extension if not exists vector;

create table profiles (
  user_id uuid primary key references auth.users(id),
  full_name text,
  target_role text,
  target_location text,
  seniority text,
  created_at timestamptz default now()
);

create table skills (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id),
  skill_name text not null,
  source text check (source in ('manual','resume')),
  created_at timestamptz default now()
);

create table certificates (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id),
  name text not null,
  issuer text,
  issue_date date,
  file_url text,
  created_at timestamptz default now()
);

create table resumes (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id),
  file_url text not null,
  parsed_text text,
  uploaded_at timestamptz default now()
);

create table job_postings (
  id uuid primary key default gen_random_uuid(),
  source text not null,              -- 'naukri' | 'adzuna' | 'unstop'
  source_job_id text not null,
  title text not null,
  company text,
  location text,
  description text,
  url text,
  posted_at timestamptz,
  scraped_at timestamptz default now(),
  extracted_skills text[],
  embedding vector(384),             -- reserved for v2, nullable in v1
  unique(source, source_job_id)
);

create table match_scores (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id),
  job_id uuid references job_postings(id),
  score numeric not null,
  matched_skills text[],
  missing_skills text[],
  computed_at timestamptz default now(),
  unique(user_id, job_id)
);

create table resume_scores (
  id uuid primary key default gen_random_uuid(),
  resume_id uuid references resumes(id),
  score numeric not null,
  feedback jsonb,
  computed_at timestamptz default now()
);

create table pitch_drafts (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id),
  job_id uuid references job_postings(id),
  content text not null,
  created_at timestamptz default now()
);

create table api_usage (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id),
  endpoint text not null,
  tokens_used int,
  created_at timestamptz default now()
);
