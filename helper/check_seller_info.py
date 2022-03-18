import csv
import sys

from tempfile import NamedTemporaryFile
import shutil

f1 = open("db/seller_id.csv", 'r')
f2 = open("db/seller_details.csv", 'r')
f3 = NamedTemporaryFile(delete=False, mode='w')

c1 = csv.reader(f1)
c2 = csv.reader(f2)
c3 = csv.writer(f3)

masterlist = list(c2)
matched = 0
total = 0

host_target_column = 0
host_prob_column = 1
master_column = 0

for hosts_row in c1:
    row = 1
    found = False

    for master_row in masterlist:
        results_row = hosts_row

        if hosts_row[host_target_column] == master_row[master_column]:
            found = True
            print(hosts_row[host_target_column])
            break
        
        row = row + 1

    if not found:
        try:
            results_row[host_prob_column] = '0'
        except IndexError:
            results_row.append('0')
    else:
        try:
            results_row[host_prob_column] = '1'
        except IndexError:
            results_row.append('1')
        matched += 1

    c3.writerow(results_row)
    total += 1

shutil.move(f3.name, f1.name)

print("Result : ", matched-1, "/", total-1)
