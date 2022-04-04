# Scrapy hands-on project

## Installation

Create a virtual environment

```virtualenv venv```

Activate the virtual environment

```source venv/bin/activate```

Install all dependencies

```pip install -r requirements.txt```

## Run a spider

Go to the crawler project

```cd crawler```

Start crawling

```scrapy crawl {{spider_name}}```

## Steps to create a spider

Go to the crawler project

```cd crawler```

Create a spider for crawling the target project

```scrapy genspider {{spider_name}} {{target_domain_name}}```

The resulted spider will be located in: `{{project}}/spiders/{{spider_name}}.py`
