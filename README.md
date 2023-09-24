## Wikipedia Search Engine

The following code is structured accordingly:

#### Phase 1

Contains code for creating inverted index in a fast manner. It does not have any memory optimisations, and hence if used on larger dataset then it will break :p

It also has a minimal search functionality, but it will give you bad results so honestly dont bother.

- `constants.py`: stores all the constants used in the code
- `dataParser.py`: contains minimal code for structuring and tokenizing text once read from xml file
- `dataReader.py`: the main file for parsing which reads from the xml file of wikidump, converts it into inverted index and writes it to the output file
- `imports.py`: a neat file with all the import libraries required
- `page.py`: contains the class Page, to keep the data in organised structure for each wiki page.
- `search.py`: a minimal search algorithm.


To run this file, execute

`./index.sh <path to dataset> <path to inverted index folder> <path to stats file>`

Here, the dataset is the wikidump, the inverted index folder is the directory you need to create where the inverted index would be stored, and the stats file is the empty file you need to create where the stats of the index will be written.

#### Phase 2

So this contains the proper code. It has proper memory handling for inverted index, and is able to compress the size of the inverted index to 1/4th of the original size of the dump. It also contains optimizations from storage and speed purposes, which give me the search results for any query within 6 seconds. 

There are a bunch of optimizations involved for it, which are a pain to go through :p

A simple idea of what the files do:

- `constants.py`: stores all the constants used in the file
- `imports.py`: a neat file with all the import libraries required.
- `invertindex.py`: creates the final inverted index from the temporary index.
- `page.py`: contains the class Page, to keep the data in organised structure for each wikipage.
- `read_data.py`: contains the main code for reading and parsing data from the xml wiki dump
- `search.py`: contains the code for optimized searching to give you 10 most relevant result for your search query.
- `stats.py`: contains the code to get relevant statistics of the inverted index created


To create the inverted index run:

(the code is meant to run in iiith ada)

To directly run it on ada, just submit a batch job after changing relevant details for `index.sh`

If you want to run it on your local maching:

```
mkdir -p ./temp
mkdir -p ./invindex
mkdir -p ./invindex/titles
python3 read_data.py <path_to_data> <path_to_invindex> <path to index stat file>
python3 invertindex.py <path_to_invindex>
```

Similarly, for searching, just run:

```
python3 search.py <path to query file> <path to inv index>
```
