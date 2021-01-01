from pprint import pprint
import spacy
import neuralcoref

langModel = "en_core_web_sm"
nlp = spacy.load(langModel)
# add pipes
neuralcoref.add_to_pipe(nlp)
sentencizer = nlp.create_pipe('sentencizer')
sentencizer.__init__([','])
nlp.add_pipe(sentencizer)

def textToDoc(text):
  doc = nlp(text)
  return doc

def textToSents(text):
  doc = nlp(text)
  return doc.sents

def getDefaultNLPDict():
  return {
    '_is_fact': 0,
    '_is_rule': 0,
    '_is_query': 0,
    '_text': '',
  }

# in: text
# out:
#   list of
#     obj of sent text and its NLP data of diff tokens
def textToNLPDictsList(text):
  print(text)
  print('##############################################################################################################################')
  doc = nlp(text)
  res = []
  for sent in doc.sents:
    print(sent)
    if (sent.text != ''):
      print('###############################################################')
      print('sent to process: ' + sent.text)
      # nlpDict = {'_text': sent.text}
      nlpDict = getDefaultNLPDict()
      nlpDict['_text'] = sent.text
      for token in sent:
        key = token.dep_
        keyBase = token.dep_
        keyI = 1
        # add postfix if key dep_ already exists
        while (nlpDict.get(key) != None):
          keyI += 1
          key = keyBase + str(keyI)
        nlpDict[key] = getCorefLemma(token)
        nlpDict[key + '_text'] = token.text
        nlpDict[key + '_lemma'] = token.lemma_
      print(nlpDict)
      res.append(nlpDict)
  return res

def sentToNLPSequence(sent):
  # item = {'_text': sent.text}
  item = getDefaultNLPDict()
  item['_text'] = sent.text
  posSeq = ''
  tagSeq = ''
  depSeq = ''
  lemmaSeq = ''
  corefLemmaSeq = ''
  for i, token in enumerate(sent):
    posSeq += ' ' + token.pos_
    tagSeq += ' ' + token.tag_
    depSeq += ' ' + token.dep_
    lemmaSeq += ' ' + token.lemma_
    # corefLemmaSeq += ' ' + getCorefLemma(token)
    corefLemmaSeq += getNonRepeatedCorefLemma(i, sent)
  item['posSeq'] = posSeq
  item['tagSeq'] = tagSeq
  item['depSeq'] = depSeq
  item['lemmaSeq'] = lemmaSeq
  item['corefLemmaSeq'] = corefLemmaSeq
  return item

def getCorefLemma(token):
  if (token._.in_coref):
    return token._.coref_clusters[0].main.lemma_
  else:
    return token.lemma_

def getCoref(token):
  if (token._.in_coref):
    return token._.coref_clusters[0].main
  else:
    return None

def getNonRepeatedCorefLemma(i, tokens):
  token = tokens[i]
  coref = getCoref(token)
  if (i >= 1):
    prevToken = tokens[i-1]
    prevCoref = getCoref(prevToken)
    if (coref != None):
      if (prevCoref != None):
        if (coref.start == prevCoref.start and coref.end == prevCoref.end):
          # is repeated coref, omit
          return ''
        else:
          # is new coref, return
          return ' ' + getCorefLemma(token)
      else:
        return ' ' + getCorefLemma(token)
    else:
      return ' ' + token.lemma_
  else:
    return ' ' + getCorefLemma(token)


def textToNLPSequenceList(text):
  doc = nlp(text)
  res = []
  for sent in doc.sents:
    if(sent.text != ''):
      item = sentToNLPSequence(sent)
      res.append(item)
  return res

def textToSimplifiedNLPSequenceList(text):
  doc = nlp(text)
  res = []
  for sent in doc.sents:
    if(sent.text != ''):
      sent = simplifySent(sent)
      item = sentToNLPSequence(sent)
      res.append(item)
  return res

def getNoParentTokens(sent):
  noParentTokens = []
  # find token with no parents
  for token in sent:
    hasNoParent = True
    for token2 in sent:
      if (token2.children is not None):
        for child in token2.children:
          # print(type(child))
          if (child == token):
            hasNoParent = False
    if (hasNoParent):
      noParentTokens.append(token)
  return noParentTokens
  
# sent processing
def simplifySent(sent):
  text = sent.text
  for chunk in sent.noun_chunks:
    text = text.replace(chunk.text, chunk.root.text, 1)
  return nlp(text)

def sentToDepTree(sent):
  tree = {}
  
  return tree

def printDoc(doc):
  for sent in doc.sents:
    print('###############################################################')
    print(sent.text)
    for token in sent:
        print(token.text, token.pos_, token.dep_)

