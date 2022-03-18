import argparse

from data_grab.run_scraper import Scraper

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--proxy', help="use proxy", action='store_false')

args = parser.parse_args()

set_url = [
        "https://www.webstaurantstore.com/lorann-oils-hi-sweet-25-lb-powdered-corn-syrup/103LOR604525.html",
        "https://www.webstaurantstore.com/regal-large-raw-cashews-10-lb/999CARAWLG10.html",
        "https://www.webstaurantstore.com/richs-on-top-19-oz-soft-whip-pourable-sweet-cream-cold-foam-topping-case/711RICH09229.html"
        ]

if(len(set_url) > 0):
    scraper = Scraper()
    scraper.get_seller(set_url, False)