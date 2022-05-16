import os

import httpx

from fastapi import FastAPI

from models import TriggerModel


app = FastAPI()


@app.post("/trigger", status_code=201)
def trigger_spider(payload: TriggerModel):
    res = httpx.post(
        url=f"{os.getenv('SCRAPY_HOST')}/schedule.json",
        data={
            'project': os.getenv('SCRAPY_PROJECT'),
            'spider': payload.ats_name,
            'params': {
                'company_id': payload.company_id,
                'scrape_id': payload.scrape_id,
                **payload.params
            }
        }
    )
    return {
        'task_id': res.json().get('task_id'),
    }
