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
    nlpSeqs = nlpc.docToParseTreeDictList(doc, MAX_CHILD, MAX_DEPTH)
    io.mapListToCsv(ROOT + '/results/' + outFilename, nlpSeqs, 'a')

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