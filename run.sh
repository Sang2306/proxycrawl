#!/usr/bin/env bash

source ./venv/bin/activate

cd ./crawl

scrapy crawl proxy_crawler
