import requests
import sqlalchemy.exc
from bs4 import BeautifulSoup as BS
from models import DBSession, Category, Article
import json
from tqdm import tqdm

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    'referer': 'https://fr.wikihow.com'
}

domain = 'https://fr.wikihow.com'
s = requests.session()


def scrape_categories(DBSession):
    categories = []
    soup = BS(s.get("https://fr.wikihow.com/Accueil", headers=headers).text, 'html.parser')
    for l in soup.findAll('li', {'class': 'cat_icon'}):
        categories.append({"category": l.text.strip(), "link": l.find('a').get('href')})
    for x in categories:
        DBSession.add(Category(name=x.get("category"), link=f'{domain}{x.get("link")}'))
    DBSession.commit()


if __name__ == '__main__':
    scrape_categories(DBSession)
    categories = DBSession.query(Category).all()

    for c in categories:
        articles_soup = BS(s.get(c.link, headers=headers).text, 'html.parser')
        articles = articles_soup.findAll('div', {'class': 'responsive_thumb'})
        for a in tqdm(articles):
            soup = BS(s.get(a.find('a').get("href"), headers=headers).text, 'html.parser')
            title = soup.select_one('#section_0 > a').text
            brief = soup.select_one('#mf-section-0 > p').text
            body = soup.select_one('#mf-section-1')

            try:
                outro = soup.select_one('#conseils').findAll('li')
            except AttributeError:
                outro = '[]'
            description = soup.find('meta', {'name': 'description'}).get("content")
            viewport = soup.find('meta', {'name': 'viewport'}).get("content")
            seo_title = soup.find('title').text
            seo_og_description = soup.find('meta', {'property': 'og:description'}).get("content")

            DBSession.add(
                Article(title=title, link=a.find('a').get("href"), brief=brief, outro=str(outro), body=str(body),
                        seo=json.dumps({'description': description, 'viewport': viewport, 'title': seo_title,
                                        'seo_og_description': seo_og_description}), category_id=c.id, lang='fr'))

            try:
                DBSession.commit()
            except sqlalchemy.exc.IntegrityError:
                DBSession.rollback()
                continue
