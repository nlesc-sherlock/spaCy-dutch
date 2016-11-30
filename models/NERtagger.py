"""
Use:
python NERtagger.py /path/to/CONLLdata/ /path/to/store/model
"""

from spacy.pipeline import EntityRecognizer
from spacy.tokens import Doc
from spacy.gold import GoldParse
import spacy
import codecs
import json
import os
from spacy.nl import Dutch

LABELS = ['PER', 'LOC', 'ORG', 'MISC', 'PRO', 'EVE']

def bio_to_biluo(labels):
    """
    Converts BIO tagging to BILUO tagging

    :param labels:
    :return:
    """
    output = [x for x in labels]
    labels = ['O'] + labels + ['O']
    for i in range(0, len(labels) - 1):
        if labels[i + 1] == 'O' and labels[i][0] == 'B':
            output[i - 1] = 'U' + output[i - 1][1:]
        if labels[i + 1][0] != 'I' and labels[i][0] == 'I':
            output[i - 1] = 'L' + output[i - 1][1:]

    return output

def read_connl(filepath, vocab):
    """
    Reads the CONLL 2002 data and creates Doc objects for each sentence.
    Also reads the entitiy labels.

    :param filepath:
    :param vocab:
    :return:
    """
    docs = []
    entities = []
    postags = []
    f = codecs.open(filepath, encoding='ISO-8859-15')

    doc_list = []
    entities_list = []
    postags_list = []
    for line  in f:
        splitted = line.split(' ')
        if len(splitted)!=3 or splitted[0] == '-DOCSTART-':
            if(len(doc_list)>0):
                docs.append(Doc(vocab, words=doc_list))
                entities.append(bio_to_biluo(entities_list))
                postags.append(postags_list)
                doc_list = []
                entities_list = []
                postags_list = []
        else:
            word, pos, label = splitted
            doc_list.append(unicode(word))
            postags_list.append(pos.strip())
            entities_list.append(label.strip())
    docs.append(Doc(vocab, doc_list))
    entities.append(entities_list)
    print('CONNL dataset loaded.')
    return docs, postags, entities


def train_NER(filepath, vocab, iterations=20):
    print("Training {} iterations".format(iterations))
    docs, entities = read_connl(filepath, vocab)
    ner = EntityRecognizer(vocab, entity_types=LABELS)
    for i in range(iterations):
        if i%5 == 0:
            print("Iteration {}...".format(i))
        for doc, entity_list in zip(docs, entities):
            ner.update(doc, GoldParse(doc, entities=entity_list))
    print("Done training.")
    return docs, ner

def save_model(ner, model_dir):
    with open(os.path.join(model_dir, 'config.json'), 'w') as file_:
        json.dump(ner.cfg, file_)
    ner.model.dump(os.path.join(model_dir, 'model'))

if __name__ == '__main__':
    import sys
    #filepath = '/media/sf_VBox_Shared/nlppln/NER/'
    filepath = sys.argv[1]
    model_dir = sys.argv[2]

    filepath_train = filepath+'ned.train'
    filepath_test = filepath+'ned.testa'

    vocab = spacy.load('nl').vocab
    docs, ner = train_NER(filepath_train, vocab, iterations=30)
    docs_test, entities_test = read_connl(filepath_test, vocab)

    save_model(ner, model_dir)
    # Print example tagging:
    doc = docs_test[2]
    ner(doc)
    for word in doc:
        print(word.text, word.tag_, word.ent_type_, word.ent_iob)