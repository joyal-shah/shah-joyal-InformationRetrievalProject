import time
from indexer import *
from main_merge import *

if __name__ == '__main__':

    #region 1. Initialize Objects
    indexObj = Indexer()
    mergerObj = FileMerge()
    #endregion

    # Implement indexing in batch size of 4
    batchSize = 4

    # region 2. Start Indexing
    print("Starting Indexing with processing " + str(batchSize) + " files at a time")
    start_time = time.time()
    indexObj.PerformIndex(batchSize, "index_00")
    print("Completed Indexing")
    print("--- %s seconds ---" % (time.time() - start_time))
    # endregion

    # region 3. Implement Merge Sort on Index files using Catalog file and Dictionary
    print("Starting Merging files")
    start_time = time.time()
    mergerObj.StartMerge_MultiCores("index_00")
    print("Completed Merging")
    print("--- %s seconds ---" % (time.time() - start_time))
    #endregion