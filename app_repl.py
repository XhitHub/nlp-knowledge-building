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

  nlpDicts = []
  sentNlpMapList = nlpc.textToNLPDictsList(text)
  nlpDicts += sentNlpMapList
  io.mapListToCsv(outProjectFolder + '/nlp_dicts.csv', nlpDicts)

  nlpSeqs = nlpc.textToNLPSequenceList(text)
  io.mapListToCsv(outProjectFolder + '/nlp_seqs.csv', nlpSeqs)
  nlpSeqs = nlpc.textToSimplifiedNLPSequenceList(text)
  io.mapListToCsv(outProjectFolder + '/sim_nlp_seqs.csv', nlpSeqs)