import attr
import lingpy

from pathlib import Path
from clldutils.misc import slug
from pylexibank import progressbar
from pylexibank import Dataset as BaseDataset

from pyconcepticon.api import Concepticon


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = 'clics1'

    def cmd_makecldf(self, args):
        wl = lingpy.Wordlist(
                self.raw_dir.joinpath('D_old-clics.tsv').as_posix())
        args.log.info('loaded wordlist')

        src = {
                'wold': 'Wold2009',
                'ids': 'Key2007',
                'logos': 'Logos2008',
                'Språkbanken': 'Saxena2013'
                }
        args.writer.add_sources()
        
        concepts = set()
        languages = set()
        concepticon = {c.id: c.gloss for c in
                Concepticon().conceptsets.values()}
        args.log.info('added concepticon')
        for k in progressbar(wl, desc='wl-to-cldf'):
            if wl[k, 'value']:
                if wl[k, 'doculect'] not in languages:
                    args.writer.add_language(
                        ID=slug(wl[k, 'doculect'], lowercase=False),
                        Name=wl[k, 'doculect'],
                        Glottocode=wl[k, 'glottolog'])
                    languages.add(wl[k, 'doculect'])
                if wl[k, 'concept'] not in concepts:
                    args.writer.add_concept(
                        ID=slug(wl[k, 'concept'], lowercase=False),
                        Name=wl[k, 'concept'],
                        Concepticon_ID=wl[k, 'concepticon_id'],
                        Concepticon_Gloss=concepticon.get(
                            wl[k, 'concepticon_id'],
                            '')
                        )
                    concepts.add(wl[k, 'concept'])
                args.writer.add_lexemes(
                    Language_ID=slug(wl[k, 'doculect'], lowercase=False),
                    Parameter_ID=slug(wl[k, 'concept'], lowercase=False),
                    Value=wl[k, 'value'],
                    Source=src.get(wl[k, 'source'], '')
                    )
