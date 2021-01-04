import sys
import io_local.io as io
import nlp.nlp_controller as nlpc

inputFolder = 'files/inputs'
outputFolder = 'files/outputs'

project = 't1'

def run():
  inFilename = inputFolder + '/' + project + '.txt'
  outProjectFolder = outputFolder + '/' + project

  text = io.textFileToString(inFilename)
  doc = nlpc.textToDoc(text)

  # nlpDicts = []
  # sentNlpMapList = nlpc.textToNLPDictsList(text)
  # nlpDicts += sentNlpMapList
  # io.mapListToCsv(outProjectFolder + '/nlp_dicts.csv', nlpDicts)

  # nlpSeqs = nlpc.docToNLPSequenceList(text)
  # io.mapListToCsv(outProjectFolder + '/nlp_seqs.csv', nlpSeqs)
  # nlpSeqs = nlpc.textToSimplifiedNLPSequenceList(text)
  # io.mapListToCsv(outProjectFolder + '/nlp_seqs_sim.csv', nlpSeqs)

  # for i in range(2,6):
  #   nlpSeqs = nlpc.docToMaxDepthTreeNLPSequenceList(text, i)
  #   io.mapListToCsv(outProjectFolder + '/nlp_seqs_tree_d'+str(i)+'.csv', nlpSeqs)

  nlpSeqs = nlpc.docToMaxDepthsTreeNLPSequenceList(doc, range(3,7))
  io.mapListToCsv(outProjectFolder + '/nlp_seqs_tree_depths.csv', nlpSeqs)
  
  