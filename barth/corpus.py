"""\
This contains a Corpus class that walks over a directory tree and
returns the file names and tokens.

- tags (parent directory name)
- tokens

"""


from collections import namedtuple
import csv
import os

import nltk
from nltk.corpus import stopwords
import pandas
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


CSV_FIELD_LIMIT = 131072 * 4


FileTokens = namedtuple('FileTokens', ['filename', 'tag', 'tokens'])


def get_english_stopset():
    """Return a set of English stop words."""
    return set(stopwords.words('english'))


def normalize(token):
    if token[0].isdigit():
        return '###'
    else:
        return token.lower()


def tokenize(text):
    return [normalize(t) for t in nltk.wordpunct_tokenize(text)]


# TODO: We may be able to pull out the directory walker from the
# tokenizer/tagger/stoplist filter.

class Corpus:

    def __init__(self, dirnames, tagger=None, stopset=None):
        """dirnames is a list of directory names"""
        self.dirnames = dirnames
        self.tagger = tagger
        self.stopset = stopset

    def get_tag(self, filename):
        """Given a file name, return the tag to classify it as."""
        return os.path.basename(os.path.dirname(filename))

    def tokenize(self, text):
        """Returns the tokens for a text."""
        tokens = nltk.wordpunct_tokenize(text)

        if self.tagger:
            tags = self.tagger(tokens)
            if self.stopset:
                tags = [
                    tag for tag in tags if tag[0].lower() not in self.stopset
                ]
        elif self.stopset:
            tags = [tag for tag in tokens if tag.lower() not in self.stopset]
        else:
            tags = tokens

        return tags

    def walk_corpus(self):
        """This iterates over the files in the corpus."""
        for dirname in self.dirnames:
            for (root, files, dirs) in os.walk(dirname):
                for filename in files:
                    filename = os.path.join(root, filename)
                    yield filename

    def tokenize_corpus(self):
        """\
        This iterates over the directories and returns each file's FileTokens.

        """
        for filename in self.walk_corpus():
            with open(filename) as f:
                yield FileTokens(
                    filename,
                    self.get_tag(filename),
                    self.tokenize(f.read()),
                )


class CsvCorpus:
    KEYS = [
        'volume_n', 'part', 'chapter_n', 'paragraph_n', 'chunk_n', 'block_n',
    ]

    def __init__(self, csv_file, tagger=None, stopset=None):
        self.csv_file = csv_file
        self.__data = None
        self.tagger = tagger
        self.stopset = stopset

    def _read_data(self, csv_file=None):
        csv.field_size_limit(CSV_FIELD_LIMIT)
        csv_file = self.csv_file if csv_file is None else csv_file
        data_dir = os.path.dirname(csv_file)

        with open(csv_file, 'r') as fin:
            rows = list(csv.DictReader(fin))
        for row in rows:
            row['loc'] = '.'.join(row[k] for k in self.KEYS if k in row)
            if 'text' not in row:
                filename = os.path.join(data_dir, row['filename'])
                with open(filename) as text_fin:
                    row['text'] = text_fin.read()

        df = pandas.DataFrame(
            rows,
            columns=[
                'filename', 'loc', 'volume_title', 'chapter_title',
                'paragraph_title', 'text',
            ],
            index=[r['loc'] for r in rows],
        )

        return df

    def _map(self, fn, src, dest=None):
        dest = dest or src
        data = self.data
        data[dest] = [fn(v) for v in data[src]]
        return data

    def _over(self, fn, src, dest=None):
        dest = dest or src
        data = self.data
        data[dest] = fn(data[src])
        return data

    def _over_rows(self, fn, dest):
        data = self.data
        data[dest] = [fn(row) for (_, row) in data.iterrows()]
        return data

    def _map_tokens(self, fn):
        self.tokenize()
        return self._map(fn, 'tokens')

    @property
    def data(self):
        if self.__data is None:
            self.__data = self._read_data()
        return self.__data

    def tokenize(self):
        df = self.data
        if 'tokens' not in df:
            df = self._map(tokenize, 'text', 'tokens')
        return df

    def filter_stopset(self, stopset=None):
        stopset = self.stopset if stopset is None else stopset
        if stopset is None:
            raise ValueError(
                'You must specify a stopset before calling filter_stopset.',
            )

        return self._map_tokens(
            lambda text: [t for t in text if t not in stopset],
        )

    def filter_short(self, length=2):
        """Removes words of length or shorter."""
        return self._map_tokens(
            lambda text: [t for t in text if len(t) > length],
        )

    def tag_rows(self, fn, col='tag'):
        """Adds a column with the tag, generated by fn."""
        self._over_rows(fn, col)

    def tag_tokens(self, tagger=None):
        tagger = self.tagger if tagger is None else tagger
        if tagger is None:
            raise ValueError(
                'You must specify a tagger before calling tag_tokens.',
            )

        def tag(tokens):
            return [
                '{}/{}'.format(*tt) for tt in tagger.tag(tokens)
            ]

        return self._map_tokens(tag)

    def count_vectorize(self, **kwargs):
        df = self.tokenize()
        corpus = [' '.join(doc) for doc in df['tokens']]
        cv = CountVectorizer(**kwargs)
        counts = cv.fit_transform(corpus)
        cdf = pandas.DataFrame(
            counts.toarray(),
            columns=cv.get_feature_names(),
            index=df.index,
        )

        return cdf

    def tfidf_vectorize(self, **kwargs):
        df = self.tokenize()
        corpus = [' '.join(doc) for doc in df['tokens']]
        tf = TfidfVectorizer(**kwargs)
        counts = tf.fit_transform(corpus)
        cdf = pandas.DataFrame(
            counts.toarray(),
            columns=tf.get_feature_names(),
            index=df.index,
        )

        return cdf


if __name__ == '__main__':
    import barth.tagging
    tagger = barth.tagging.build_tagger()
    # tagger = None
    corpus = CsvCorpus(
        'data/corpus.csv', tagger=tagger, stopset=get_english_stopset(),
    )
    counts = corpus.count_vectorize(ngram_range=(1, 3))
    print(corpus.data)
    print(counts)
    tfidf = corpus.tfidf_vectorize(ngram_range=(1, 3))
    print(tfidf)
