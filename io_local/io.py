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
  # data=[('smith, bob',2),('carol',3),('ted',4),('alice',5)]
  with open(filename,'w') as out:
      csv_out=csv.writer(out)
      # csv_out.writerow(['name','num'])
      for row in data:
          csv_out.writerow(row)

def mapListToCsv(filename, mapsList, mode='w'):
  # data=[('smith, bob',2),('carol',3),('ted',4),('alice',5)]
  keys = set().union(*(d.keys() for d in mapsList))
  # print(keys)
  keyList = list(keys)
  # print(keyList)
  keyList.sort()
  # print(keyList)
  os.makedirs(os.path.dirname(filename), exist_ok=True)
  # print('mapsList:')
  # print(mapsList)

  # with open(filename, mode, newline='') as out:
  #   dict_writer = csv.DictWriter(out, keyList)
  #   dict_writer.writeheader()
  #   dict_writer.writerows(mapsList)

  f = io.open(filename, mode=mode, newline='', encoding="utf-8")
  dict_writer = csv.DictWriter(f, keyList)
  dict_writer.writeheader()
  dict_writer.writerows(mapsList)
