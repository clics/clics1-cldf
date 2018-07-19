# coding=utf-8
from __future__ import unicode_literals, print_function
from itertools import groupby

import attr
import lingpy
from pycldf.sources import Source

from clldutils.path import Path
from clldutils.misc import slug
from pylexibank.dataset import Metadata, Concept
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import pb, getEvoBibAsBibtex


class Dataset(BaseDataset):
    dir = Path(__file__).parent

    def cmd_download(self, **kw):
        src = {}
        for k in ['List2014f', 'Wold2009', 'Logos2008', 'Key2007',
                'Saxena2013']:
            src[k] = getEvoBibAsBibtex(k)
        self.raw.write(
                'sources.bib', 
                '\n\n'.join(src.values())
                )

    def cmd_install(self, **kw):
        wl = lingpy.Wordlist(self.raw.posix('D_old-clics.tsv'))

        src = {
                'wold': 'Wold2009',
                'ids': 'Key2007',
                'logos': 'Logos2008',
                'Språkbanken': 'Saxena2013'
                }

        with self.cldf as ds:
            ds.add_sources(*self.raw.read_bib())
            for k in pb(wl, desc='wl-to-cldf'):
                if wl[k, 'value']:
                    ds.add_language(
                        ID=slug(wl[k, 'doculect']),
                        Name=wl[k, 'doculect'],
                        Glottocode=wl[k, 'glottolog'])
                    ds.add_concept(
                        ID=slug(wl[k, 'concept']),
                        Name=wl[k, 'concept'],
                        Concepticon_ID=wl[k, 'concepticon_id']
                        )
                    ds.add_lexemes(
                        Language_ID=slug(wl[k, 'doculect']),
                        Parameter_ID=slug(wl[k, 'concept']),
                        Value=wl[k, 'value'],
                        Form=wl[k, 'value'],
                        Source=src.get(wl[k, 'source'], ''))
