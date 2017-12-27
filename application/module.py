# -*- coding:utf8 -*-
from application import db
from datetime import datetime
import random
from application import login_manager

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(50),unique=True)
    salt = db.Column(db.String(32))
    password = db.Column(db.String(32))
    head_url = db.Column(db.String(256))
    images = db.relationship("Image",backref='user',lazy='dynamic')


    def __init__(self,name,password,salt=''):
        self.name=name
        self.password=password
        self.head_url = 'http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) + 't.png'
        self.salt = salt

    def __repr__(self):
        print "user id:%d, name: %s " % self.id,self.name

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(256))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    time = db.Column(db.DateTime)
    comments = db.relationship("Comment")

    def __init__(self,url,user_id):
        self.url = url
        self.user_id = user_id
        self.time = datetime.now()

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time = db.Column(db.DateTime)
    image_id = db.Column(db.Integer,db.ForeignKey('image.id'))
    content = db.Column(db.String(256))
    status = db.Column(db.Integer,default=0)
    user = db.relationship("User")

    def __init__(self,user_id,image_id,content):
        self.time = datetime.now()
        self.user_id = user_id
        self.image_id = image_id
        self.content = content

    def __repr__(self):
        print "[image %d][comment %d][user %d]: %s {%s}" % self.image_id,self.id,self.user_id,self.content,self.time


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)