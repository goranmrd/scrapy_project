# -*- coding: utf-8 -*-
from ..items import PdfUrlsItem
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class PdfUrlSpider(CrawlSpider):
    name = 'pdf_url'
    allowed_domains = [
                'pdf995.com',
                 'kmmc.in',
                 'adobe.com',
                 'planetebook.com',
                 'ohchr.org',
                 'eforms.state.gov',
                 'eforms.state.gov',
                 'assets.publishing.service.gov.uk',
                 'papers.mathyvanhoef.com',
                 'apple.com'
                  ]

    start_urls = [
                 'http://www.pdf995.com',
                 'http://kmmc.in',
                 'https://www.adobe.com',
                 'https://www.planetebook.com',
                 'https://www.ohchr.org',
                 'https://eforms.state.gov',
                 'https://eforms.state.gov',
                 'https://assets.publishing.service.gov.uk',
                 'https://papers.mathyvanhoef.com',
                 'https://www.apple.com'
                  ]

    rules = (
        Rule(
                LinkExtractor(), callback="parse_httpbin", follow=True
            ),
    )

    def parse_httpbin(self, response):
        self.logger.info('Got successful response from {}'.format(response.url))
        # do something useful here...
        item = PdfUrlsItem()
        item["url"] = response.url
        print(response.headers["content-type"])
        if "Content-Disposition" in response.headers.keys() and "application/pdf" in str(response.headers["content-type"]):
            print("Content-Disposition is in header.")
            print(response.headers["Content-Disposition"])
            filename = re.findall("filename=(.+)", str(response.headers["Content-Disposition"]))[0]
            item["filename"] = filename
        elif "application/pdf" in str(response.headers["content-type"]):
            print("content-type")
            item["filename"] = response.url.split("/")[-1]
            print(response.url)
        else:
            print("No pdf file.")
            item["filename"] = "None"
        return item


