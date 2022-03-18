# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

seller_id text,
catalog_size text,
business_name text,
first_name text,
last_name text,
address text,
phone_number text,
email text,
country text,
positive_feedback text,
feedback_score text,
categories text,
seller_profile text,
store_url text,
inventory_link text,


class SellerProfile(scrapy.Item):
    seller_id = scrapy.Field()
    catalog_size = scrapy.Field()
    business_name = scrapy.Field()
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    address = scrapy.Field()
    phone_number = scrapy.Field()
    email = scrapy.Field()
    country = scrapy.Field()
    positive_feedback = scrapy.Field()
    feedback_score = scrapy.Field()
    categories = scrapy.Field()
    seller_profile = scrapy.Field()
    store_url = scrapy.Field()
    inventory_link = scrapy.Field()
