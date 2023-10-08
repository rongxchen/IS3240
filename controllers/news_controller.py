from flask import Blueprint
from services.financial_news_service import from_reuters
from general_config import token_required, result

news_api = Blueprint("news_api", __name__)

@news_api.get("/api/news/<int:page>/<int:size>")
@token_required
def get_news_by_page(user_id, page, size):
    """ get news from routers by page and size
    :param page: current page
    :param size: size of news per page
    :return: a list of news articles
    """
    news_list = from_reuters(page, size)
    if news_list:
        return result(200, "success", news_list)
    return result(400, "failed")
