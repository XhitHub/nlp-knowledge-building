import sys
import io_local.io as io
import nlp.nlp_controller as nlpc

inputFolder = 'C:/Users/John/Documents/pgi_dev/NLP_local_storage/inputs'
outputFolder = 'C:/Users/John/Documents/pgi_dev/NLP_local_storage/outputs'

print(sys.argv)
project = sys.argv[1]

inFilename = inputFolder + '/' + project + '.csv'
outFilename = outputFolder + '/' + project + '.csv'

res = []
textArrList = io.csvToList(project)
print(textArrList)
for textArr in textArrList:
    text = textArr[0]
    sentNlpMapList = nlpc.textToNLPDictsList(text)
    res += sentNlpMapList

io.mapListToCsv(project, res)