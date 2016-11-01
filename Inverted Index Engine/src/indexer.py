#HW2 - Indexer
from operator import itemgetter
from tokenizer import *
from fileparse import *
import os


# This class implements custom Indexer as per HW2 requirements
class Indexer(object):

    def __init__(self):
        self.dirPath = "E:\\NEU - Computer Engineering\\Sem2\\IR\\Data\\AP89_DATA\\AP_DATA\\ap89_collection"
        self.docsData = {}
        self.AllDocs = {}
        self.DocLength = {}
        self.fileController = FileParser()
        self.tokenController = Tokenizer()
        self.stopwords = self.getStopWords()

    def getStopWords(self):
        fileToOpen = open("StopWords.txt", 'r')

        stopwords = []

        for line in fileToOpen:
            stopwords.append(line.replace("\n", ""))

        return stopwords

    def PerformIndex(self,batchSize,indexName):

        files_list = self.getFileList()
        totalFiles = len(files_list)
        fileIndex = 0
        if totalFiles != 0:
            filesIndexed = 0
            docIndex = 1

            while (filesIndexed <= totalFiles):

                endIndex = filesIndexed + batchSize

                if endIndex > totalFiles:
                    diff = endIndex - totalFiles
                    endIndex = endIndex - diff

                for files in files_list[filesIndexed:endIndex]:
                    fileIndex = fileIndex + 1
                    tup = self.fileController.indexFile(files, docIndex,indexName,self.stopwords)
                    docsInFile = tup[0]
                    docIndex = docIndex + len(docsInFile)
                    self.docsData.update(docsInFile)
                    self.AllDocs.update(tup[1])
                    self.DocLength.update(tup[2])

                filesIndexed = filesIndexed + batchSize

                temp_name = str((filesIndexed / batchSize))

                if len(temp_name) == 1:
                    temp_name = "0" + temp_name

                invertedFileName = "index_" + temp_name

                print('Creating inverted index file ' + invertedFileName)

                # Updates the TermIdMap with new terms from parsed docs
                self.tokenController.updateTermIdMap(self.docsData, invertedFileName,indexName)

                # reset docData
                self.docsData.clear()

                print ("Completed batch: " + str((filesIndexed / batchSize)))

            print (len(self.tokenController.termIdMap))
            term_l = sorted(self.tokenController.termIdMap.items(), key=itemgetter(1))
            t_c = {}
            for t in term_l:
                t_c[t[0]] = str(t[1])
            self.fileController.createNewFiles(indexName+"\\terms","json",json.dumps(t_c))
            self.fileController.createNewFiles(indexName+"\\docId", "json", json.dumps(self.AllDocs))
            self.fileController.createNewFiles(indexName+"\\doclength", "json", json.dumps(self.DocLength))

        else:
            print("No files found in directory")

    def getFileList(self):
        fileList = []

        for root, dirs, files in os.walk(self.dirPath):
            for name in files:
                if name not in ('readme'):
                    fileList.append(os.path.join(root,name))

        return fileList