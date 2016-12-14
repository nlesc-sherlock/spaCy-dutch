# spaCy-dutch
Repository for creating models, vocabulary and other necessities for Dutch in Spacey

## Language data
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
