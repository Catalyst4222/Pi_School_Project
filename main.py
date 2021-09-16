import csv

import barcode_reader

with open('names.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['name'], row['s_number'])
print(row)

StudentID = '100002'
#read csv, and split on "," the line
csv_file = csv.reader(open('names.csv', "r"), delimiter=",")

# lines = [line for line in csv_file]
# print(lines)

#loop through the csv list
for row in csv_file:
    #if current rows 2nd value is equal to input, print that row
    if StudentID == row[1]:
        print(row)
