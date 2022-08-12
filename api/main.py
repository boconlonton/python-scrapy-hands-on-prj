import os

import httpx

from fastapi import FastAPI


from fastapi import Depends

from models import TriggerRequest
from models import TriggerResponse

from custom_rss import CUSTOM_RSS

from authentication import api_key_auth


app = FastAPI()


@app.post("/api/v1/trigger",
          status_code=200,
          dependencies=[Depends(api_key_auth)],
          response_model=TriggerResponse)
async def trigger_spider(payload: TriggerRequest) -> dict:
    async with httpx.AsyncClient() as client:
        print(payload)
        print(os.getenv('SCRAPY_HOST'))
        print(os.getenv('SCRAPY_PROJECT'))
        print("main.py is here")
        if payload.ats_name == 'customrss':
            res = await client.post(
                url=f"{os.getenv('SCRAPY_HOST')}/schedule.json",
                data={
                    'project': os.getenv('SCRAPY_PROJECT'),
                    'spider': CUSTOM_RSS.get(
                        f'{payload.company_id}-{payload.scrape_id}'
                    ),
                    'company_id': payload.company_id,
                    'scrape_id': payload.scrape_id,
                    'start_url': payload.start_url,
                    'ats_name': payload.ats_name,
                    **payload.params,
                }
            )
        else:
            res = await client.post(
                url=f"{os.getenv('SCRAPY_HOST')}/schedule.json",
                data={
                    'project': os.getenv('SCRAPY_PROJECT'),
                    'spider': payload.ats_name,
                    'company_id': payload.company_id,
                    'scrape_id': payload.scrape_id,
                    'start_url': payload.start_url,
                    'ats_name': payload.ats_name,
                    **payload.params,
                }
            )
    return {
        'task_id': res.json().get('jobid'),
        'message': 'success'
    }
