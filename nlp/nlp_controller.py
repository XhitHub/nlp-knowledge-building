from pprint import pprint
import spacy

langModel = "en_core_web_sm"
nlp = spacy.load(langModel)

def textToDoc(text):
  doc = nlp(text)
  return doc

def textToSents(text):
  doc = nlp(text)
  return doc.sents

def getDefaultNLPDict():
  return {
    'text': ''
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
      nlpDict = {'text': sent.text}
      for token in sent:
        # if (!nlpDict[token.dep_])
        nlpDict[token.dep_] = token.lemma_
        nlpDict[token.dep_ + '_text'] = token.text
      print(nlpDict)
      res.append(nlpDict)
  return res

def sentToNLPSequence(sent):
  item = {'_text': sent.text}
  posSeq = ''
  tagSeq = ''
  depSeq = ''
  lemmaSeq = ''
  for token in sent:
    posSeq += ' ' + token.pos_
    tagSeq += ' ' + token.tag_
    depSeq += ' ' + token.dep_
    lemmaSeq += ' ' + token.lemma_
  item['posSeq'] = posSeq
  item['tagSeq'] = tagSeq
  item['depSeq'] = depSeq
  item['lemmaSeq'] = lemmaSeq
  return item

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

