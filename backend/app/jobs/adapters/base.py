from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel

class RawJobPosting(BaseModel):
    source: str
    source_job_id: str
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    description: str
    url: str
    posted_at: Optional[str] = None

class JobSourceAdapter(ABC):
    @abstractmethod
    def fetch_listings(self, query: str, location: str, limit: int = 50) -> List[RawJobPosting]:
        ...
