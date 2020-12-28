import spacy
import neuralcoref

langModel = "en_core_web_sm"
nlp = spacy.load(langModel)
neuralcoref.add_to_pipe(nlp)

def corefReplacement(sent):
  doc1 = nlp(sent.text)
  print(doc1._.coref_clusters)