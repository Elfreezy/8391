from datetime import datetime
from slugify import slugify
from random import randint
from sqlalchemy import func

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


def slugy(text):
    return slugify(text, separator='-', lowercase=True) + '-' + str(randint(0, 10 ** 10))


fck = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
                )


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(140), unique=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('Tag', secondary=fck, lazy='dynamic', backref='posts')

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.slug = slugy(self.title)

    def get_timestamp(self):
        return self.created.strftime("%d-%m-%Y %H:%M")

    def set_tags(self, tags):
        symbols = [',']
        for symbol in symbols:
            tags = tags.replace(symbol, ' ')
        tags = tags.split()
        for tag in tags:
            tag = tag.lower()
            created_tag = Tag.query.filter(Tag.title == tag).first()
            if created_tag is None:
                tag = Tag(title=tag, posts=[self])
                db.session.add(tag)
                db.session.commit()
            else:
                created_tag.posts.append(self)
                db.session.add(created_tag)
                db.session.commit()
        # self.tags = tags
        return


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))

    def get_posts(self, id):
        posts = db.session.execute('SELECT post_id FROM tags WHERE tag_id = {}'.format(id))
        result = []
        for post in posts:
            post_id = post[0]
            result.append(post_id)
        return result

    def delete_tag(self):
        db.session.delete(self)
        db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    login = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))

    posts = db.relationship('Post', backref='author')

    def set_password_hash(self, password):
        self.password = generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
