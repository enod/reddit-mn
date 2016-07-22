from app import db
from datetime import date


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Posts', backref='author', lazy='dynamic')
    comments = db.relationship('Comments', backref='commenter', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    upvotes = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # subreddit = db.Column(db.String(255))
    # Defining One to Many relationships with the relationship function on the Parent Table
    comments = db.relationship('Comments', backref="post", cascade="all, delete-orphan", lazy='dynamic')

    def __init__(self, title, url, upvotes, time):
        self.title = title
        self.url = url
        self.upvotes = 0
        # self.subreddit = subreddit

    def __repr__(self):
        return '<Post %r(%r)>' % (self.title, self.url)

    def score(self):
        try:
            return self.upvotes  # purely based on upvotes right now
            # return (self.upvotes) / (self.upvotes + self.downvotes)
        except ZeroDivisionError:
            return 0


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Comment %r: %s>' % (self.text, self.post_id)
