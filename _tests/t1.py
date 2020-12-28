import sys
import io_local.io as io
import nlp.nlp_controller as nlpc
import nlp.coref_controller as corefc

inputFolder = 'files/inputs'
outputFolder = 'files/outputs'

project = 't1'

def run():
  text = "My sister has a dog, she loves him. Angela lives in Boston, she is quite happy in that city."

  sents = nlpc.textToSents(text)
  for sent in sents:
    corefc.corefReplacement(sent)