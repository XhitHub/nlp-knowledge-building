import csv
import os
import io

def csvToList(filename):
  with open(filename, newline='') as f:
      reader = csv.reader(f)
      data = list(reader)
  return data

def textFileToString(filename):
  f = open(filename, "r")
  res = ""
  for x in f:
    res += x
  return res

def tupleListToCsv(filename, data):
  with open(filename,'w') as out:
      csv_out=csv.writer(out)
      # csv_out.writerow(['name','num'])
      for row in data:
          csv_out.writerow(row)

def mapListToCsv(filename, mapsList, mode='w', header=None, writeheader=False):
  os.makedirs(os.path.dirname(filename), exist_ok=True)
  if (header == None):
    keys = set().union(*(d.keys() for d in mapsList))
    keyList = list(keys)
    keyList.sort()
  else:
    keyList = header
  f = io.open(filename, mode=mode, newline='', encoding="utf-8")
  dict_writer = csv.DictWriter(f, keyList)
  if writeheader:
    dict_writer.writeheader()
  dict_writer.writerows(mapsList)

def getHeaderFromMapList(mapsList):
  keys = set().union(*(d.keys() for d in mapsList))
  keyList = list(keys)
  keyList.sort()
  return keyList
