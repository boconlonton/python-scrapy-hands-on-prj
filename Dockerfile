FROM python:3.8

RUN mkdir /scrapy-application

WORKDIR /scrapy-application

RUN apt-get update \
    && apt-get install -y git

RUN pip3 install virtualenv \
    && virtualenv venv \
    && . venv/bin/activate

RUN pip3 install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . /scrapy-application

WORKDIR /scrapy-application/crawler

CMD ["scrapyd-deploy", "default"]

CMD ["scrapyd"]