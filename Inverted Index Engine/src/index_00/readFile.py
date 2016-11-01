from stemming.porter2 import stem
from ordereddict import OrderedDict
import json
import os

def readTermFile(termFile):

    requiresStemming = False
    curDir = os.getcwd()

    if (curDir.__contains__("index_11") or curDir.__contains__("index_10")):
        requiresStemming = True

    with open(termFile) as f:
        data = f.readlines()
        cdata = OrderedDict({})

        for d in data:
            d=d[0:-1]
            original_term = d
            if requiresStemming:
                d = stem(d)
            cdata[original_term] = d
        return cdata

def getFileData(file_name):

        fileToOpen = file_name

        data = {}

        with open(fileToOpen) as data_file:
            data = json.load(data_file)

        return data

def getDataFromIndexFile(term,termID,Catalog,documentID):

        index_file = "index.txt"
        # Get OffSet from catalog file
        term_data = Catalog[termID[term]].split(':')

        start_pos = int(term_data[0])
        bytes_to_read = int(term_data[1])
        tup_1 = readContent(index_file, start_pos, bytes_to_read)
        docT = tup_1.split(':')
        docMap = []

        for docTuple in docT:
            docs_data = docTuple.split(",")
            docId = documentID[docs_data[0]]
            docTerms = []
            for posIndex in docs_data[1:]:
                docTerms.append(int(posIndex))
            tf = len(docTerms)
            docMap.append({'docId': docId, '_score': tf, 'tpos': docTerms})

        return docMap

def readContent(index_file, start_pos, bytes_to_read):
    data = ""
    with open(index_file, "rb") as binary_file:
        # Seek position and read N bytes
        binary_file.seek(start_pos)  # Go to beginning
        data = binary_file.read(bytes_to_read)
        binary_file.close()
        return data


def createNewFiles(fileName, fileExtension, fileContent):
    try:
        name = fileName + "." + fileExtension
        file = open(name, 'w')
        file.write(str(fileContent))
        file.close()
    except:
        print("error occured")

input_terms = readTermFile("in.4")

fileContent = ""

Catalog = getFileData("catalog.json")
documentID = getFileData("docId.json")
termID = getFileData("terms.json")

for term in input_terms:
    if input_terms[term] in termID:
        docs_for_term = getDataFromIndexFile(input_terms[term],termID,Catalog,documentID)
    else:
        fileContent += term + " " + "0 0" + "\n"
    doc_freq = len(docs_for_term)
    term_freq = 0
    for data in docs_for_term:
        term_freq += len(data['tpos'])
    fileContent += term + " " + str(doc_freq) + " " + str(term_freq) + "\n"

createNewFiles("joyal.out.no.stop.no.stem","txt",fileContent)

