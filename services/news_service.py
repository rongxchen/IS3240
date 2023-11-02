from datetime import datetime
from models.model import News, session
from sqlalchemy import desc, text
from services.news_service_helper import from_reuters, from_bbg


def find_latest(source):
    return session.query(News).filter_by(source=source).order_by(desc("timestamp")).first()

def write_to_db(news_list, source, latest=None):
    for news in news_list:
        timestamp = int(datetime.strptime(news["publish_time"], "%Y-%m-%d").timestamp())
        # if latest != None:
        #     if timestamp < latest.timestamp or (news["title"] == latest.title and timestamp == latest.timestamp):
        #         print("stop syncing")
        #         return False
        timestamp = int(datetime.strptime(news.get("publish_time"), "%Y-%m-%d").timestamp())
        news_obj = News(news["title"], news["publish_time"], timestamp, source, news.get("url", ""),
                        news.get("category", ""), news.get("img_url"))
        session.add(news_obj)
        session.commit()
    return True

def remove_duplicates():
    sql = text("DELETE FROM news WHERE id NOT IN (SELECT MIN(id) FROM news GROUP BY title)")
    session.execute(sql)
    session.commit()

def sync_news():
    remove_duplicates()
    latest = find_latest("routers")
    for i in range(1, 16):
        news_from_routers = from_reuters(i, 20)
        written = write_to_db(news_from_routers, "routers", latest)
        if not written:
            break
        print(f"page {i} finished")
    latest = find_latest("bloomberg")
    news_from_routers = from_bbg()
    written = write_to_db(news_from_routers, "bloomberg", latest)
    print("synced to latest")

def find_total(keyword=None):
    filter_by = f" where title like '%{keyword}%'"
    total = session.execute(text("select count(1) from news" + (filter_by if keyword else ""))).fetchall()[0][0]
    return int(total)

def get_news_by_page(page, size, keyword=None):
    _from = (page-1) * size
    news_list = session.query(News).filter(News.title.like(f'%{str(keyword).strip()}%')).order_by(desc("timestamp")).limit(size).offset(_from).all() \
        if keyword else session.query(News).order_by(desc("timestamp")).limit(size).offset(_from).all()
    print(news_list)
    return {
        "list": [{
            "title": news.title, "url": news.url, "publish_time": news.publish_time, "img_url": news.img_url,
            "category": news.category.replace(" ", "/"), "source": str(news.source).upper()
        } for news in news_list],
        "total": find_total(keyword)
    }

def search_news(page, size, keyword):
    print("from search")
    return get_news_by_page(page, size, keyword)
