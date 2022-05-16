FROM python:3.8-alpine

RUN mkdir /scrapy-application

WORKDIR /scrapy-application

RUN apk add --update \
gcc \
musl-dev \
libffi-dev \
libxml2-dev \
libxslt-dev \
openssl-dev

RUN pip3 install --upgrade pip

COPY ./requirements.txt requirements.txt

RUN python3 -m venv venv \
&& . ./venv/bin/activate

RUN pip3 install -r requirements.txt

COPY . /scrapy-application

WORKDIR /scrapy-application

CMD ["scrapyd-deploy", "crawler"]
