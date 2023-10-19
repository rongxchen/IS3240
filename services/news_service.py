from datetime import datetime
from models.model import News, session
from sqlalchemy import desc
from services.news_service_helper import from_reuters

def find_latest(source):
    return session.query(News).filter_by(source=source).order_by(desc("timestamp")).first()

def write_to_db(news_list, source, latest=None):
    for news in news_list:
        timestamp = int(datetime.strptime(news["publish_time"], "%Y-%m-%d").timestamp())
        if timestamp < latest.timestamp or (news["title"] == latest.title and timestamp == latest.timestamp):
            print("stop syncing")
            return False
        timestamp = int(datetime.strptime(news.get("publish_time"), "%Y-%m-%d").timestamp())
        news_obj = News(news["title"], news["publish_time"], timestamp, source, news.get("url", ""),
                        news.get("category", ""), news.get("img_url"))
        session.add(news_obj)
        session.commit()
    return True

def sync_news():
    latest = find_latest("routers")
    print(latest)
    for i in range(1, 16):
        news_from_routers = from_reuters(i, 20)
        written = write_to_db(news_from_routers, "routers", latest)
        if not written:
            break
        print(f"page {i} finished")
    print("synced to latest")

def get_news_by_page(page, size):
    _from = (page-1) * size
    news_list = session.query(News).order_by(desc("timestamp")).limit(size).offset(_from).all()
    return [{
        "title": news.title, "url": news.url, "publish_time": news.publish_time, "img_url": news.img_url,
        "category": news.category, "source": str(news.source).upper()
    } for news in news_list]
