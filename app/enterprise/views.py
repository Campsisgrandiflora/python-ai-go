# -*- coding:utf-8 -*-

from flask import render_template, redirect, url_for, flash, session, request, make_response, g
from app.enterprise.forms import LoginForm, RegisterForm, EnterpriseDetailForm, PwdForm
from app.models import Tag, Demo, Enterprise, Demand, Usercol, User
from . import enterprise
from werkzeug.security import generate_password_hash
from app import db, app
from app.decorators import enterprise_login_reg
import uuid, os, datetime, pickle


def change_filename(filename):
    fname, fext = os.path.splitext(filename)
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s%s' % (filename_prefix, str(uuid.uuid4().hex), fext)


# 企业主页
@enterprise.route('/', methods=['GET', 'POST'])
@enterprise_login_reg
def index():
    form = EnterpriseDetailForm()
    user = g.user

    form.face.validators = []
    if request.method == 'GET':
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
    if form.validate_on_submit():
        data = form.data

        if form.face.data:
            file_face = form.face.data.filename
            if not os.path.exists(app.config["EF_DIR"] + g.user.uuid + '/'):
                os.makedirs(app.config["EF_DIR"] + g.user.uuid + '/')
                # os.chmod(app.config["EF_DIR"] + g.user.uuid + '/', "rw")
            user.face = change_filename(file_face)
            form.face.data.save(app.config["EF_DIR"] + g.user.uuid + '/' + user.face)

        name_count = Enterprise.query.filter_by(name=data['name']).count
        if data['name'] != user.name and name_count == 1:
            flash("昵称已经存在了", 'err')
            return redirect('user.index')
        email_count = Enterprise.query.filter_by(email=data['email']).count

        if data['email'] != user.email and email_count == 1:
            flash("邮箱已经存在了", 'err')
            return redirect('user.index')
        phone_count = Enterprise.query.filter_by(phone=data['phone']).count

        if data['phone'] != user.phone and phone_count == 1:
            flash("手机号码已经存在了", 'err')
            return redirect('enterprise.index')

        user.name = data['name']
        user.email = data['email']
        user.phone = data['phone']
        user.info = data['info']

        db.session.add(user)
        db.session.commit()
        flash('修改成功!', 'ok')
        return redirect(url_for('enterprise.index'))
    return render_template('enterprise/enterprise.html', form=form, user=user)


# 收藏demo列表
@enterprise.route('/demo_col/', methods=['GET', 'POST'])
@enterprise_login_reg
def demo_col():
    return render_template('enterprise/demo_col.html')


# 解决方案列表
@enterprise.route('/resolve/', methods=['GET', 'POST'])
@enterprise_login_reg
def resolve():
    return render_template('enterprise/resolve.html')


# 关注列表
@enterprise.route('/followed/', methods=['GET', 'POST'])
@enterprise_login_reg
def followed():
    follows = Usercol.query.filter_by(enterprise_id=g.user.id).filter_by(object=False).all()
    return render_template('enterprise/followed.html', follows=follows)


# 参与众筹列表
@enterprise.route('/crowd_funding/', methods=['GET', 'POST'])
@enterprise_login_reg
def crowd_funding():
    return render_template('enterprise/crowd_funding.html')


# 修改密码
@enterprise.route('/pwd/', methods=['GET', 'POST'])
@enterprise_login_reg
def pwd():
    form = PwdForm()
    user = g.user
    if form.validate_on_submit():
        data = form.data
        if not user.check_pwd(data['old_pwd']):
            flash('密码错误', 'err')
            return redirect(url_for('enterprise.pwd'))
        user.pwd = generate_password_hash(data["new_pwd"])
        db.session.add(user)
        db.session.commit()
        flash('修改密码成功,请重新登录', 'ok')
        return redirect(url_for('enterprise.logout'))
    return render_template('enterprise/pwd.html', form=form)


# 匹配结果
@enterprise.route('/match/', methods=['GET', 'POST'])
@enterprise_login_reg
def match():
    user_id = session.get('user_id')
    with open(app.static_folder + '/keyword/' + 'redemandlist.dat', 'rb') as file:
        d = pickle.load(file)

    redic = {}
    demanddic = {}
    for demand in Demand.query.filter_by(enterprise_id=user_id):
        reid = d[demand.id]
        demanddic[demand.id] = demand
        relist = []

        for id, score in reid:
            demo = Demo.query.filter_by(
                id=id
            ).first()
            relist.append(demo)
        redic[demand.id] = relist

    return render_template('enterprise/match.html', demanddic=demanddic, redic=redic)


# 用户画像
@enterprise.route('/portrait/', methods=['GET', 'POST'])
def portrait():
    user = g.user
    my_tags = user.tags.all()

    q = Tag.query
    tags = q.all()
    count = q.count()

    for tag in my_tags:
        tags.remove(tag)

    if request.method == 'POST':
        for tag in my_tags:
            user.tags.remove(tag)

        for tag_id in range(count):
            if request.form.get(str(tag_id)):
                tag = q.filter_by(id=tag_id).first()
                user.tags.append(tag)

        db.session.add(user)
        db.session.commit()

        my_tags = user.tags.all()

        q = Tag.query
        tags = q.all()
        count = q.count()

        for tag in my_tags:
            tags.remove(tag)

    return render_template('enterprise/portrait.html', tags=tags, my_tags=my_tags)


# 个人展示空间
@enterprise.route('/zone/<int:enterprise_id>', methods=['GET', 'POST'])
def zone(enterprise_id=None):
    enterprise = Enterprise.query.filter_by(id=enterprise_id).first()
    user_id = session.get('user_id')
    is_user = session.get('is_user')
    g.is_user = is_user
    if user_id and is_user:
        user1 = User.query.filter(User.id == user_id).first()
        if user1:
            me = user1
    elif user_id and not is_user:
        user1 = Enterprise.query.filter(Enterprise.id == user_id).first()
        if user1:
            me = user1
    if request.method == 'POST':
        if request.get_json()['mydata'] == 'follow':
            me.ent_follow(enterprise)
            return redirect(url_for('enterprise.zone', enterprise_id=enterprise.id))
        # 取消关注
        elif request.get_json()['mydata'] == 'unfollow':
            me.ent_unfollow(enterprise)
            return redirect(url_for('enterprise.zone', enterprise_id=enterprise.id))
    return render_template('enterprise/Zone.html', user=enterprise, me=me, is_user=is_user)


# 注册
@enterprise.route('/register/', methods=['GET', 'POST'])
def register():
    q = Tag.query
    tags = q.all()
    count = q.count()

    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = Enterprise(
            name=data['name'],
            email=data['email'],
            pwd=generate_password_hash(data['pwd']),
            uuid=uuid.uuid4().hex
        )
        for tag_id in range(count):
            if request.form.get(str(tag_id)):
                tag = q.filter_by(id=tag_id).first()
                user.tags.append(tag)

        db.session.add(user)
        db.session.commit()
        flash("注册成功", "ok")

    return render_template('enterprise/register.html', form=form, tags=tags)


# 登录
@enterprise.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    nexturl = request.args.get('next')

    if form.validate_on_submit():
        data = form.data
        user = Enterprise.query.filter_by(email=data['email']).first()
        if not user.check_pwd(data['pwd']):
            flash('密码错误', 'err')
            return redirect(url_for('enterprise.login'))
        session["is_user"] = False
        session["user_id"] = user.id

        return redirect(nexturl or url_for('enterprise.index'))
    return render_template('enterprise/login.html', form=form)


# 登出
@enterprise.route('/logout/')
@enterprise_login_reg
def logout():
    session.clear()
    return redirect(url_for("enterprise.login"))


@enterprise.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = Enterprise.query.filter(Enterprise.id == user_id).first()
        if user:
            g.user = user


@enterprise.context_processor
def my_context_processpr():
    if hasattr(g, 'user'):
        return {'user': g.user, 'is_user': False}
    return {}
