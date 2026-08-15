from typing import List
from app.db.client import supabase
from app.jobs.adapters.base import RawJobPosting
from app.jobs.adapters.adzuna_adapter import AdzunaAdapter
from app.jobs.adapters.unstop_adapter import UnstopAdapter
from app.jobs.adapters.naukri_adapter import NaukriAdapter

def get_enabled_adapters():
    return [
        AdzunaAdapter(),
        NaukriAdapter(),
        UnstopAdapter(),
    ]

def run_scrapers():
    """
    Orchestrates job scraping across all enabled adapters and upserts results.
    """
    adapters = get_enabled_adapters()
    all_jobs: List[RawJobPosting] = []

    # Hardcoded queries for the shared cache as per specs
    queries = ["software engineer", "data scientist", "product manager"]
    locations = ["india", "bangalore", "remote"]

    for adapter in adapters:
        adapter_jobs = []
        try:
            for query in queries:
                for location in locations:
                    # In a real scenario we'd respect rate limits here
                    jobs = adapter.fetch_listings(query=query, location=location, limit=50)
                    adapter_jobs.extend(jobs)
                    
            print(f"Adapter {adapter.SOURCE_NAME} returned {len(adapter_jobs)} results.")
            if len(adapter_jobs) == 0:
                print(f"WARNING: Adapter {adapter.SOURCE_NAME} returned 0 results. Possible breakage.")
            
            all_jobs.extend(adapter_jobs)
        except Exception as e:
            print(f"Adapter {adapter.SOURCE_NAME} failed: {e}")

    # Upsert to database
    upserted_count = 0
    for job in all_jobs:
        job_data = job.model_dump()
        try:
            # using upsert on (source, source_job_id) - assuming Supabase handles unique constraint correctly
            response = supabase.table('job_postings').upsert(
                job_data,
                on_conflict='source,source_job_id'
            ).execute()
            upserted_count += 1
        except Exception as e:
            print(f"Failed to upsert job {job.source_job_id}: {e}")
            
    print(f"Scrape completed. Upserted {upserted_count} jobs.")
    return upserted_count
