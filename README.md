# spaCy-dutch
Repository for creating models, vocabulary and other necessities for Dutch in Spacey

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
