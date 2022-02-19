from datetime import datetime
from tech_news.database import search_news


# Requisito 6
def search_by_title(title):
    """Seu código deve vir aqui"""
    response = [
        (news["title"], news["url"])
        for news in search_news(
            {"title": {"$regex": f"{title}", "$options": "i"}})
    ]
    return response


# Requisito 7
def search_by_date(date):
    """Seu código deve vir aqui"""
    try:
        datetime.fromisoformat(date)
        response = [
            (news['title'], news['url'])
            for news in search_news(
                {"timestamp": {"$regex": f"{date}"}}
            )
        ]
    except ValueError:
        raise ValueError("Data inválida")
    return response


# Requisito 8
def search_by_source(source):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
