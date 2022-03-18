import scrapy
import re
import os

from datetime import datetime
from helper.utils import clean_result, safe_split
from w3lib.html import remove_tags

# from scrapy.shell import inspect_response

class GrabSellerID(scrapy.Spider):
    name = 'GrabSellerID'
    start_urls = []
    brand = {}

    looked = 0
    found = 0

    current_page = 0
    max_page = 100

    custom_settings = {
        'LOG_LEVEL': 'ERROR',  # CRITICAL, ERROR, WARNING, INFO, DEBUG
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
        },

        'DOWNLOAD_DELAY': 5,
        'CONCURRENT_REQUESTS_PER_DOMAIN' : 3,
        # CONCURRENT_REQUESTS_PER_IP = 2
    }

    def parse(self, response):
        list_item = response.css(".s-item   ")

        for items in list_item:
            details_link = items.css(
                '.s-item__link::attr(href)').extract_first()

            o = os.path.dirname(details_link)
            details_link = "https://www.ebay.co.uk/itm" + \
                details_link.replace(o, '').split("?")[0]
            yield scrapy.Request(url=details_link, callback=self.parse_details)

        # follow pagination link
        nav_btn_urls = response.css('.ebayui-pagination__control')

        for nb in nav_btn_urls:
            btn_text = nb.css('a::attr(rel)').extract_first()

            if btn_text == "next":
                next_page_url = nb.css('a::attr(href)').extract_first()
                next_page_url = response.urljoin(next_page_url)

                self.current_page += 1

                if(self.current_page < self.max_page):
                    yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_details(self, response):
        is_info_present = response.css('.bsi-cnt').extract_first()
        self.looked += 1

        seller_id = clean_result(
            response.css('.mbg-nw').extract_first(), [])
        positive_feedback = clean_result(response.css(
            '#si-fb').extract_first(), ["Positive Feedback"])
        feedback_score = clean_result(
            response.css('.mbg-l a').extract_first(), [])

        if is_info_present:
            self.found += 1

            now = datetime.now()

            print(now.strftime("%H:%M:%S"),">>", self.found, "/", self.looked)

            name = clean_result(response.css('.bsi-bn').extract_first(), [])
            address = clean_result(response.css(
                '.bsi-cic').extract_first(), ["Complete information"], False)

            d = response.css('.bsi-c2').extract_first()
            d = remove_tags(d)
            d = d.strip()
            d = d[::-1]
            d = d.replace('Phone:', '').replace(
                'Email:', '').replace('Fax:', '')

            contacts = d.splitlines()

            phone = []
            email = []

            for c in contacts:
                c = c.strip()
                if "@" in c:
                    email.append(c)
                else:
                    phone.append("'" + c)



            item = {
                'brand_name': self.brand['name'],
                'page_number': self.current_page,
                'seller_id': seller_id,
                'business_name': name,
                'address': address,
                'phone_number': phone,
                'email': email,
                'positive_feedback': positive_feedback,
                'feedback_score': feedback_score,
                'seller_profile': 'https://www.ebay.co.uk/usr/' + seller_id,
                'inventory_link': 'https://www.ebay.co.uk/sch/' + seller_id + '/m.html?_nkw=&_armrs=1&_ipg=&_from=',
                'check_url': response.url,
            }
        else:
            item = {
                'brand_name': self.brand['name'],
                'page_number': self.current_page,
                'seller_id': seller_id,
                'business_name': '-',
                'address': '-',
                'phone_number': '-',
                'email': '-',
                'positive_feedback': positive_feedback,
                'feedback_score': feedback_score,
                'seller_profile': 'https://www.ebay.co.uk/usr/' + seller_id,
                'inventory_link': 'https://www.ebay.co.uk/sch/' + seller_id + '/m.html?_nkw=&_armrs=1&_ipg=&_from=',
                'check_url': response.url,
            }

        yield item
