import requests
from typing import List
from app.jobs.adapters.base import JobSourceAdapter, RawJobPosting
from app.config import settings
import urllib.parse

class AdzunaAdapter(JobSourceAdapter):
    SOURCE_NAME = "adzuna"
    BASE_URL = "https://api.adzuna.com/v1/api/jobs"

    def fetch_listings(self, query: str, location: str, limit: int = 50) -> List[RawJobPosting]:
        if not settings.adzuna_app_id or not settings.adzuna_app_key:
            print("Adzuna credentials not configured. Skipping.")
            return []

        # Adzuna API is specific to a country, we'll hardcode India ('in') as requested
        country = "in"
        url = f"{self.BASE_URL}/{country}/search/1"
        
        params = {
            "app_id": settings.adzuna_app_id,
            "app_key": settings.adzuna_app_key,
            "results_per_page": limit,
            "what": query,
            "where": location,
            "content-type": "application/json"
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            jobs = []
            for item in data.get("results", []):
                company_name = item.get("company", {}).get("display_name")
                location_name = item.get("location", {}).get("display_name")
                
                jobs.append(
                    RawJobPosting(
                        source=self.SOURCE_NAME,
                        source_job_id=str(item.get("id")),
                        title=item.get("title", ""),
                        company=company_name,
                        location=location_name,
                        description=item.get("description", ""),
                        url=item.get("redirect_url", ""),
                        posted_at=item.get("created")
                    )
                )
            return jobs
        except Exception as e:
            print(f"Error fetching from Adzuna: {e}")
            return []
