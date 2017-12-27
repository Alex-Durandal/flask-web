# -*- coding:utf8 -*-
import os
from random import choice
from flask_script import Manager
from application import app,db
from application.module import Comment,Image,User
import random
manager = Manager(app)

def get_image_url():
    dir=app.config.get('IMAGE_DIR')
    image_list = os.listdir(dir)
    for i in xrange(len(image_list)):
        if os.path.isdir(image_list[i]):
            image_list.pop(i)
    url = "/static/images/photo/"+choice(image_list)
    return url
    # url = 'http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) + 't.png'
    return url

@manager.command
def initDB():
    db.drop_all()
    db.create_all()
    for i in range(0, 10):
            db.session.add(User('牛客' +str(i), 'a'+str(i)))
            for j in range(0, 3): #每人发三张图
                db.session.add(Image(get_image_url(), i + 1))
                for k in range(0, 3):
                    db.session.add(Comment(i+1, 1+3*i+j,  '这是一条评论'+str(k)))
    db.session.commit()


if __name__ == '__main__':
    manager.run()
