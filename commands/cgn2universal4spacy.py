#!/usr/bin/env python
import click
import codecs

import pandas as pd

from nlppln.utils import create_dirs

tag_mapping = {
    'ADJ': 'ADJ',  # adjective
    'TW(rang': 'ADJ',  # adjective (rangtelwoord) rangtelwoord kan ook adverb zijn?
    'BW': 'ADV',  # adverb (bijwoord)
    'TSW': 'INTJ',  # interjection (tussenwerpsel)
    'N(soort': 'NOUN',  # noun (substantief (zelfstandig naamwoord))
    'N(eigen': 'PROPN',   # proper noun (eigennaam)
    'WW': 'VERB',  # verb (werkwoord)
    'VZ': 'ADP',  # adposition (voorzetsel (preposition))
    #: 'AUX',  # auxiliary verb (hulpwerkwoord -> not available in CGN)
    'VG(neven)': 'CONJ',  # coordinating conjunction (neveschikkend voegwoord)
    'LID': 'DET',  # determiner (lidwoorden, telwoorden, aanwijzende voornaamwoorden, bezittelijke voornaamwoorden, en kwantoren)
    'TW(hoofd': 'NUM',  # numeral (hoofdtelwoord)
    : 'PART',  # particle
    'VNW': 'PRON',  # pronoun (voornaamwoord)
    'VG(onder)': 'SCONJ'  # subordinating conjunction (onderschikkend voegwoord)
    'LET': 'PUNCT',  # punctuation (leesteken)
    : 'SYM',  # symbol
    'SPEC': 'X'  # other (speciale tekens)
}


@click.command()
@click.argument('meta_in', type=click.Path(exists=True))
@click.argument('meta_out', nargs=1, type=click.Path())
def command(meta_in, meta_out):
    create_dirs(meta_out)

    cgn_tags = pd.read_csv(meta_in, index_col=0, encoding='utf-8')

    heads = []

    for tag in cgn_tags.index:
        click.echo(tag)
        head = tag.split('(')[0]
        heads.append(head)

    click.echo(set(heads))

    #with codecs.open(meta_out, 'wb', encoding='utf-8') as f:
    #    pass


if __name__ == '__main__':
    command()
