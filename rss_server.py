"""
RSS Generator
"""
import datetime
from peewee import Model, SqliteDatabase, CharField, IntegerField, TextField, DateTimeField
from flask import Flask
from dateutil import parser
from flask import request, Response
from feedgen.feed import FeedGenerator

app = Flask(__name__)
db = SqliteDatabase('wechat.sqlite')


class BaseModel(Model):
    class Meta:
        database = db

class Posts(BaseModel):
    id = IntegerField()
    biz = CharField()
    title = CharField()
    appmsgid = CharField()
    accountName = CharField()
    author = CharField()
    title = CharField()
    contentUrl = CharField(unique=True)
    digest = TextField()
    idx = IntegerField()
    sourceUrl = CharField()
    createTime = DateTimeField()
    readNum = IntegerField()
    likeNum = IntegerField()
    rewardNum = IntegerField()
    electedCommentNum = IntegerField()


@app.route('/feeds/<feed_id>', methods=['GET'])
def feeds(feed_id):
    # TODO 获取feed信息
    feed = {
        "name": "对应的RSS名称"
    }
    fg = FeedGenerator()
    if feed:
        fg.id(feed["name"])
        fg.title(feed["name"])
        fg.link(href=request.url)
        fg.description(feed["name"])
    else:
        fg.id("RSS Qiwihui")
        fg.title("RSS Qiwihui")
        return fg.atom_str(pretty=True)

    # 获取文章
    posts = Posts.select().where(Posts.biz == feed_id).limit(10)

    for post in posts:
        fe = fg.add_entry()
        fe.id(post.contentUrl)
        fe.title(post.title)
        fe.author(name=post.author, replace=True)
        fe.content(post.digest)
        fe.link(href=post.contentUrl)
        fe.pubDate(parser.parse(post.createTime))
        fe.published(parser.parse(post.createTime))
    ret = fg.atom_str(pretty=True)
    ret = ret.decode('utf-8') if isinstance(ret, bytes) else ret
    return Response(ret, mimetype='text/xml')
