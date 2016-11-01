- This Project is implemented in Python version 2.7

Objective
Implement inverted index which should be able to handle large numbers of documents and terms without using excessive memory or disk I/O.

This involves writing two programs:

1. A tokenizer and indexer
2. Language Model Ranker

Step One: Tokenizing and creating Catalog File
- The first step of indexing is tokenizing documents from the collection. 
- That is, given a raw document you need to produce a sequence of tokens. 
- A token is a contiguous sequence of characters which matches a regular expression i.e, any number of letters and numbers, possibly separated by single periods in the middle. 
- For instance, bob and 376 and 98.6 and 192.160.0.1 are all tokens. 123,456 and aunt's are not tokens.
- Assign a unique integer ID to each term and document in the collection. 
- Store the maps from term to term_id and from document to doc_id in the inverted index. 
  For instance, given a document with doc_id 20:
  The car was in the car wash.
  the tokenizer might produce the tuples:
  (1, 20, 1), (2, 20, 2), (3, 20, 3), (4, 20, 4), (1, 20, 5), (2, 20, 6), (5, 20, 7)
  with the term ID map:
  1: the
  2: car
  3: was
  4: in
  5: wash

Step Two: Indexing
- The next step is to record each document’s tokens in an inverted index. 
- The inverted list for a term must contain the following information:

- The DF and CF (aka TTF) of the term.
- A list of IDs of the documents which contain the term, along with the TF of the term within that document and a list of positions within the document where the term occurs. (The first term in a document has position 1, the second term has position 2, etc.)

Also storing the following information.

	a. The total number of distinct terms (the vocabulary size) and the total number of tokens (total CF) in the document collection.
	b. The map between terms and their IDs
	c. The map between document names and their IDs
	d. All inverted lists/files written on the hard drive have to be sorted on DocBlocks by the TF count. This will facilitate merging, in particular with mergesort. 

Performance Requirements
- Writing multiple files during the indexing process, but not more than about 1,000 files total. 
  1. For instance, not storing the inverted list for each term in a separate file.
  2. If keeping partial inverted lists in memory during indexing, then limit by number of documents (not store more than 1,000 postings per term in memory at a time). 
  3. Final inverted index should be stored in a single (or few) file(s), no more than 20. The total size must be at most that of the size of the unindexed document collection, around 300MB with stopwords, and around 170MB without stopwords.  
- Able to access the inverted list for an arbitrary term in time at most logarithmic in the vocabulary size, regardless of where that term’s information is stored in the index. 
- Cannot find an inverted list by scanning through the entire index.
