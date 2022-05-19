# Scrapy hands-on project

## Components

- API
- Web Crawler

## How to use

### Prerequisites

- Docker
- docker-compose

### Run

`docker-compose up --build`

## Test

```
curl --location --request POST 'http://localhost:8000/trigger' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer 2f927842-de67-43ae-93cc-41716e01964b' \
--data-raw '{
    "company_id": 158230,
    "scrape_id": 53289,
    "start_url": "https://careers.lids.com/feed/357900",
    "ats_name": "customrss",
    "params": {
        "parent_node": "job",
        "rid": "ID"
    }
}'
```

## Local Environment Setup

Clone the repository

`git clone https://github.com/boconlonton/python-scrapy-hands-on-prj.git`

Activate the virtual environment

`cd python-scrapy-hands-on-prj && virtualenv venv && source venv/bin/activate`

Install dependencies

`pip install -r crawler/requirements.txt`

Install precommit

`pre-commit install`
