from typing import List
from app.jobs.adapters.base import JobSourceAdapter, RawJobPosting

class UnstopAdapter(JobSourceAdapter):
    SOURCE_NAME = "unstop"

    def fetch_listings(self, query: str, location: str, limit: int = 50) -> List[RawJobPosting]:
        # Stubbed for v1 as requested
        print("Unstop adapter is stubbed in v1.")
        return []
