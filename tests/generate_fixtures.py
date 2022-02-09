# Este arquivo é usado para gerar a fixture usada nos testes do projeto
import json
import pickle
from unittest.mock import patch
import requests
from tech_news.scraper import get_tech_news
from tests.test_scraper import mocked_fetch


with patch("tech_news.scraper.create_news"), patch(
    "tech_news.scraper.fetch", side_effect=mocked_fetch
):
    news = get_tech_news(40)

with open("tests/assets/cached_news.json", "w") as cached_news:
    json.dump(news, cached_news)

# betrybe response (pickled)
response = requests.get("https://app.betrybe.com")
with open("tests/assets/betrybe_response.pickle", "wb") as response_file:
    pickle.dump(response, response_file)

# httpbin 404 response (pickled)
response = requests.get("https://httpbin.org/status/404")
with open("tests/assets/404_response.pickle", "wb") as response_file:
    pickle.dump(response, response_file)
