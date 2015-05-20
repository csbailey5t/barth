import requests
from lxml import etree
from urllib.parse import urljoin
import re
import json
import os
import shutil
import itertools


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

    def write(self, soup):
        loc = find_title(soup)
        filename = make_title(loc)
        print('Writing {} to {}'.format(loc, filename))
        with open(filename, 'w') as f:
            json.dump(self, f, cls=JSONEncoder, indent=2)
        with open(filename + '.html', 'w') as f:
            f.write(etree.tostring(
                soup,
                pretty_print=True,
                method='html'
                ).decode('utf8'))

    @staticmethod
    def parse(url, soup):
        heads = list(find_spans(soup, 'head'))
        para_head = heads.pop(0)
        abstract = '\n'.join(
            get_text(div) for div in para_head.itersiblings('div')
            )

        para = Paragraph(url, get_text(para_head), abstract)
        para.sections += (
            Section.parse(section_head) for section_head in heads
            )

        return para


class Section:

    def __init__(self, number, title, contents=None):
        self.number = number
        self.title = title
        self.contents = contents or []

    @staticmethod
    def parse(head):
        # TODO: find section numbers
        section = Section(None, get_text(head))
        section.contents += itertools.chain.from_iterable(
            SectionContents.parse(sibling) for sibling in head.itersiblings()
            )
        return section


class SectionContents:

    EXCURSUS = 0
    TEXT = 1
    PAGE_BREAK = 2

    def __init__(self, content_type, data):
        self.content_type = content_type
        self.data = data

    @staticmethod
    def parse(tag):
        content_type = SectionContents.TEXT
        if tag.get('class') == 'excursus':
            content_type = SectionContents.EXCURSUS

        for seg in re.split(r'(-- - --)', get_text(tag)):
            if '--' in seg:
                # TODO: handle page numbers
                yield SectionContents(SectionContents.PAGE_BREAK, None)
            else:
                yield SectionContents(content_type, seg)


class JSONEncoder(json.JSONEncoder) :
    def default(self, obj) :
        if isinstance(obj, (Paragraph, Section, SectionContents)) :
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


def download_links(url, link_text):
    page = requests.get(url)
    soup = etree.HTML(page.text)

    for a in soup.findall('.//a'):
        if link_text in ''.join(a.itertext()):
            yield urljoin(page.url, a.get('href'))

def find_title ( soup ):
    node = soup.find('.//a[@name]')
    if node is None:
        return None

    (paragraph, volume)  = list(node.itersiblings('i'))
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

def find_span(el, class_):
    return el.find(".//span[@class='{}']".format(class_))

def find_spans(el, class_):
    return el.findall(".//span[@class='{}']".format(class_))


def get_text(el):
    return ''.join(el.itertext())


def download_volume(parent_url):
    for url in download_links(parent_url, 'View Text'):
        # print('Downloading {}'.format(url))
        resp = requests.get(url)
        soup = etree.HTML(resp.text)
        title = find_span(soup, 'head')
        if title is None:
            raise Exception('No <span class="head"> found.')
        if (get_text(title) == "EDITORS' PREFACE") :
            continue

        page = Paragraph.parse(url, soup)
        page.write(soup)


def main(url = TOC_URL):
    shutil.rmtree('output')
    os.makedirs('output')
    for url in download_links(url, 'Table of Contents'):
        download_volume(url)

if __name__ == '__main__':
    main()
