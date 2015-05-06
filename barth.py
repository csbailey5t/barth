import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import json
import os
import shutil


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

def find_title ( soup ):
    node = soup.find(is_a_name)
    if node is None:
        return None

    (paragraph, volume)  = node.find_next_siblings('i')
    match = re.search(r'\d+', paragraph.text)
    if match:
        paragraph = int(match.group(0))
    else:
        paragraph = 0

    match = re.search(r'([IVX]+),(\d+)', volume.text)
    volume = match.group(1)
    part_volume = int(match.group(2))

    return (volume, part_volume, paragraph)

def make_title( loc, dirname='output', ext='json' ):
    (v, pv, p) = loc
    n = 0
    template = os.path.join(dirname, '{}-{:02}-{:02}-{{}}.{}'.format(v, pv, p, ext))
    while True:
        filename = template.format(n)
        if not os.path.exists(filename):
            return filename
        n += 1

def is_a_name ( node ):
    return node.name == 'a' and node.has_attr('name')

def download_volume(url):
    for url in download_links(url, 'View Text'):
        page = requests.get(url)
        soup = BeautifulSoup(page.text)
        loc = find_title( soup )
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
        filename = make_title( loc )
        print('Writing {} to {}'.format( loc, filename ))
        with open(filename, 'w') as f:
            json.dump(page, f, cls=JSONEncoder)
        # raise SystemExit()


def main(url = TOC_URL):
    shutil.rmtree('output')
    os.makedirs('output')
    for url in download_links(url, 'Table of Contents'):
        download_volume(url)

if __name__ == '__main__':
    main()
