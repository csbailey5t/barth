"""\
This contains a Corpus class that walks over a directory tree and
returns the file names and tokens.

- tags (parent directory name)
- tokens

"""


from collections import namedtuple
import os

import nltk
from nltk.corpus import stopwords


FileTokens = namedtuple('FileTokens', ['filename', 'tag', 'tokens'])


def get_english_stopset():
    """Return a set of English stop words."""
    return set(stopwords.words('english'))


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
