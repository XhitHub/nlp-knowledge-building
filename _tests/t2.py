import sys
import io_local.io as io
import nlp.nlp_controller as nlpc

inputFolder = 'files/inputs'
outputFolder = 'files/outputs'

project = 't1'

def run():
  text = "Almost all module functions depend on the basic function random(), which generates a random float uniformly in the semi-open range [0.0, 1.0). Python uses the Mersenne Twister as the core generator. It produces 53-bit precision floats and has a period of 2**19937-1. The underlying implementation in C is both fast and threadsafe. The Mersenne Twister is one of the most extensively tested random number generators in existence. However, being completely deterministic, it is not suitable for all purposes, and is completely unsuitable for cryptographic purposes."

  sents = nlpc.textToSents(text)
  for sent in sents:
    noParentTokens = nlpc.getNoParentTokens(sent)
    print('###############################')
    print(sent)
    for token in noParentTokens:
      print(token.text)
    print('###############')
    for token in noParentTokens:
      print(token.dep_)
