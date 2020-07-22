import collections
import csv
from selenium import webdriver

dictionary = collections.defaultdict(list)
i = 0
readFile = []
with open('out_url.csv', encoding="utf-8") as csvfile:
    readCSV = csv.reader(csvfile)
    for row in readCSV:
        if (row[0] != ''):
            i = i + 1
            dictionary[i].append(row[1])
        else:
            dictionary[i].append(row[1])
csvfile.close()

f = open('out_url.csv', encoding="utf-8")
reader = csv.reader(f)
readFile = list(reader)
f.close()

# filter for identical urls -> no duplicates
temp = []
for category in dictionary:
    for link in dictionary[category]:
        if (link not in temp):
            temp.append(link)
        else:
            print(category, link)
    temp = []

i = -1
for category in dictionary:
    print(category)
    tempURL = collections.defaultdict(list)
    for link in dictionary.get(category):
        i = i + 1
        driver = webdriver.Firefox()
        driver.get(link)
        if (driver.current_url != link):
            link = driver.current_url
            print((category, link))
            readFile[i].append(link)
            if (link[-4:] == '.pdf'):
                readFile[i].append('PDF')
                if (link not in tempURL.keys()):
                    tempURL[link].append(i)
                else:
                    readFile[i].append('Duplicate Redirect')
                    k = tempURL.get(link)
                    readFile[k].append('Duplicate Redirect')
                driver.close()
            else:
                readFile[i].append('Non PDF')
                driver.close()
        else:
            readFile[i].append('No Redirect')
            if (link[-4:] == '.pdf'):
                readFile[i].append('PDF')
                if (link not in tempURL.keys()):
                    tempURL[link].append(i)
                else:
                    readFile[i].append('Duplicate PDF')
                    k = tempURL.get(link)
                    readFile[k].append('Duplicate PDF')
                driver.close()
            else:
                readFile[i].append('Non PDF')
                driver.close()
    for url in tempURL:
        k = tempURL.get(url)[0]
        readFile[k].append(url)

with open('tagged.csv', "w", newline='', encoding="utf-8") as out_file:
    writeCSV = csv.writer(out_file)
    writeCSV.writerows(readFile)
out_file.close()
