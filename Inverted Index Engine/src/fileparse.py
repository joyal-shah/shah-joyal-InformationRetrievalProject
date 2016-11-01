import sys
import regex
import json
from ordereddict import OrderedDict
import os
from stemming.porter2 import stem

class FileParser(object):
    def __init__(self):
        self.fileCount = 0
        self.documentID = ""

    def readContent(self,index_file, start_pos, bytes_to_read):
        data = ""
        with open(index_file, "rb") as binary_file:
            # Seek position and read N bytes
            binary_file.seek(start_pos)  # Go to beginning
            data = binary_file.read(bytes_to_read)
            binary_file.close()
            return data

    def readFiles(self,fileName,fileType):
        try:
            with open(fileName) as data_file:
                if fileType == "json":
                    data = json.load(data_file)
                else:
                    data = data_file.read()
            return data
        except:
            print("Error while reading file " + fileName)
            if fileType == "json":
                return {}
            else:
                return ""

    def appendToFile(self,fileName,fileExtension,fileContent):
        try:

            name = fileName + "." + fileExtension

            if fileExtension == "json":
                json_data = {}

                #read content from files if already existing
                if os.path.isfile(name):
                    json_data = self.readFiles(name, fileExtension)

                json_data.update(json.loads(fileContent))
                self.createNewFiles(fileName,fileExtension,json.dumps(json_data))
                json_data.clear()
            else:
                if os.path.isfile(name):
                    with open(name, "a+") as cur_file:
                        cur_file.write(str(fileContent))
                        cur_file.close()
                else:
                    self.createNewFiles(fileName,fileExtension,fileContent)
        except:
            print("error occured")
            sys.exit(0)

    def createNewFiles(self,fileName,fileExtension,fileContent):
        try:
            name = fileName + "." + fileExtension
            file = open(name, 'w')
            file.write(str(fileContent))
            file.close()
        except:
            print("error occured")
            sys.exit(0)

    def writeDocId(self):
        self.createNewFiles("DOCID","txt",self.documentID)

    def filterText(self,text,indexName,stopwords):
        global removeStopWords
        global performStemming

        removeStopWords = False
        performStemming = False

        token_tuple_list = regex.findall('([0-9a-z]+(\.?[0-9a-z]+)*)',text.lower().strip())
        data_list = []

        if indexName in ("index_10","index_11"):
            performStemming = True

        if indexName in ("index_01","index_11"):
            removeStopWords = True

        for tuple in token_tuple_list:
            temp_text = tuple[0]

            if removeStopWords and temp_text in stopwords: #Do not append
                continue

            if performStemming:
                temp_text = stem(temp_text)

            data_list.append(temp_text)

        return data_list

    def getPositionIndices(self, termList):
        posMap = OrderedDict({})
        item_index = 0
        for term in termList:
            if term not in posMap:
                posMap[term] = []
            posMap[term].append(item_index)
            item_index = item_index + 1
        return posMap

    def indexFile(self,filePath,startDocIndex,indexName,stopwords):
        docContent = {}
        docMap = {}
        docLength = {}
        try:
            fileToOpen = open(filePath,'r')

            newDocFound = False
            curDocNo = ""
            curText = ""
            appendText = False

            for line in fileToOpen:
                # check whether its a new Doc
                if line.__contains__("<DOC>"):
                    newDocFound = True
                if line.__contains__("</DOC>"):
                    docContent[startDocIndex] = {}
                    tempDocText = self.filterText(curText,indexName,stopwords)
                    positions = self.getPositionIndices(tempDocText)
                    docContent[startDocIndex][curDocNo] = positions
                    docMap[startDocIndex] = curDocNo
                    docLength[curDocNo] = len(tempDocText)
                    startDocIndex = startDocIndex + 1

                    # reset variables
                    newDocFound = False
                    curDocNo = ""
                    curText = ""

                if newDocFound == True:
                    if appendText == True:
                        curText += line
                    if line.__contains__("<DOCNO>"):
                        curDocNo = line.replace("<DOCNO> ", "").replace(" </DOCNO>\n", "")
                    if line.__contains__("<TEXT>"):
                        appendText = True
                        curText += line
                    if line.__contains__("</TEXT>"):
                        appendText = False
                        curText = curText.replace("<TEXT>", "").replace("</TEXT>", "").replace("\n", " ")
        except IOError:
            print("Error: can't find file or read data")
        else:
            fileToOpen.close()

        return (docContent,docMap,docLength)