import urllib.request
from PyPDF2 import PdfFileReader
import csv
import json
f=open("urls.txt","r")
x=[i.split("\n")[0] for i in f.readlines()]
files=open('innovators.csv', 'a', newline='')
writer = csv.writer(files)
count=0
for i in x:
   count+=1
   if (count%200==0):
    print(count)
   try:
       urllib.request.urlretrieve(i, "filename.pdf")
       pdf_toread = PdfFileReader(open("filename.pdf", "rb"))
       pdf_info = pdf_toread.getDocumentInfo()
       writer.writerow([i,pdf_info])
   except Exception as e:
       print(e)