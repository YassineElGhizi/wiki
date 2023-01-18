import requests
import base64
from models import DBSession, Article
from bs4 import BeautifulSoup as BS
import json
from clean import clean
from tqdm import tqdm


def translate_article(body: str, source: str):
    try:
        encoded = base64.b64encode(bytes(body, 'utf-8'))
        encodedStr = encoded.decode('utf-8')

        urll = "https://09ab-62-210-99-231.ngrok.io"
        contents = {
            "source": source,
            "dest": "English",
            "text": encodedStr,
            "version": "free"
        }
        req = requests.post(urll, json=contents)
        decoded = base64.b64decode(bytes(req.text, 'utf-8'))
        return decoded.decode('utf-8')
    except Exception as e:
        print(f'[-] Translator Exception :: {e}')
        return -1


if __name__ == '__main__':
    translated_ids = [a.id_parent for a in DBSession.query(Article).filter(Article.id_parent != None)]
    articles = DBSession.query(Article).filter(
        ~Article.id.in_(translated_ids),
        Article.category_id == 15
    ).all()

    for article in tqdm(articles):
        text = BS(article.body, 'html.parser')
        if len(text.text.strip()) == 0:
            continue

        title_en = translate_article(article.title, 'French')
        if title_en == -1:
            continue

        text_en = translate_article(text.text.strip(), 'French')
        if text_en == -1:
            continue

        brief_en = translate_article(article.brief, 'French').strip()
        if brief_en == -1:
            continue

        lis = article.outro[1:-1].split('</li>,')
        if len(lis) == 0:
            continue

        outros = []
        for x in lis:
            elem = translate_article(x.replace('<li>', '').replace('</li>', ''), 'French')
            if elem != -1:
                outros.append(elem)

        seo = json.loads(article.seo)
        seo_description = translate_article(seo.get("description"), 'French')
        if seo_description == -1:
            continue

        seo_title = translate_article(seo.get("title"), 'French')
        if seo_title == -1:
            continue

        seo_seo_og_description = translate_article(seo.get("seo_og_description"), 'French')
        if seo_seo_og_description == -1:
            continue

        a = Article(
            title=title_en.strip(),
            brief=brief_en.strip(),
            outro=str(outros).strip(),
            body=text_en.strip(),
            seo=json.dumps({"description": seo_description, "viewport": seo.get("viewport"), "title": seo_title,
                            "seo_og_description": seo_seo_og_description}),
            lang='en',
            id_parent=article.id,
            category_id=article.category_id
        )
        DBSession.add(a)
        DBSession.commit()
