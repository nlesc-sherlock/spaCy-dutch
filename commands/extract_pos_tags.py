#!/usr/bin/env python
import click
import json
import codecs
import pandas as pd

from collections import Counter

from nlppln.utils import create_dirs


@click.command()
@click.argument('in_files', nargs=-1, type=click.Path(exists=True))
@click.argument('meta_out', nargs=1, type=click.Path())
def command(in_files, meta_out):
    create_dirs(meta_out)

    pos_tags = Counter()

    for fi in in_files:
        with codecs.open(fi, 'rb', encoding='utf-8') as f:
            saf = json.load(f)
            for t in saf.get('tokens', []):
                pos = t.get('pos')
                tags = pos.split('_')
                for tag in tags:
                    pos_tags[tag] += 1

    data = pd.DataFrame.from_dict(pos_tags, orient='index')
    data.columns = ['frequency']

    data = data.sort_index()

    with codecs.open(meta_out, 'wb', encoding='utf-8') as f:
        data.to_csv(f, encoding='utf-8')


if __name__ == '__main__':
    command()
