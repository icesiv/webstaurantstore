# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class DataGrabPipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("db/cars.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        # dealer_id,vin,title,price,stock_id,stock_type,mileage
        self.curr.execute("""DROP TABLE IF EXISTS sellers""")
        self.curr.execute("""CREATE TABLE `seller` (
              `seller_id` varchar(100) NOT NULL,
              `business_name` varchar(200) DEFAULT NULL,
              `first_name` varchar(100) DEFAULT NULL,
              `last_name` varchar(100) DEFAULT NULL,
              `address` varchar(254) DEFAULT NULL,
              `phone_number` varchar(200) DEFAULT NULL,
              `email` varchar(200) DEFAULT NULL,
              `country` varchar(100) DEFAULT NULL,
              `positive_feedback` int DEFAULT NULL,
              `feedback_score` int DEFAULT NULL,
              `catalog_size` int DEFAULT NULL,
              `categories` varchar(254) DEFAULT NULL,
              `seller_profile` varchar(200) DEFAULT NULL,
              `store_url` varchar(200) DEFAULT NULL,
              `inventory_link` varchar(200) DEFAULT NULL,
              `check_url` varchar(200) DEFAULT NULL,
              `created` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
              PRIMARY KEY (`seller_id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci""")



    def process_item(self, item, spider):
        self.store_in_db(item)
        print("Pipe >> " , item['title'])
        return item

    def store_in_db(self, item):
        self.curr.execute("""insert into cars_db values (?,?,?)""", (
            item['title'],
            item['vin'],
            item['price']
        ))
        self.conn.commit()

#             'catalog_size': '-',
#             'first_name': '-',
#             'last_name': '-',
#             'country': '-',
#             'categories': '-',
#             'store_url': '-',
