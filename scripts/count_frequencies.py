from __future__ import unicode_literals, print_function

import plac
from pathlib import Path
import os
from preshed.counter import PreshCounter

from spacy.attrs import ORTH

import spacy
import codecs


def count_frequencies(lang_id, corpus_dir):
    """
    Counts word count en document count for each word in the corpus.

    :param lang_id:
    :param corpus_dir: directory with text files
    :return:
    """
    nlp = spacy.load(lang_id)
    vocab = nlp.vocab
    tokenizer = nlp.tokenizer

    counts = PreshCounter()
    doccounts = PreshCounter()
    for filename in os.listdir(corpus_dir):
        with codecs.open(os.path.join(corpus_dir, filename),
                         encoding='utf-8') as f:
            data = f.read()
            doc = tokenizer(data)
            doc.count_by(ORTH, counts=counts)
            doccount = doc.count_by(ORTH)
            for k, v in doccount.iteritems():
                doccounts.inc(k, 1)

    return counts, doccounts, tokenizer

def write_frequencies(counts, doccounts, output_dir, tokenizer):
    filepath = os.path.join(output_dir, 'freqs.txt')
    with codecs.open(filepath, 'w', 'utf8') as file_:
        for orth, freq in counts:
            string = tokenizer.vocab.strings[orth]
            if not string.isspace():
                doc_freq = doccounts[orth]
                output = unicode('%d\t%s\t%s\n' % (freq, doc_freq, string))
                file_.write(output)

def main(lang_id, corpus_dir, output_dir):
    counts, doccounts, tokenizer = count_frequencies(lang_id, corpus_dir)
    write_frequencies(counts, doccounts, output_dir, tokenizer)


if __name__ == '__main__':
    plac.call(main)
