from pprint import pprint
import spacy
import neuralcoref

langModel = "en_core_web_sm"
nlp = spacy.load(langModel)
# add pipes
neuralcoref.add_to_pipe(nlp)
# comma sentencizer is exec after coref
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

def tokensToNLPSequence(tokens, postfix=''):
  # item = {'_text': sent.text}
  item = getDefaultNLPDict()
  # item['_text'] = sent.text
  posSeq = ''
  tagSeq = ''
  depSeq = ''
  lemmaSeq = ''
  corefLemmaSeq = ''
  for i, token in enumerate(tokens):
    posSeq += ' ' + token.pos_
    tagSeq += ' ' + token.tag_
    depSeq += ' ' + token.dep_
    lemmaSeq += ' ' + token.lemma_
    # corefLemmaSeq += ' ' + getCorefLemma(token)
    corefLemmaSeq += getNonRepeatedCorefLemma(i, tokens)
  item['posSeq' + postfix] = posSeq
  item['tagSeq' + postfix] = tagSeq
  item['depSeq' + postfix] = depSeq
  item['lemmaSeq' + postfix] = lemmaSeq
  item['corefLemmaSeq' + postfix] = corefLemmaSeq
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


def docToNLPSequenceList(doc):
  res = []
  for sent in doc.sents:
    if(sent.text != ''):
      item = tokensToNLPSequence(sent)
      item['_text'] = sent.text
      res.append(item)
  return res

def docToMaxDepthsTreeNLPSequenceList(doc, maxDepths):
  res = []
  for sent in doc.sents:
    if(sent.text != ''):
      finalItem = {}
      finalItem['_text'] = sent.text
      for maxDepth in maxDepths:
        postfix = '_d' + str(maxDepth)
        nlpTreeTraverseTokens = sentToMaxDepthTree(sent, maxDepth)
        item = tokensToNLPSequence(nlpTreeTraverseTokens, postfix)
        finalItem = {**finalItem, **item}
      res.append(finalItem)
  return res

def docToMaxDepthTreeNLPSequenceList(doc, maxDepth):
  res = []
  for sent in doc.sents:
    if(sent.text != ''):
      nlpTreeTraverseTokens = sentToMaxDepthTree(sent, maxDepth)
      item = tokensToNLPSequence(nlpTreeTraverseTokens)
      item['_text'] = sent.text
      res.append(item)
  return res

def sentToMaxDepthTree(sent, maxDepth):
  sentRoots = getNoParentTokens(sent)
  resTokens = []
  for sentRoot in sentRoots:
    addTreeNodesMaxDepth(resTokens, sentRoot, maxDepth)
  return resTokens

def addTreeNodesMaxDepth(resList, treeRoot, maxDepth):
  # mid first traverse
  if maxDepth == 0:
    return
  else:
    resList.append(treeRoot)
    # recurse children
    if (treeRoot.children is not None):
      for child in treeRoot.children:
        addTreeNodesMaxDepth(resList, child, maxDepth-1)


def docToSimplifiedNLPSequenceList(doc):
  res = []
  for sent in doc.sents:
    if(sent.text != ''):
      # simple sent
      sent = simplifySent(sent)
      item = tokensToNLPSequence(sent)
      item['_text'] = sent.text
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

def parseTreeToDict(rootNodes, currDepth, maxChild, maxDepth):
  resDict = {}
  recursiveParseTreeToDict(resDict, rootNodes, 0, maxChild, maxDepth)
  return resDict


def recursiveParseTreeToDict(resDict, rootNodes, currDepth, maxChild, maxDepth):
  if currDepth == maxDepth:
    return
  if rootNodes == None:
    return
  for i,node in enumerate(rootNodes[:maxChild]):
    prefix = str(currDepth) + '-' + str(i) + '_'
    resDict[prefix + 'dep_'] = node.dep_
    resDict[prefix + 'pos_'] = node.pos_
    resDict[prefix + 'tag_'] = node.tag_
    resDict[prefix + 'lemma_'] = node.lemma_
    resDict[prefix + 'corefLemma_'] = node._.coref_clusters[0].main.corefLemma_
    recursiveParseTreeToDict(resDict, node.children[:maxChild], currDepth + 1, maxChild, maxDepth)
  

  
# sent processing
# TODO: simplify by working on NLP doc instead of change to string back and forth
def simplifySent(sent):
  text = sent.text
  for chunk in sent.noun_chunks:
    text = text.replace(chunk.text, chunk.root.text, 1)
  return nlp(text)

# def sentToDepTree(sent):
#   tree = {}
  
#   return tree

def printDoc(doc):
  for sent in doc.sents:
    print('###############################################################')
    print(sent.text)
    for token in sent:
        print(token.text, token.pos_, token.dep_)

