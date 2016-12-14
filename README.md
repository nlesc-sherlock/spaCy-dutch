# spaCy-dutch

Repository for creating models, vocabulary and other necessities for Dutch in spaCy.
By explaining in detail what we did, we also hope it becomes easier for others to add new
languages.

## Add Dutch Language to spaCy

To be able to load the spaCy pipleline for Dutch (or another language), the language
must be added to spaCy:

* Create file `spacy/nl/__init__.py` to define the Dutch language
* Created file `spacy/nl/language_data.py` and populated stop words with existing list, the rest was copied from German
* Add `nl` to `spacy/__init__.py`, `spacy/__init__.py` and `setup.py`
* Create test in `spacy/tests/integration/test_load_languages.py`

For people who just want to play with Dutch text in spaCy, the necessary adjustments
to the code can be found in [this repository](https://github.com/nlesc-sherlock/spacy).
Use the branch `dutch`. To install the Dutch version of spaCy:

```
# make sure you are using recent pip/virtualenv versions
python -m pip install -U pip virtualenv

git clone https://github.com/nlesc-sherlock/spaCy.git
cd spaCy
git checkout dutch

virtualenv .env && source .env/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Add Dutch language data folder

This README specifies how we trained models for Dutch. The resulting models and
other data can be downloaded from [Zenodo](http://doi.org/10.5281/zenodo.202662).
After downloading and extracting the archive, copy the nl-0.1.0 folder to `spaCy/spacy/data`.

The Dutch pipeline using trained models can now be loaded with:
```
import spacy

nlp = spacy.load('nl')
```
*Please note that the pipeline can also be loaded without the Dutch language data folder.
And that spaCy will complain when something is missing from the language data.
Keep this in mind when creating your own language resources.*

## Create Vocab with Brown clusters, word frequencies, and vectors

To generate Brown clusters, word frequencies, and vectors we used a (small) subset of the
Dutch Wikipedia. To be precise, we used the first 10000 documents from the
[Wikipedia dump of November 20, 2016](https://dumps.wikimedia.org/nlwiki/20161120/).

After downloading the dump files
* https://dumps.wikimedia.org/nlwiki/20161120/nlwiki-20161120-pages-articles1.xml.bz2
* https://dumps.wikimedia.org/nlwiki/20161120/nlwiki-20161120-pages-articles2.xml.bz2
* https://dumps.wikimedia.org/nlwiki/20161120/nlwiki-20161120-pages-articles3.xml.bz2
* https://dumps.wikimedia.org/nlwiki/20161120/nlwiki-20161120-pages-articles4.xml.bz2

article text was extracted using [sift](https://github.com/wikilinks/sift) (requires
[pyspark](http://spark.apache.org/docs/0.9.0/python-programming-guide.html)).
See [notebook](https://github.com/nlesc-sherlock/spaCy-dutch/blob/master/notebooks/extract%20wikipedia%20dump.ipynb)

Next run the script to initialize the model:

```
sh scripts/createvocab.sh path/to/temp path/to/corpus outputpath
```

`path/to/corpus` refers to a directory containing text files. There should be a text file
for each document in the corpus. The files should be utf-8 encoded.

Settings used to generate the Dutch data:
* the corpus consists of 999 (more or less random) Wikipedia articles (**this is much too small!**)
* 100 Brown clusters (**this is much too small!**)
* vector size 300 and window size 5

The script downloads [brown-cluster](https://github.com/percyliang/brown-cluster)
and [GloVe](https://github.com/stanfordnlp/GloVe) to generate models. This software is
deleted when the script is done.

The script creates files:

* `vocab/lexems.bin`
* `vocab/oov_prob`
* `vocab/strings.json`
* `vocab/tag_map.json`
* `vocab/vec.bin`

## POS tagger

The POS tagger was trained using the Dutch data from Universal Dependencies:
* [UD_Dutch](https://github.com/UniversalDependencies/UD_Dutch)
* [UD_Dutch-LassySmall](https://github.com/UniversalDependencies/UD_Dutch-LassySmall)

For training, we used both train sets and for testing we used both test sets.
See the [notebook](https://github.com/nlesc-sherlock/spaCy-dutch/blob/master/notebooks/Dutch%20tagger%20UD%20data.ipynb)
for number of training iterations and performance plots.

The accuracy on the test set is 88.57 when using an empty vocabulary and default
lexical attributes. When using the
Dutch vocab (i.e., adding Brown clusters and word frequencies), accuracy is 88.43.
Using the Dutch vocabulary did not improve POS tagger accuracy. This probably is
due to the small corpus used to generate the Brown clusters, and the small number of
clusters extracted. It is likely that the performance of the POS tagger will
increase if it is retrained using better Brown cluster data.

[Notebook](https://github.com/nlesc-sherlock/spaCy-dutch/blob/master/notebooks/Dutch%20tagger%20UD%20data.ipynb)
with code for training and evaluating the POS tagger (based on
[this example](https://github.com/explosion/spaCy/blob/master/examples/training/train_tagger.py)).
In this notebook, the following data files are generated:

* `vocab/tag_map.json`
* `vocab/serializer.json`
* `pos/model`

## Named Entity Recognizer

The NER was trained using data from [CoNLL 2002](http://www.cnts.ua.ac.be/conll2002/ner.tgz)
([more info](http://www.cnts.ua.ac.be/conll2002/ner/)). *The UD_Dutch(-LassySmall) data does
not contain NER data.*

After downloading and extracting the data (files `data/ned.train.gz`, `data/ned.testa`,
`data/ned.testb`), run the script to create the NER component:
```
python models/NERtagger.py /path/to/CONLLdata/ /path/to/store/model/files
```

The NER component is trained for 30 iterations.

The script generates the following files:

* `ner/model`
* `ner/config.json`

Performance can be calculated using [this
notebook](https://github.com/nlesc-sherlock/spaCy-dutch/blob/master/notebooks/EvaluateNER.ipynb).

Test set | Precision | Recall | F-measure
--- | --- | --- | ---
CoNLL 2002 testa | 68.95 | 66.23 | 67.56
CoNLL 2002 testb | 73.61 | 71.42 | 72.50

Compared to the [results from CoNLL 2002](http://www.cnts.ua.ac.be/conll2002/ner/),
this performance is not bad, but not extremely good either.

Improved POS tagging might benefit these results.

## Dependency parser

**Note** training the dependency parser for Dutch is not finished yet.

The dependency parser was trained using [UD_Dutch-LassySmall](https://github.com/UniversalDependencies/UD_Dutch-LassySmall).
This [notebook](https://github.com/nlesc-sherlock/spaCy-dutch/blob/master/notebooks/train%20dutch%20dependency%20parser.ipynb)
explains how the parser was trained.

First, we had to transform the training data, because spaCy uses a different numbering
of the heads than what is provided in the data.

```
# format used in UD_Dutch-LassySmall
words = [u'In', u'werkelijkheid', u'werd', u'hij', u'gevangen', u'genomen', u'door', u'de', u'Britse', u'generaal', u'Halkett', u'.']
heads = [2, 6, 6, 6, 6, 0, 10, 10, 10, 6, 10, 6]
deps = [u'case', u'nmod', u'auxpass', u'nsubj', u'compound', 'root', u'case', u'det', u'amod', u'nmod', u'appos', u'punct']

# same sentence in spaCy format
words = [u'In', u'werkelijkheid', u'werd', u'hij', u'gevangen', u'genomen', u'door', u'de', u'Britse', u'generaal', u'Halkett', u'.']
heads = [1, 5, 5, 5, 5, 5, 9, 9, 9, 5, 9, 5]
deps = [u'case', u'nmod', u'auxpass', u'nsubj', u'compound', 'root', u'case', u'det', u'amod', u'nmod', u'appos', u'punct']
```
Training the parser with this data results in the following error message:

```
ValueError: Could not find a gold-standard action to supervise the dependency parser.
The GoldParse was projective.
```

## Language data
The data generated should consist of the following files:

File | Copied/Generated | Source
--- | --- | ---
`deps/config.json` | Generated | n.a.
`deps/model` | Generated | n.a.
`ner/config.json` | Generated | NER
`ner/model` | Generated | NER
`pos/model` | Generated | POS tagger
`tokenizer/infix.txt` | Copied | German language data
`tokenizer/morphs.json` | Copied | German language data
`tokenizer/prefix.json` | Copied | German language data
`tokenizer/specials.json` | Copied | German language data
`tokenizer/suffix.json` | Copied | German language data
`vocab/gazetteer.json` | Copied | German language data
`vocab/lemma_rules.json` | Copied | German language data
`vocab/lexems.bin` | Generated | `scripts/createvocab.sh`
`vocab/oov_prob` | Generated | `scripts/createvocab.sh`
`vocab/serializer.json` | Generated | POS tagger
`vocab/strings.json` | Generated | `scripts/createvocab.sh`
`vocab/tag_map.json` | Generated | `scripts/createvocab.sh`
`vocab/vec.bin` | Generated | `scripts/createvocab.sh`

## To do list

### Required

* Better (larger corpus) for generating vocab data
  * Better word frequencies
  * More Brown clusters (~3700)
  * Retrain vectors on better corpus
  * Retrain POS tagger
  * Retrain NER
* Train Dependency parser (fix error)
* Add tests for models

### Nice to have/experiment with

* Files for tokenizer (pre/in/suffixes etc.) (now it is copied for German)
* Throw away short sentences in the training data
* Threshold POS tags on confidence
* Create download script for Dutch language data
* More thourough evaluation of POS, NER, and DEP
* Add [Dutch WordNet](https://github.com/cltl/OpenDutchWordnet)
