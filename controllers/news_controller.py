from flask import Blueprint, request
from services import news_service
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
    keyword = request.args.get("keyword")
    print(keyword)
    news_list = news_service.get_news_by_page(page, size) if not keyword and keyword.strip() != "" else news_service.search_news(page, size, keyword)
    if news_list:
        return result(200, "success", news_list)
    return result(400, "failed")
