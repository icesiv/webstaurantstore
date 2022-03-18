import os
import datetime

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from helper.get_proxy import refresh_proxy

from data_grab.spiders.spider_grab_item import GrabItem

class Scraper:
    def __init__(self):
        settings_file_path = 'data_grab.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.process = CrawlerProcess(get_project_settings())

    def get_seller(self, s_urls, is_proxy_on):
        spider = GrabItem
        today = datetime.date.today()
        spider.custom_settings['FEED_URI'] = 'db/' + \
            today.strftime("%d_%m_%Y") + '.csv'

        if is_proxy_on:
            refresh_proxy()
            spider.custom_settings['DOWNLOADER_MIDDLEWARES'].update({
                'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
                'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
            })


        spider.start_urls = s_urls

        self.spiders = GrabItem
        self.process.crawl(self.spiders)
        self.process.start()  # the script will block here until the crawling is finished
