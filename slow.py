import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import shutil
import re

TOC_URL = "http://solomon.dkbl.alexanderstreet.com/cgi-bin/asp/philo/dkbl/volumes_toc.pl?&church=ON"

def write_paragraph(filename, text, dirname='paragraphs'):
    completeName = os.path.join(dirname, filename+'.txt')
    print('Writing ' + completeName)
    with open(completeName, 'w') as f:
        f.write(text)

def get_paragraph_number(soup):
    node = soup.find('a', {'name': True})
    if node is None:
        return None

    loc = node.next_sibling.next_sibling
    match = re.search(r'\d+', loc.text)
    if match:
        paragraph = int(match.group(0))
    else:
        paragraph = 0
    return paragraph

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
        head = soup.find('span', {'class': 'head'})
        title = head.get_text()

        if title is None:
            raise Exception('No <span class=head> found.')
        if (title == "EDITORS' PREFACE"):
            continue

        filename = title.replace(' ', '_').lower()
        number = str(get_paragraph_number(soup))
        filename = number + '.' + filename

        abstract = '\n'.join(hibold.get_text() for hibold in soup.find_all(class_='hibold'))
        content = head.parent
        paragraph_text = content.get_text()


        write_paragraph(filename, paragraph_text)

def main(url = TOC_URL):

    shutil.rmtree('paragraphs')
    os.makedirs('paragraphs')

    volume_links = list(download_links(url, 'Table of Contents'))
    for url in volume_links[:-2]:
        download_volume(url)


if __name__ == '__main__':
    main()
