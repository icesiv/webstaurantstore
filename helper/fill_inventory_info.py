import csv
import sys

from tempfile import NamedTemporaryFile
import shutil

# inventory_link,catalog_size,categories

f1 = open("db/output/ebay_seller_details.csv", 'r')
f2 = open("db/output/ebay_seller_inventory.csv", 'r')
f3 = NamedTemporaryFile(delete=False, mode='w')

c1 = csv.DictReader(f1)
c2 = csv.DictReader(f2)

fieldnames = [
    'seller_id',
    'catalog_size',
    'business_name',
    'first_name',
    'last_name',
    'address',
    'email',
    'country',
    'positive_feedback',
    'feedback_score',
    'categories',
    'seller_profile',
    'store_url',
    'inventory_link',
]
c3 = csv.DictWriter(f3, fieldnames=fieldnames)
c3.writeheader()


matched = 0
total = 0

for hosts_row in c1:
    results_row = hosts_row
    # results_row['inventory_link'] = results_row['inventory_link'].replace('http://','https://')

    if results_row['catalog_size'] == '-':
        for row in c2:
            if results_row['inventory_link'] == row['inventory_link']:
                results_row['catalog_size'] = row['catalog_size']
                results_row['categories'] = row['categories']
                matched += 1
                break

    c3.writerow(results_row)
    total += 1


print("Result : ", matched-1, "/", total-1)
shutil.move(f3.name, f1.name)

f1.close()
f2.close()
