import json
from fileparse import *
class Tokenizer(object):

    def __init__(self):
        self.termIdMap = {}
        self.termDocMap = []
        self.fileController = FileParser()

    '''
    updateTermIdMap: Updates existing document dictionary, with new invertedFile and index
    '''
    def updateTermIdMap(self,docDict,invertedFileName,indexName):
        termId = len(self.termIdMap) + 1

        self.termTuple = {}

        for docId in docDict:
            for docNo in docDict[docId]:
                docText = docDict[docId][docNo]

                for w in docText:

                    if w not in self.termIdMap:
                        self.termIdMap[w] = termId
                        termId = termId + 1

                    posList = docText[w]

                    if len(posList) == 0:
                        print('')

                    if w not in self.termTuple:
                        self.termTuple[w] = {}

                    if docId not in self.termTuple[w]:
                       self.termTuple[w][docId] = {}

                    self.termTuple[w][docId] = {'tf': len(posList), 'tf_pos': posList}

        fileContent = ""
        catalogFileContent = {}
        startOffSet = 0
        endOffSet = 0
        for term in self.termTuple:
            doc_freq = len(self.termTuple[term])
            ttf = 0
            docTuple = ""

            for data in sorted(self.termTuple[term].items(), key = lambda x: x[1]['tf'], reverse=True):
                doc_Id = str(data[0])
                doc_tf = str(data[1]['tf'])
                doc_tpos = ""

                for pos in data[1]['tf_pos']:
                    doc_tpos += str(pos) + ","

                ttf = ttf + int(doc_tf)

                docTuple += doc_Id + "," + doc_tpos[0:-1] + ":"

            finalDocTuple = docTuple[0:-1] + "\n"
            fileContent += finalDocTuple
            endOffSet = len(finalDocTuple)
            catalogFileContent[self.termIdMap[term]] = str(startOffSet).encode('utf-8') + ':' + str(endOffSet - 1).encode('utf-8')
            startOffSet += endOffSet + 1

        self.fileController.createNewFiles(indexName+"\\"+invertedFileName, "txt", str(fileContent[0:-1]).encode('utf-8'))
        self.fileController.createNewFiles(indexName+"\\"+invertedFileName, "json", json.dumps(catalogFileContent))