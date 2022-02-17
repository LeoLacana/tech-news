import selectors
import requests
import time
import parsel


# Requisito 1
def fetch(url):
    """Seu código deve vir aqui"""
    try:
        time.sleep(1)
        response = requests.get(url, timeout=1)
        if response.status_code == 200:
            return response.text
    except requests.ReadTimeout:
        pass
    return None


# Requisito 2
def scrape_novidades(html_content):
    """Seu código deve vir aqui"""
    selector = parsel.Selector(text=html_content)
    list_href = selector.css(
        "div.tec--list__item a.tec--card__thumb__link::attr(href)"
    ).getall()
    return list_href


# Requisito 3
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""
    try:
        selector = parsel.Selector(text=html_content)
        link_next_page = selector.css(
            "div.tec--list a.tec--btn::attr(href)"
        ).get()
        return link_next_page
    except requests.ReadTimeout:
        pass
    return None


# Requisito 4
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
