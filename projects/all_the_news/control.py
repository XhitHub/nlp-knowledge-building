import sys
import re
import pandas as pd
import io_local.io as io
import nlp.nlp_controller as nlpc

# project dependent
#   data shape
#   how to get the text
# same for diff projects
#   processing on text
#   save processing res

ROOT = 'projects/all_the_news/data'
inFilename = 'articles1.csv'
# outFilename = 'articles1_NLPSEQ.csv'
outFilename = 'articles1_PARSE_TREE_DICT.csv'
outFilename_write = 'articles1_PARSE_TREE_DICT_WRITE.csv'
reportFilename = 'articles1_NLPSEQ_report.txt'
maxDepths = range(3,7)
MAX_CHILD = 5
MAX_DEPTH = 7

def dataSourceToNLP():
  df = pd.read_csv(ROOT + '/'+inFilename)
  sizeStr = str(len(df.index))
  # try Vectorization later
  for index, row in df.iterrows():
    text = cleanText(row['content'])
    doc = nlpc.textToDoc(text)
    print(str(index) + '/' + sizeStr)
    # nlpSeqs = nlpc.docToMaxDepthTreeNLPSequenceList(doc, 4)
    # nlpSeqs = nlpc.docToMaxDepthsTreeNLPSequenceList(doc, maxDepths)
    treeDicts = nlpc.docToParseTreeDictList(doc, MAX_CHILD, MAX_DEPTH)
    io.mapListToCsv(ROOT + '/results/' + outFilename, treeDicts, 'a', writeheader=True)

def dataSourceUnevenHeaderToNLP_v2(stopAt=100):
  df = pd.read_csv(ROOT + '/'+inFilename)
  sizeStr = str(len(df.index))
  treeDicts = []
  # try Vectorization later
  for index, row in df.iterrows():
    if(index > stopAt):
        break
    text = cleanText(row['content'])
    doc = nlpc.textToDoc(text)
    print(str(index) + '/' + sizeStr)
    # nlpSeqs = nlpc.docToMaxDepthTreeNLPSequenceList(doc, 4)
    # nlpSeqs = nlpc.docToMaxDepthsTreeNLPSequenceList(doc, maxDepths)
    tempTreeDicts = nlpc.docToParseTreeDictList(doc, MAX_CHILD, MAX_DEPTH)
    treeDicts.extend(tempTreeDicts)
  io.mapListToCsv(ROOT + '/results/' + outFilename_write, treeDicts, 'w', writeheader=True)

def dataSourceUnevenHeaderToNLP(headerSampleCount=10, writeHeader=True):
  df = pd.read_csv(ROOT + '/'+inFilename)
  sizeStr = str(len(df.index))
  headerSampleMaplist = []
  # get header from sampling
  # try Vectorization later
  if writeHeader:
    for index, row in df.iterrows():
      if(index > headerSampleCount):
        break
      text = cleanText(row['content'])
      doc = nlpc.textToDoc(text)
      print(str(index) + '/' + sizeStr)
      treeDicts = nlpc.docToParseTreeDictList(doc, MAX_CHILD, MAX_DEPTH)
      headerSampleMaplist.extend(treeDicts)
    sampledHeader = io.getHeaderFromMapList(headerSampleMaplist)
    # write header
    io.mapListToCsv(ROOT + '/results/' + outFilename, [], 'a', header=sampledHeader)
  for index, row in df.iterrows():
    text = cleanText(row['content'])
    doc = nlpc.textToDoc(text)
    print(str(index) + '/' + sizeStr)
    treeDicts = nlpc.docToParseTreeDictList(doc, MAX_CHILD, MAX_DEPTH)
    io.mapListToCsv(ROOT + '/results/' + outFilename, treeDicts, 'a', header=sampledHeader)


def classifyNLP(featureForGrouping):
  res = {}
  df = pd.read_csv(ROOT + '/results/' + outFilename)
  sizeStr = str(len(df.index))
  for index, row in df.iterrows():
    print(str(index) + '/' + sizeStr)
    posSeq = row[featureForGrouping]
    if (res.get(posSeq) == None):
      # is new posSeq entry
      res[posSeq] = 1
    else:
      res[posSeq] += 1
  with open(ROOT + '/results/' + reportFilename, 'w') as f:
    print(res, file=f)

def cleanText(text):
  cleaned = re.sub('\s{2,}', ' ', text)
  return cleaned



# depracated

# def dataSourceToNLP_v1():
#   df = pd.read_csv(ROOT + '/'+inFilename)
#   sizeStr = str(len(df.index))
#   # try Vectorization later
#   # for row in df.itertuples():
#   for index, row in df.iterrows():
#     text = cleanText(row['content'])
#     # print('##############################################################################################################################')
#     # print('processing: ' + text)
#     print(str(index) + '/' + sizeStr)
#     nlpSeqs = nlpc.textToNLPSequenceList(text)
#     io.mapListToCsv(ROOT + '/results/' + outFilename, nlpSeqs, 'a')


# def dataSourceToNLP_v2():
#   df = pd.read_csv(ROOT + '/'+inFilename)
#   sizeStr = str(len(df.index))
#   # try Vectorization later
#   for index, row in df.iterrows():
#     text = cleanText(row['content'])
#     print(str(index) + '/' + sizeStr)
#     nlpSeqs = nlpc.textToNLPSequenceList(text)
#     io.mapListToCsv(ROOT + '/results/' + outFilename, nlpSeqs, 'a')