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

``curl -X 'POST' \
  'http://localhost:8000/trigger' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "company_id": {COMPANY_ID},
  "scrape_id": {SCRAPE_ID},
  "start_url": {START_URL},
  "ats_name": {ATS_NAME},
  "params": {
    "parent_node": "job",
    "title": "title",
    "rid": "referencenumber"
  }
}'``