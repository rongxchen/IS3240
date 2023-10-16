import requests
import json
from utils.http import get_headers

headers = get_headers()

def enc_params(page, size):
    """ helper function to construct get params for routers news scraping
    :param page: current page
    :param size: size of news per page
    :return: a json-like string to be concatenated with the url
    """
    offset = (page-1) * size
    params = {
        "arc-site":"reuters","called_from_a_component":True,"fetch_type":"collection","id":"/business/finance/",
        "offset":offset,"section_id":"/business/finance/","size":size,"sophi_page":"*","sophi_widget":"topic",
        "uri":"/business/finance/","website":"reuters"
    }
    return json.dumps(params)

def from_reuters(page, size):
    """
    :param page: current page
    :param size: size of news per page
    :return: a list of news articles
    """
    params = enc_params(page, size)
    url = f"https://www.reuters.com/pf/api/v3/content/fetch/articles-by-section-alias-or-id-v1?query={params}"
    resp = requests.get(url=url, headers=headers)
    reuters_domain = "https://www.reuters.com"
    news_list = []
    try:
        articles = resp.json()["result"]["articles"]
        for article in articles:
            if "title" not in article or "canonical_url" not in article:
                continue
            title = article.get("title", "")
            url = reuters_domain + article.get("canonical_url", "")
            publish_time = article.get("published_time", "").split("T")[0]
            img_url = article.get("thumbnail", {}).get("url", "")
            category = article.get("kicker", {}).get("name", "")
            news_list.append({
                "title": title.replace("'", "\""), "url": url, "publish_time": publish_time, "img_url": img_url, "category": category
            })
    except Exception as e:
        print(e)
    return news_list
