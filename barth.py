import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import json


# NB: BS is producing a different node structure, so ignore Chrome dev tools.
# Next, need to walk over the contents, parsing them into Sections and
# SectionContents to populate the Paragraphs.


TOC_URL = "http://solomon.dkbl.alexanderstreet.com/cgi-bin/asp/philo/dkbl/volumes_toc.pl?&church=ON"

class Paragraph:
    def __init__(self, url, title, abstract, sections=None):
        self.url = url
        self.title = title
        self.abstract = abstract
        self.sections = sections or []

class Section:
    def __init__(self, number, title, contents=None):
        self.number = number
        self.title = title
        self.contents = contents or []

class SectionContents:
    EXCURSUS = 0
    TEXT = 1
    PAGE_BREAK = 2

    def __init__(self, content_type, data):
        self.content_type = content_type
        self.data = data

class JSONEncoder(json.JSONEncoder) :
    def default(self, obj) :
        if isinstance(obj, (Paragraph, Section, SectionContents)) :
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


def download_links(url, link_text):
    page = requests.get(url)
    soup = BeautifulSoup(page.text)

    for a in soup.find_all('a'):
        if link_text in a.get_text():
            yield urljoin(page.url, a['href'])

def download_volume(url):
    for url in download_links(url, 'View Text'):
        page = requests.get(url)
        soup = BeautifulSoup(page.text)
        title = soup.find(class_='head')
        if (title.get_text() == "EDITORS' PREFACE") :
            continue

        # open('filename.html', 'w').write(soup.prettify())
        # raise SystemExit()

        abstract = '\n'.join(hibold.get_text() for hibold in soup.find_all(class_='hibold'))
        page = Paragraph(url, title.get_text(), abstract)
        section = Section(None, None)
        page.sections.append(section)
        div = title.find_next_sibling('div')
        # TODO: find section numbers and start new Section objects
        for p in div :
            if hasattr(p, 'get_text') :
                # TODO: handle page numbers
                for seg in re.split(r'(-- - --)', p.get_text()) :
                    if '--' in seg :
                        section.contents.append(SectionContents(SectionContents.PAGE_BREAK, None))
                    else :
                        section.contents.append(SectionContents(SectionContents.TEXT, seg))
        # TODO: get unique file names (from the paragraph #) to write each paragraph to a new file
        open('preface.json', 'w').write(json.dumps(page, cls=JSONEncoder))
        raise SystemExit()


def main(url = TOC_URL):
    for url in download_links(url, 'Table of Contents'):
        download_volume(url)

if __name__ == '__main__':
    main()
