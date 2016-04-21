# This Python file uses the following encoding: utf-8
# Parse information about patent, its authors and link for it on http://www.findpatent.ru

# for parsing was used information from site inspection
import requests
import codecs
from bs4 import BeautifulSoup


def url_to_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.text.encode('utf-8'), "lxml")


# authors information is on specific patent page
def parse_for_authors(url_patent):
    soup = url_to_soup(url_patent)
    authors_items = soup.find_all('span', attrs={'itemprop': "author"})
    return [i.text for i in authors_items]


def parse_url_for_patentdata(url, url_author):
    results = []
    soup = url_to_soup(url + url_author)

    patents_list = soup.find_all('div', {'class': 'p5w100 clearfix'})
    for patent in patents_list:
        patent_link = url + patent.a.get('href')
        patent_title = patent.a.get('title')
        patent_authors = parse_for_authors(patent_link)

        results.append({
            'title': patent_title,
            'link': patent_link,
            'authors': patent_authors
        })
    return results


def main_run():
    url = 'http://www.findpatent.ru'
    url_author = '/byauthors/947427/'  # authorlink - Гречко Эдуард Никитович
    data = parse_url_for_patentdata(url, url_author)
    with codecs.open('patents.txt', 'w', 'utf-8') as output_file:
        for i, patent in enumerate(data):
            output_file.write(str(i + 1) + '. ' + patent['title'] + ' - ')
            for author in patent['authors']:
                output_file.write(author + ', ')
            output_file.write('\n' + patent['link'] + '\n')


if __name__ == "__main__":
    main_run()
