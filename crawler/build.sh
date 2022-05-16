#!/bin/bash

docker build -t paradox/scrapy .
docker container run -p 6800:6800 --rm --name scrapy-demo paradox/scrapy