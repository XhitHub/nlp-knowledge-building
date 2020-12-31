import spacy
import neuralcoref

langModel = "en_core_web_sm"
nlp = spacy.load(langModel)
neuralcoref.add_to_pipe(nlp)

def corefReplacement(sent):
  doc1 = nlp(sent.text)
  print(doc1._.coref_clusters)
  for token in doc1:
    print(token.lemma_)
    if (token._.in_coref):
      # print ("(" + str(token._.coref_clusters[0].main) + ")")
      for cluster in token._.coref_clusters:
        print ("(" + str(cluster.main) + ")")