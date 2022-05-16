from pydantic import BaseModel

from typing import Mapping


class TriggerModel(BaseModel):
    company_id: int
    scrape_id: int
    start_url: str
    ats_name: str
    params: Mapping[str, str]
