# image-crawler-cli
# Description
image-crawler-cli is a command line program that helps in scraping web pages for images and do it recursively as per the depth specified.

# Installation
This is a python script, and requires python3 interpreter to be installed and some packages.
To install the required packages, make use of the requirements.txt file
Run the following command:

`pip3 install -r requirements.txt`


tqdm==4.60.0 # for progressbar
requests==2.25.1 # for making http requests
beautifulsoup4==4.9.3 # for scraping the data

# Project structure

crawl.py - It is the entry point of the program
util.scraping_utils.py - Contains all the functions related to web scraping, making network calls
util.helpers.py - Contains some helper functions for outputting the formatted data and for validation

# Usage
usage: python3 crawler.py base_url depth

crawl specified webpages

positional arguments:
  base_url             Start url
  depth                depth for crawling recursively

optional arguments:
  -h, --help       show this help message and exit

Eg: python3 crawl.py https://abcd.com 0


