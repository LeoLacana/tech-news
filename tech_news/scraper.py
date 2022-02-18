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
def scrape_write(selector):
    try:
        getWriter = (
            selector.css("a.tec--author__info__link::text").get()
        ).strip()
    except AttributeError:
        try:
            getWriter = (
                selector.css("div.tec--timestamp__item > a::text").get()
            ).strip()
        except AttributeError:
            getWriter = (
                selector.css("div.tec--author__info p:first-child::text").get()
            )
    return getWriter


def scrape_shares_count(selector):
    try:
        getSharesCount = int(
            selector.css(
                "nav.tec--toolbar div.tec--toolbar__item::text"
            ).re_first(r"(\d*)(?:\s*Compartilharam*$)")
        )
    except TypeError:
        getSharesCount = 0
    return getSharesCount


def scrape_noticia(html_content):
    """Seu código deve vir aqui"""
    selector = parsel.Selector(html_content)

    getUrl = selector.css("link[rel='canonical']::attr(href)").get()

    getTitle = selector.css("h1.tec--article__header__title::text").get()

    getTimestamp = selector.css(
        ".tec--timestamp__item time#js-article-date::attr(datetime)").get()

    getWriter = scrape_write(selector)

    getSharesCount = scrape_shares_count(selector)

    getCommentsCount = selector.css(
            "nav.tec--toolbar button#js-comments-btn::attr(data-count)"
        ).get()
    if getCommentsCount is None:
        getCommentsCount = 0

    getSummary = "".join(
        selector.css("div.tec--article__body p:first-child *::text").getall()
    )

    getSourcer = selector.css(
        "div.z--mb-16 a::text").getall()
    getSourcerRefatored = []
    for source in getSourcer:
        getSourcerRefatored.append(source.strip())

    getCategories = selector.css(
        "#js-categories a::text").getall()
    getCategoriesRefatored = []
    for category in getCategories:
        getCategoriesRefatored.append(category.strip())

    response = {
        "url": getUrl,
        "title": getTitle,
        "timestamp": getTimestamp,
        "writer": getWriter,
        "shares_count": getSharesCount,
        "comments_count": int(getCommentsCount),
        "summary": getSummary,
        "sources": getSourcerRefatored,
        "categories": getCategoriesRefatored,
    }
    return response


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
