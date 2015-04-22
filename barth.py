import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# NB: BS is producing a different node structure, so ignore Chrome dev tools.
# Next, need to walk over the contents, parsing them into Sections and
# SectionContents to populate the Paragraphs.


TOC_URL = "http://solomon.dkbl.alexanderstreet.com/cgi-bin/asp/philo/dkbl/volumes_toc.pl?&church=ON"

class Paragraphs:
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
        title = soup.find(class_='head').get_text()
        abstract = '\n'.join(hibold.get_text() for hibold in soup.find_all(class_='hibold'))
        p = Paragraph(url, title, abstract)

def main(url = TOC_URL):
    for url in download_links(url, 'Table of Contents'):
        download_volume(url)

if __name__ == '__main__':
    main()
