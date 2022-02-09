from tech_news.scraper import (
    fetch,
    scrape_novidades,
    scrape_noticia,
    scrape_next_page_link,
    get_tech_news,
)
from tech_news.database import db
from tests.assets.test_assets import (
    all_news,
    urls_from_novidades,
)
import time
import pytest
import pickle
from requests.exceptions import ReadTimeout


# Req.1
def test_fetch(mocker):
    # executada com uma URL correta retorna o conteúdo html
    path = "tests/assets/betrybe_response.pickle"
    with open(path, "rb") as response_file:
        response = pickle.load(response_file)
    mocker.patch("requests.get", return_value=response)
    result = fetch("https://app.betrybe.com/")
    assert "<!doctype html>" in result
    content = (
        "Aprenda a programar com uma formação de alta"
        " qualidade e só comece a pagar quando conseguir um bom"
        " trabalho."
    )
    assert content in result

    # sofrendo timeout, retorna None
    mocker.patch("requests.get", side_effect=ReadTimeout)
    assert fetch("https://httpbin.org/delay/5") is None

    # retorna None quando recebe uma resposta com código
    # diferente de 200
    path = "tests/assets/404_response.pickle"
    with open(path, "rb") as response_file:
        response = pickle.load(response_file)
    mocker.patch("requests.get", return_value=response)
    assert fetch("https://httpbin.org/status/404") is None

    # respeita o rate limit
    mocker.patch("requests.get")
    start = time.time()
    request_counter = 0
    while (time.time() - start) < 4:
        fetch("http://www.google.com.br")
        request_counter += 1
    assert request_counter <= 5


# Req.2
def test_scrape_novidades():
    with open("tests/assets/tecmundo_pages/novidades.html") as f:
        html_content = f.read()
    expected = urls_from_novidades
    # retorna os dados esperados quando chamada com os parâmetros corretos
    assert scrape_novidades(html_content) == expected
    # retorna uma lista vazia quando chamada com parâmetros incorretos
    assert scrape_novidades("") == []


# Req.3
def test_scrape_next_page_link():
    with open("tests/assets/tecmundo_pages/novidades.html") as f:
        html_content = f.read()
    expected = "https://www.tecmundo.com.br/novidades?page=2"
    # retorna os dados esperados quando chamada com os parâmetros corretos
    assert scrape_next_page_link(html_content) == expected
    # retorna None quando chamada com os parâmetros incorretos
    assert scrape_next_page_link("") is None


@pytest.fixture
def noticia_html_v1():
    path = (
        "tests/"
        "assets/"
        "tecmundo_pages/"
        "dispositivos-moveis|"
        "215327-pixel-5a-tera-lancamento-limitado-devido-escassez-chips.htm."
        "html"
    )
    with open(path) as f:
        return f.read()


@pytest.fixture
def noticia_html_v2():
    path = (
        "tests/"
        "assets/"
        "tecmundo_pages/"
        "minha-serie|"
        "215168-10-viloes-animes-extremamente-inteligentes.htm."
        "html"
    )
    with open(path) as f:
        return f.read()


@pytest.fixture
def noticia_html_v3():
    path = (
        "tests/"
        "assets/"
        "tecmundo_pages/"
        "seguranca|"
        "215274-pmes-principais-alvos-ataques-ciberneticos.htm."
        "html"
    )
    with open(path) as f:
        return f.read()


# Req.4
def test_scrape_noticia(noticia_html_v1, noticia_html_v2, noticia_html_v3):
    assert scrape_noticia(noticia_html_v1) == all_news[15]
    assert scrape_noticia(noticia_html_v2) == all_news[1]
    assert scrape_noticia(noticia_html_v3) == all_news[11]


def mocked_fetch(url):
    """Fake-fetches html from local file caches"""
    skip = len("https://www.tecmundo.com.br/")
    file_id = url[skip:].replace("/", "|")
    path = f"tests/assets/tecmundo_pages/{file_id}.html"
    with open(path) as cached_html:
        return cached_html.read()


# Req.5
@pytest.mark.parametrize("amount", [20, 30, 40])
def test_get_tech_news(amount, mocker):
    # Arrange
    db.news.drop()
    mocker.patch("tech_news.scraper.fetch", new=mocked_fetch)
    mocked_create_news = mocker.patch("tech_news.scraper.create_news")

    # Act
    result = get_tech_news(amount)
    mocked_create_news.assert_called_once_with(result)

    # Assert
    # A função retorna a quantidade correta de notícias
    assert result == all_news[:amount]  # resultados originais
