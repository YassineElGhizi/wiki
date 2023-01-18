from models import DBSession, Article
import re


def clean(body):
    boiler_plate = []
    for elem in body.split("\n"):
        if elem not in ['', 'X', '.']:
            if not 'https' in elem and not 'Advertisement' in elem and not 'Advertising' in elem and not 'div>' in elem:
                boiler_plate.append(
                    re.sub("\(.*?\)|\[.*?\]", "", elem).strip().replace(". ", "").replace("!", "")
                )

    return "\n".join(boiler_plate)


# if __name__ == '__main__':
#     boiler_plate = []
#     article = DBSession.query(Article).filter(Article.id_parent == 1).first()
#     print(article.body)

# for elem in article.body.split("\n"):
#     if elem not in ['', 'X', '.']:
#         if not 'https' in elem and not 'Advertisement' in elem:
#             boiler_plate.append(
#                 re.sub("\(.*?\)|\[.*?\]", "", elem).strip().replace(". ", "").replace("!", "")
#             )
#
# pussy = "\n".join(boiler_plate)
# print(pussy)
