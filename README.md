# spaCy-dutch
Repository for creating models, vocabulary and other necessities for Dutch in Spacey

## Data used for generating Dutch language resources

### Brown clusters and word frequencies

To generate Brown clusters and word frequencies, we used a (small) subset of the
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

TODO: refer to training script

### POS tagger

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
*

### Named Entity Recognizer

### Dependency parser

### Language data
The data generated should consist of the following files:

Lemmatizer:
*	Index= Wordnet/index.{pos}
*	Exceptions = Wordnet/{pos}.exc
*	Rules = Vocab/lemma_rules.json

Vocab:
*	Lex_attr_getters, tag_map from language
*	Tag_map = Vocab/tag_map.json
*	Oov_prob = vocab/oov_prob -> input for lex_attr_getters
*	Lemmatizeer possibly loaded
*	Serializer_freqs = vocab/serializer.json

Vectors added:
*	/vocab/vec.bin are added to vocab

Tokenizer:
*	No files from datapath, all from language data(?). And vocab as input.

Tagger
*	Templates = Pos/templates.json
*	Model = pos/model

Parser
*	Cfg = Deps/config.json
*	model = Deps/model

NER
*	Cfg = Deps/config.json
* model = Deps/model

## What did we do
* created file `spacy/nl/__init__.py` to define the Ducth language
* created file `spacy/nl/language_data.py` and populated stop words with known list, the rest was copied from German
* added nl to `spacy/__init__.py`, `spacy/__init__.py` and `setup.py`
* created test in `spacy/tests/integration/test_load_languages.py`
* extracted 1000 documents from wikipedia, and tagged them with frog
* crafted a [tag-map](https://github.com/nlesc-sherlock/spaCy-dutch/blob/master/data/nl-0.1.0/vocab/tag_map.json) for Dutch, to use universal POS tags
* Added this tag_map also to `spacy/nl/language_data.py`
* Trained a POS tagger on [UD data](https://github.com/UniversalDependencies/UD_Dutch) (see [this notebook](https://github.com/nlesc-sherlock/spaCy-dutch/blob/master/notebooks/Dutch%20tagger%20UD%20data.ipynb))
* After training the POS tagger, we exported the Vocab files `strings.json`, `serializer.json`, `lexemes.bin`
* We created a data folder nl-0.1.0 and we put `tag_map.json` and the files from the previous point in the subfolder `vocab`
* In `nl-0.1.0/vocab/` we also created an empty `lemma_rules.json` and we copied the `gazetteer.json` from the English data folder
* The Tagger model was exported to `nl-0.1.0/pos`.
* We linked to this data from the spacy source code, so that we can make Dutch language pipelines
* We trained the NER model based on [CONLL2002 data](http://www.cnts.ua.ac.be/conll2002/ner/) (see [NERtagger](https://github.com/nlesc-sherlock/spaCy-dutch/tree/master/models))
* The NER model was exported to `nl-0.1.0/ner`.
* Created Notebooks to evaluate [NER](https://github.com/nlesc-sherlock/spaCy-dutch/blob/master/notebooks/EvaluateNER.ipynb) and [POS tagging](https://github.com/nlesc-sherlock/spaCy-dutch/blob/master/notebooks/EvaluateTagger.ipynb)
* Used spacy/bin/init_model.py to initalize the vocabulary. We did the following as prepartion:
 * Created brown clusters on the first 9999 items of wikipedia, see scripts/brown-clusters.sh
 * Created word2vec models with glove on the same corpus, see scripts/nlwiki.sh
 * Created a frequency file on the same corpus, see notebooks/CreateFrequencies.ipynb


## Ideas for further improvement
* Better brown clustering (more clusters, larger corpus)
* Calculate frequencies on larger corpus
* Better word2vec: longer vectors, larger corpus
* specifiy input for tokenizer (pre/in/suffixes etc) for Dutch (now it is copied for German)
* Throw away short sentences in the training data
* Threshold pos tags on confidence
* Create download script for Dutch language data
* Train NER
* Train DEP
* Evaluate POS. NER, DEP
* Document what we have done + performance
* Train brown clusters and add to training of tagger, ner and dep
* Why is lexemes.bin empty?
* Create vocab from wikipedia corpus as in [bin/init_model.py](https://github.com/nlesc-sherlock/spaCy/blob/master/bin/init_model.py)
* Goal: Make pull request with what we've got (so others can help)
