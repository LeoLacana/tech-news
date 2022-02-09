# flake8: noqa

from unittest.mock import patch
from tech_news.menu import analyzer_menu
from tech_news.scraper import fetch
from pymongo import MongoClient
from decouple import config

DB_HOST = config("DB_HOST", default="localhost")
DB_PORT = config("DB_PORT", default="27017")

client = MongoClient(host=DB_HOST, port=int(DB_PORT))
db = client.tech_news

NEW_NOTICE = {
    "url": "https://www.tecmundo.com.br/brincadeira-levadaserio.htm",
    "title": "Yakuza Like a Dragon era beat em up",
    "timestamp": "2020-11-23T11:00:01",
    "writer": "André Luis Dias Custodio",
    "shares_count": 0,
    "comments_count": 0,
    "summary": "Sumario da noticia",
    "sources": ["ResetEra"],
    "categories": ["Plataformas", "PC", "Console"],
}

NEW_NOTICE_ANALYZER = {
    "url": "https://www.tecmundo.com.br/vamos.htm",
    "title": "Vamoscomtudo",
    "timestamp": "2020-11-23T11:00:01",
    "writer": "Leonardo",
    "shares_count": 1,
    "comments_count": 1,
    "summary": "Sumario 2",
    "sources": ["ResetEra"],
    "categories": ["PC", "Console"],
}

NEW_NOTICE_1 = {
    "url": "https://www.tecmundo.com.br/noticia_1.htm",
    "title": "noticia_1",
    "timestamp": "2020-11-23T11:00:01",
    "writer": "Escritor_1",
    "shares_count": 1,
    "comments_count": 1,
    "summary": "Sumario da noticia_1",
    "sources": ["Fonte_1"],
    "categories": ["PC_1", "Console_1"],
}

NEW_NOTICE_2 = {
    "url": "https://www.tecmundo.com.br/noticia_2.htm",
    "title": "noticia_2",
    "timestamp": "2020-11-23T11:00:01",
    "writer": "Escritor_2",
    "shares_count": 1,
    "comments_count": 1,
    "summary": "Sumario da noticia_2",
    "sources": ["Fonte_2"],
    "categories": ["PC_2", "Console_2"],
}

NEW_NOTICE_3 = {
    "url": "https://www.tecmundo.com.br/noticia_3.htm",
    "title": "noticia_3",
    "timestamp": "2020-11-23T11:00:01",
    "writer": "Escritor_3",
    "shares_count": 1,
    "comments_count": 1,
    "summary": "Sumario da noticia_3",
    "sources": ["Fonte_3"],
    "categories": ["PC_3", "Console_3"],
}

NEW_NOTICE_4 = {
    "url": "https://www.tecmundo.com.br/noticia_4.htm",
    "title": "noticia_4",
    "timestamp": "2020-11-23T11:00:01",
    "writer": "Escritor_4",
    "shares_count": 1,
    "comments_count": 1,
    "summary": "Sumario da noticia_4",
    "sources": ["Fonte_4"],
    "categories": ["PC_4", "Console_4"],
}

NEW_NOTICE_5 = {
    "url": "https://www.tecmundo.com.br/noticia_5.htm",
    "title": "noticia_5",
    "timestamp": "2020-11-23T11:00:01",
    "writer": "Escritor_5",
    "shares_count": 1,
    "comments_count": 1,
    "summary": "Sumario da noticia_5",
    "sources": ["Fonte_5"],
    "categories": ["PC_5", "Console_5"],
}

NEW_NOTICE_6 = {
    "url": "https://www.tecmundo.com.br/noticia_6.htm",
    "title": "noticia_6",
    "timestamp": "2020-11-23T11:00:01",
    "writer": "Escritor_6",
    "shares_count": 1,
    "comments_count": 1,
    "summary": "Sumario da noticia_6",
    "sources": ["Fonte_6"],
    "categories": ["PC_6", "Console_6"],
}

def test_analyzer_menu_basic(capsys):
    # validar saída do console analyzer menu
    def fake_input(prompt=""):
        print(prompt, end=" ")
        return ""
    with patch("builtins.input", fake_input):
        analyzer_menu()
    out, err = capsys.readouterr()
    assert (
        "Selecione uma das opções a seguir:\n 0 - Popular o banco com notícias;\n 1 - Buscar notícias por título;\n 2 - Buscar notícias por data;\n 3 - Buscar notícias por fonte;\n 4 - Buscar notícias por categoria;\n 5 - Listar top 5 notícias;\n 6 - Listar top 5 categorias;\n 7 - Sair."
        in out
    )


def test_analyzer_menu_functions(capsys, mocker):
    # executar opção sair
    with patch("builtins.input") as mocked_input:
        mocked_input.side_effect = ["7", ""]
        analyzer_menu()
    out, err = capsys.readouterr()
    assert "Encerrando script\n" in out

    # executar opção invalida
    with patch("builtins.input") as mocked_input:
        mocked_input.side_effect = ["8", ""]
        analyzer_menu()
    out, err = capsys.readouterr()
    assert err == "Opção inválida\n"

    # executar opção buscar por titulo
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE_ANALYZER)
    with patch("builtins.input") as mocked_input, patch(
        "tech_news.menu.search_by_title"
    ) as mock_search_by_title:
        mocked_input.side_effect = ["1", "Vamoscomtudo"]
        analyzer_menu()
        mock_search_by_title.assert_called_once_with("Vamoscomtudo")

    # executar opção buscar por data
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE_ANALYZER)
    with patch("builtins.input") as mocked_input, patch(
        "tech_news.menu.search_by_date"
    ) as mock_search_by_date:
        mocked_input.side_effect = ["2", "2020-11-23"]
        analyzer_menu()
        mock_search_by_date.assert_called_once_with("2020-11-23")

    # executar opção buscar por fonte
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE_ANALYZER)
    with patch("builtins.input") as mocked_input, patch(
        "tech_news.menu.search_by_source"
    ) as mock_search_by_source:
        mocked_input.side_effect = ["3", "ResetEra"]
        analyzer_menu()
        mock_search_by_source.assert_called_once_with("ResetEra")

    # executar opção buscar por categoria
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE_ANALYZER)
    with patch("builtins.input") as mocked_input, patch(
        "tech_news.menu.search_by_category"
    ) as mock_search_by_category:
        mocked_input.side_effect = ["4", "Console"]
        analyzer_menu()
        mock_search_by_category.assert_called_once_with("Console")

    # executar opção top5 noticias
    db.news.delete_many({})
    db.news.insert_many(
        [
            NEW_NOTICE_1,
            NEW_NOTICE_2,
            NEW_NOTICE_3,
            NEW_NOTICE_4,
            NEW_NOTICE_5,
            NEW_NOTICE_6,
        ]
    )
    with patch("builtins.input") as mocked_input, patch(
        "tech_news.menu.top_5_news"
    ) as mock_top_5_news:
        mocked_input.side_effect = ["5", ""]
        analyzer_menu()
        mock_top_5_news.assert_called_once()

    # executar opção top5 categorias
    db.news.delete_many({})
    db.news.insert_many(
        [
            NEW_NOTICE_1,
            NEW_NOTICE_2,
            NEW_NOTICE_3,
            NEW_NOTICE_4,
            NEW_NOTICE_5,
            NEW_NOTICE_6,
        ]
    )
    with patch("builtins.input") as mocked_input, patch(
        "tech_news.menu.top_5_categories"
    ) as mock_top_5_categories:
        mocked_input.side_effect = ["6", ""]
        analyzer_menu()
        mock_top_5_categories.assert_called_once()

    # executar opção popular banco
    def mocked_fetch(url):
        path = (
            "tests/assets/tecmundo_pages/"
            + url.split("https://www.tecmundo.com.br/")[1].replace("/", "|")
            + ".html"
        )
        with open(path) as f:
            html_content = f.read()
        return html_content

    mocker.patch("tech_news.scraper.fetch", new=mocked_fetch)
    with patch("builtins.input") as mocked_input, patch(
        "tech_news.menu.get_tech_news"
    ) as get_tech_news:
        mocked_input.side_effect = ["0", "1"]
        analyzer_menu()
        get_tech_news.assert_called_once()
