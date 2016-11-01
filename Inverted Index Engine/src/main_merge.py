'''
This file implements merge sort on various index files and utilises catalog files to perform merging.
'''
import os
import time
import random, string

from fileparse import *

class FileMerge(object):

    def __init__(self):
        self.FilesMerged = 1
        self.FileManager = FileParser()
        self.TermCatalog = {}

    def StartMerge_MultiCores(self,directory):
        indexfileList = []
        catalogfileList = []
        for root, dirs, files in os.walk(directory):
            for name in files:
                if not name.__contains__('json'):
                    indexfileList.append(os.path.join(directory, name))

        files_completed = 0

        while (len(indexfileList)) > 1:
            print('Remaining Merges: '+str(len(indexfileList)))
            for i in range(0,1):
                f1 = indexfileList[i]
                f2 = indexfileList[i+1]
                f3 = str(f1).replace("txt","json")
                f4 = str(f2).replace("txt","json")
                tupdata = self.MergeFiles_MultiProc(f1,f2,f3,f4,directory)
                indexfileList.append(tupdata[0])
                indexfileList.remove(f1)
                indexfileList.remove(f2)

    def getTermDocTuple(self,index_file,catalogTerm):
        try:
            term_data = catalogTerm.split(':')
            start_pos = int(term_data[0])
            bytes_to_read = int(term_data[1])
            tup_1 = self.FileManager.readContent(index_file,start_pos,bytes_to_read)

            if "," not in tup_1:
                print('here')
            docT = tup_1.split(':')
            return docT
        except:
            print('Error while fetching document tuple for term')
            return ""

    def get_term_freq(self,tuple_string):
        docString = tuple_string.split(',')
        ttf = len(docString[1:])
        return ttf

    '''
    MergeTuples: Given two tuples tup1 and tup2, it merges the tuple based on term frequency utilising
                 merge sort.
    '''
    def MergeTuples(self, tup1, tup2):

        mergedTuple = []

        while len(tup1) > 0 and len(tup2) > 0:
            if self.get_term_freq(tup1[0]) >= self.get_term_freq(tup2[0]):
                mergedTuple.append(tup1[0])
                tup1.remove(tup1[0])
            else:
                mergedTuple.append(tup2[0])
                tup2.remove(tup2[0])

        # Either of tup1 or tup2 may have elements left; consume them
        while len(tup1) > 0:
            mergedTuple.append(tup1[0])
            tup1.remove(tup1[0])

        while len(tup2) > 0:
            mergedTuple.append(tup2[0])
            tup2.remove(tup2[0])

        return mergedTuple

    '''
    randomword: Given a length input, returns a random string of given length
    '''
    def randomword(self,length):
        return ''.join(random.choice(string.lowercase) for i in range(length))

    '''
    Merge_Multiple_Proc: Merges two index files (index_file_1 and index_file_2) based on catalog_data_1
                         and catalog_data_2
    '''
    def Merge_Multiple_Proc(self, index_file_1, index_file_2, catalog_data_1, catalog_data_2, directory):

        fileContent = ""
        startOffSet = 0
        endOffSet = 0
        invertedFileName = directory + "\\" + "index_" + self.randomword(4)

        for term in catalog_data_1:

            docTuple = ""
            t_1 = term
            docTuple_1 = self.getTermDocTuple(index_file_1, catalog_data_1[term])

            if term in catalog_data_2:
                docTuple_2 = self.getTermDocTuple(index_file_2, catalog_data_2[term])
                docTuple = ":".join(self.MergeTuples(docTuple_1, docTuple_2))
                catalog_data_2.pop(term, None)
            else:
                docTuple = ":".join(docTuple_1)

            fileContent += docTuple + "\n"
            endOffSet = len(docTuple) + 1
            self.TermCatalog[t_1] = str(startOffSet).encode('utf-8') + ':' + str(endOffSet - 1).encode('utf-8')
            startOffSet += endOffSet + 1
            self.FileManager.appendToFile(invertedFileName, "txt", str(fileContent).encode('utf-8'))
            fileContent = ""

        # Perform the same operation for remaining terms in Catalog_2
        for rem_term in catalog_data_2:
            docTuple = ":".join(self.getTermDocTuple(index_file_2, catalog_data_2[rem_term]))
            fileContent += docTuple + "\n"
            endOffSet = len(docTuple) + 1
            self.TermCatalog[rem_term] = str(startOffSet).encode('utf-8') + ':' + str(endOffSet - 1).encode('utf-8')
            startOffSet += endOffSet + 1
            self.FileManager.appendToFile(invertedFileName, "txt", str(fileContent).encode('utf-8'))
            fileContent = ""
            # catalog_data_2.pop(rem_term,None)

        self.FileManager.createNewFiles(invertedFileName, "json", json.dumps(self.TermCatalog))

        return(invertedFileName + ".txt",invertedFileName + ".json")

    '''
    Merge_Multiple_Proc: Merges two index files (index_file_1 and index_file_2) based on catalog_data_1
                         and catalog_data_2
    '''
    def MergeFiles_MultiProc(self,index_file_1,index_file_2,catalog_file_1,catalog_file_2,directory):

        # Bring Catalog Files in Memory
        ct1_data = self.FileManager.readFiles(catalog_file_1, "json")
        ct2_data = self.FileManager.readFiles(catalog_file_2, "json")

        ct1_size = len(ct1_data)
        ct2_size = len(ct2_data)

        if ct1_size == 0 and ct2_size == 0:
            print('No files to Merge')
        elif ct1_size > 0 and ct2_size > 0:
            mytup = self.Merge_Multiple_Proc(index_file_1, index_file_2, ct1_data, ct2_data, directory)
            self.FilesMerged += 1
            return mytup