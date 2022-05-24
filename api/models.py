from pydantic import BaseModel

from typing import Mapping, Any, Union


class TriggerRequest(BaseModel):
    company_id: str
    scrape_id: str
    start_url: str
    ats_name: str
    params: Union[Mapping[str, Any], None]


class TriggerResponse(BaseModel):
    task_id: str = "12312312"
    message: str = "success"
