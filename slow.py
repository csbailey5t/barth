import requests
from bs4 import BeautifulSoup

def main():

    page = requests.get('http://solomon.dkbl.alexanderstreet.com/cgi-bin/asp/philo/dkbl/getobject.pl?c.830:1.barth')
    soup = BeautifulSoup(page.text)

    head = soup.find('span', {'class': 'head'})

    body = head.parent

    paragraph_text = body.get_text()

    f = open('part_volume_one.txt', 'w')
    f.write(paragraph_text)
    f.close()

if __name__ == '__main__':
    main()
