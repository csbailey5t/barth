import os
import pickle

import nltk
from nltk.corpus import brown, names


def build_tagger(tagged_sents=None, default_tag='DEFAULT', tagger_cache=None):
    """This builds a tagger from a corpus."""
    if tagger_cache is not None and os.path.exists(tagger_cache):
        with open(tagger_cache, 'rb') as f:
            tagger = pickle.load(f)
    else:
        if tagged_sents is None:
            tagged_sents = brown.tagged_sents()

        name_tagger = [
            nltk.DefaultTagger('PN').tag([
                name.lower() for name in names.words()
            ])
        ]
        patterns = [
            (r'.*ing$', 'VBG'),               # gerunds
            (r'.*ed$', 'VBD'),                # simple past
            (r'.*es$', 'VBZ'),                # 3rd singular present
            (r'.*ould$', 'MD'),               # modals
            (r'.*\'s$', 'NN$'),               # possessive nouns
            (r'.*s$', 'NNS'),                 # plural nouns
            (r'^-?[0-9]+(.[0-9]+)?$', 'CD'),  # cardinal numbers
            (r'.*ly$', 'RB'),                       # adverbs
            # comment out the following line to raise to the surface all
            # the words being tagged by this last, default tag when you
            # run debug.py.
            (r'.*', 'NN')                     # nouns (default)
        ]

        # Right now, nothing will get to the default tagger, because the
        # regex taggers last pattern essentially acts as a default tagger,
        # tagging everything as NN.
        tagger0 = nltk.DefaultTagger(default_tag)
        regexp_tagger = nltk.RegexpTagger(patterns, backoff=tagger0)
        tagger1 = nltk.UnigramTagger(tagged_sents, backoff=regexp_tagger)
        tagger2 = nltk.BigramTagger(tagged_sents, backoff=tagger1)
        tagger3 = nltk.UnigramTagger(name_tagger, backoff=tagger2)

        tagger = tagger3
        if tagger_cache is not None:
            with open(tagger_cache, 'wb') as f:
                pickle.dump(tagger, f, pickle.HIGHEST_PROTOCOL)

    return tagger
