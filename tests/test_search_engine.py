# flake8: noqa

from tech_news.analyzer.search_engine import (
    search_by_title,
    search_by_date,
    search_by_source,
    search_by_category,
)
import pytest
from pymongo import MongoClient
from decouple import config

from tech_news.database import db

NEW_NOTICE = {
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

LIST = [("Vamoscomtudo", "https://www.tecmundo.com.br/vamos.htm")]


def test_buscar_noticia_pelo_titulo():
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    assert search_by_title("Vamoscomtudo") == LIST

    # título inválido retorna lista vazia
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    assert search_by_title("titulo_invalido") == []

    # trata casos case-sensitive
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    assert search_by_title("VAMOSCOMTUDO") == LIST


def test_buscar_noticia_pela_data():
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    assert search_by_date("2020-11-23") == LIST

    # data inexistente no db deve retornar uma lista vazia
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    assert search_by_date("2019-12-12") == []

    # formato inválido retorna erro
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    with pytest.raises(ValueError, match="Data inválida"):
        search_by_date("21-12-1980")

    # data inválida retorna erro
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    with pytest.raises(ValueError, match="Data inválida"):
        search_by_date("2001-02-31")

    # data inválida retorna erro
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    with pytest.raises(ValueError, match="Data inválida"):
        search_by_date("2020-31-02")

    # data inválida retorna erro
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    with pytest.raises(ValueError, match="Data inválida"):
        search_by_date("1988-14-25")

    # data inválida retorna erro
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    with pytest.raises(ValueError, match="Data inválida"):
        search_by_date("1997-02-31")

def test_buscar_noticia_pela_fonte():
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    assert search_by_source("ResetEra") == LIST
    
    # fonte que não existe retorna lista vazia
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    assert search_by_source("fonte_invalida") == []

    # trata casos case-sensitive
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    assert search_by_source("RESETERA") == LIST


def test_buscar_noticia_pela_categoria():
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    assert search_by_category("Console") == LIST

    # categoria inexistente retorna lista vazia
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    assert search_by_category("categoria_invalida") == []

    # trata casos case-sensitive
    db.news.delete_many({})
    db.news.insert_one(NEW_NOTICE)
    assert search_by_category("CONSOLE") == LIST
