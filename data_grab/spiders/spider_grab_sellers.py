import scrapy
import os

from datetime import datetime
from helper.utils import clean_result, safe_split
from w3lib.html import remove_tags

# from scrapy.shell import inspect_response

class GrabSeller(scrapy.Spider):
    name = 'GrabSeller'
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

        item['seller_id'] = (response.url).replace('https://www.ebay.co.uk/usr/', '')
        item['catalog_size'] = '-'

        addtess_block = response.css(".ovly_upnl")
        addtess_rows = addtess_block.css(".bsi_row")

        for row in addtess_rows:
            row_id = row.css(".bsi_cell_label::attr(id)").extract_first()

            if(row_id == 'address'):
                item[row_id] = clean_result(
                    row.css(".bsi_cell_value").extract_first(), [])
            elif (row_id == 'business_name') or (row_id == 'first_name') or (row_id == 'last_name') or (row_id == 'phone_number') or (row_id == 'email') or (row_id == 'fax_number'):
                item[row_id] = row.css(
                    ".bsi_cell_value::text").extract_first()

        item['country'] = response.css('.mem_loc::text').extract_first()


        item['positive_feedback'] = clean_result(response.css('.perctg').extract_first(), ["positive", "Feedback"])
        item['feedback_score'] = response.css('.mbg-id+ a::text').extract_first()
        
        item['categories'] = '-'
        
        item['seller_profile'] = response.url
        item['store_url'] = response.css(".store_lk a::attr(href)").extract_first()
        
        item['inventory_link'] = response.css(".soi_lk a::attr(href)").extract_first()
        
        if(item['inventory_link']==None):
            item['inventory_link'] = '-'
            item['catalog_size'] = '-'
            item['categories'] = '-'
            now = datetime.now()
        
            print(now.strftime("%H:%M:%S"),">>", item['seller_id'])
            yield item
        else:
            item['inventory_link'] = item['inventory_link'].replace('http:','https:')

            request = scrapy.Request(item['inventory_link'],
                                callback=self.parse_inventory,
                                cb_kwargs=dict(item=item))
            yield request
        
    def parse_inventory(self, response, item):
        now = datetime.now()
        print(now.strftime("%H:%M:%S"),">>",item['seller_id'])

        item['inventory_link'] = response.url
        item['catalog_size'] = response.css('.rcnt::text').extract()
        item['categories'] = response.css('.cat-t a::text').extract()

        yield item
