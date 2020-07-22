import collections
import csv
import urllib.request as urllib
import os
import hashlib

import PyPDF2
from PyPDF2 import PdfFileReader

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

currentPath = os.getcwd()

f = open('tagged.csv', encoding="utf-8")
reader = csv.reader(f)
readFile = list(reader)
f.close()

lastNum = 1
i = -1
for r in readFile:
    i = i + 1
    if(r[0])==str(lastNum):
        tempFileNames = collections.defaultdict(list)
        tempFileHash = collections.defaultdict(list)
        path = os.path.join(currentPath, str(lastNum))
        os.mkdir(path)
        lastNum = lastNum + 1
    if(len(r)>4):
        file_name = r[4].split('/')[-1]
        if (file_name not in tempFileNames.keys()):
            tempFileNames[file_name].append(i)
            readFile[i].append(' ')
        else:
            readFile[i].append('Duplicate filename')
            k = tempFileNames.get(file_name)[0]
            readFile[k][5] = 'Duplicate filename'
        filePath =  path + '/' + file_name
        urllib.urlretrieve(r[4], filePath )
        hash = md5(filePath)
        if (hash not in tempFileHash.keys()):
            tempFileHash[hash].append(i)
            readFile[i].append(hash)
        else:
            readFile[i].append('Duplicate hash')
            k = tempFileHash.get(hash)[0]
            readFile[k][6] = 'Duplicate hash'
        pd = PdfFileReader(open(filePath, "rb"))
        if(pd.isEncrypted):
            print("Cant read")
            ########## ISSUE #################
        else:
            pdf_info = pd.getDocumentInfo()
            readFile[i].append(str(pdf_info))

with open('final.csv', "w", newline='', encoding="utf-8") as out_file:
    writeCSV = csv.writer(out_file)
    writeCSV.writerows(readFile)
out_file.close()
