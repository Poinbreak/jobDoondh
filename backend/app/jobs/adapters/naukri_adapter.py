from typing import List
from playwright.sync_api import sync_playwright
import time
import urllib.parse
from app.jobs.adapters.base import JobSourceAdapter, RawJobPosting

class NaukriAdapter(JobSourceAdapter):
    SOURCE_NAME = "naukri"
    BASE_URL = "https://www.naukri.com"

    def fetch_listings(self, query: str, location: str, limit: int = 50) -> List[RawJobPosting]:
        jobs = []
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Format URL: https://www.naukri.com/software-engineer-jobs-in-bangalore
                formatted_query = query.replace(' ', '-')
                formatted_location = location.replace(' ', '-')
                search_url = f"{self.BASE_URL}/{formatted_query}-jobs-in-{formatted_location}"
                
                page.goto(search_url, wait_until="domcontentloaded")
                time.sleep(3) # Wait for JS rendering
                
                job_cards = page.locator("div.srp-jobtuple-wrapper").all()
                
                for idx, card in enumerate(job_cards):
                    if idx >= limit:
                        break
                        
                    try:
                        title_el = card.locator("a.title")
                        title = title_el.inner_text().strip()
                        url = title_el.get_attribute("href")
                        
                        company = card.locator("a.comp-name").first.inner_text().strip()
                        location_text = card.locator("span.locWdth").inner_text().strip()
                        
                        # In a real scraper, we might need to navigate to the job page for the full description
                        # For v1, we just extract whatever short description is on the card
                        desc_el = card.locator("span.job-desc")
                        description = desc_el.inner_text().strip() if desc_el.count() > 0 else ""
                        
                        source_job_id = url.split('-')[-1] if url else f"naukri-{idx}"
                        
                        jobs.append(
                            RawJobPosting(
                                source=self.SOURCE_NAME,
                                source_job_id=source_job_id,
                                title=title,
                                company=company,
                                location=location_text,
                                description=description,
                                url=url if url.startswith('http') else f"https:{url}"
                            )
                        )
                    except Exception as card_error:
                        print(f"Error parsing Naukri card: {card_error}")
                        
                browser.close()
        except Exception as e:
            print(f"Error scraping Naukri: {e}")
            
        return jobs
