import json

with open("tests/assets/cached_news.json") as arquivo:
    all_news = json.load(arquivo)

with open("tests/assets/cached_urls.json") as arquivo:
    urls_from_novidades = json.load(arquivo)
