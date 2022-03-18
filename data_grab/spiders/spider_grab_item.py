import scrapy
import re

from datetime import datetime
from helper.utils import clean_result, safe_split
from w3lib.html import remove_tags

# from scrapy.shell import inspect_response

class GrabItem(scrapy.Spider):
    name = 'GrabItem'
    start_urls = []

    custom_settings = {
        'LOG_LEVEL': 'ERROR',  # CRITICAL, ERROR, WARNING, INFO, DEBUG
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
        },

        'DOWNLOAD_DELAY': 3,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 3,
        # CONCURRENT_REQUESTS_PER_IP = 2
    }

    def parse(self, response):
        item = dict()

        # item['item_title'] = response.css('#page-header-description::text').extract_first()

        now = datetime.now()
        print(now.strftime("%H:%M:%S"),">>")

        # item['inventory_link'] = response.url
        single_price = response.css('#priceBox td::text').extract_first()

        if single_price == None:
            item['single_price'] =  response.css('.price::text').extract_first()
            item['discount_price'] = "-"
            item['quantity_discount'] = "-"
        else:    
            item['single_price'] = single_price
            item['discount_price'] = response.css('.price::text').extract_first()

            quantity_discount_txt = response.css('#priceBox label::text').extract_first()
            x = re.findall("[1-9]", quantity_discount_txt)
            item['quantity_discount'] = int (x[0]) + 1 

        # item['stock_out'] = response.css('#priceBox label::text').extract()
        item['shipping'] = response.css('#priceBox .plus-text::text').extract()

        print ( item )
        yield item
