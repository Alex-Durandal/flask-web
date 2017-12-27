# -*- coding:utf8 -*-
import hashlib
from random import sample

from flask_login import login_user, login_required,logout_user,current_user

from application import app,db
from flask import render_template,redirect,request,flash,get_flashed_messages
from module import Image,User


@app.route('/')
def index():
    images = Image.query.order_by("id desc").limit(10)
    return render_template("index.html",images=images)


@app.route('/profile/<int:user_id>/')
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    if(user == None):
        return redirect('/')
    return render_template("profile.html",user=user)

@app.route("/image/<int:image_id>/")
@login_required
def pageDetail(image_id):
    image = Image.query.get(image_id)
    return render_template('pageDetail.html',image=image)

def redirect_with_msg(target, msg, category):
    if msg != None:
        flash(msg, category=category)
    return redirect(target)

@app.route('/regist/',methods=['POST'])
def regist():
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()

    if username=='' or password=='':
        return redirect_with_msg('/reglogin/',u'用户名密码不能为空','regist')

    user = User.query.filter_by(name=username).first()
    if user != None:
        return redirect_with_msg('/reglogin/', u'用户名已存在', 'regist')

    salt = '.'.join(sample('01234567890abcdefghigABCDEFGHI', 10))
    m = hashlib.md5()
    m.update(password + salt)
    password = m.hexdigest()
    user = User(username,password,salt)
    db.session.add(user)
    db.session.commit()

    login_user(user)
    flash('Regist successfully.')

    next = request.args.get('next')
    print next
    if next != None and next.startwith('/'):
        return redirect(next)
    return redirect_with_msg('/', u'注册成功', 'regist')

@app.route('/login/',methods=['POST'])
def login():
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    if username=='' or password=='':
        return redirect_with_msg('/reglogin/',u'用户名密码不能为空','login')

    user = User.query.filter_by(name=username).first()
    if user == None:
        return redirect_with_msg('/reglogin/', u'用户名不存在', 'login')
    salt = user.salt
    m = hashlib.md5()
    m.update(password + salt)
    password = m.hexdigest()

    if password != user.password:
        return redirect_with_msg('/reglogin/', u'密码错误', 'login')

    login_user(user)

    next = request.args.get('next')
    print next
    if next != None and next.startwith('/'):
        return redirect(next)
    return redirect_with_msg('/', u'登录成功', 'login')

@app.route('/reglogin/', methods=['GET', 'POST'])
def reglogin():
    msg = ''
    for m in get_flashed_messages(with_categories=False, category_filter=['login','regist']):
        msg = msg + m
    return render_template('login.html', msg=msg)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/')