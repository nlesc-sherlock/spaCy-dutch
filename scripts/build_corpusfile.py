from __future__ import unicode_literals, print_function

import plac
import os

import spacy
import codecs



def main(lang_id, corpus_dir, out_file):
    #corpus_dir = Path(corpus_dir)
    #output_dir = Path(output_dir)

    #assert output_dir.exists()

    nlp = spacy.load(lang_id)
    tokenizer = nlp.tokenizer

    with codecs.open(out_file, 'w', 'utf8') as out:
        for filename in os.listdir(corpus_dir):
            with codecs.open(os.path.join(corpus_dir, filename),
                             encoding='utf-8') as f:
                data = f.read()
            doc = tokenizer(data)
            text = u' '.join([token.text for token in doc])
            out.write(text + u'\n')


if __name__ == '__main__':
    plac.call(main)