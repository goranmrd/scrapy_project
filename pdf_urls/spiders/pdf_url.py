# -*- coding: utf-8 -*-
import scrapy
from ..items import PdfUrlsItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
import re


class PdfUrlSpider(scrapy.Spider):
    name = 'pdf_url'
    allowed_domains = ['goranlazarevski.com']
    start_urls = [
        'http://www.pdf995.com/samples/pdf.pdf', 'http://kmmc.in/wp-content/uploads/2014/01/lesson2.pdf',
        'https://www.adobe.com/content/dam/acom/en/products/acrobat/pdfs/adobe-acrobat-xi-protect-pdf-file-with-permissions-tutorial-ue.pdf',
        'https://www.planetebook.com/free-ebooks/the-great-gatsby.pdf',
        'https://www.ohchr.org/EN/UDHR/Documents/UDHR_Translations/eng.pdf', 'https://eforms.state.gov/Forms/ds11.pdf',
        'https://eforms.state.gov/Forms/ds5504.PDF',
        'https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/793360/Online_Harms_White_Paper.pdf',
        'https://papers.mathyvanhoef.com/dragonblood.pdf',
        'https://www.apple.com/mac/docs/Apple_T2_Security_Chip_Overview.pdf'
    ]

    def start_requests(self):

        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_httpbin,
                                 errback=self.errback_httpbin,
                                 dont_filter=True)

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
        yield item

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

