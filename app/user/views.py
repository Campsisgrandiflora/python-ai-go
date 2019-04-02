# -*- coding:utf-8 -*-

from flask import render_template, redirect, url_for, flash, session, request, g
from app.user.forms import LoginForm, RegisterForm, UserDetailForm, PwdForm, PortraitForm
from app.models import Tag, Demo, User, Demand, Enterprise, Usercol
from . import user
from werkzeug.security import generate_password_hash
from app import db, app
from app.decorators import user_login_reg, person_login_reg
import uuid, os, datetime, pickle
from app.ext.evaluate import *
from app.ext.generator import generate_graph


def change_filename(filename):
    fname, fext = os.path.splitext(filename)
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s%s' % (filename_prefix, str(uuid.uuid4().hex), fext)


# 生成一个知识图谱 输入为图谱名称id
def generate_graph(id):
    import csv
    # 读取csv文件
    with open(app.static_folder + '/keyword/' + str(id) + '.csv') as f:
        reader = csv.reader(f)
        lis = list(reader)[1:]
        nodes = [{"name": l[1]} for l in lis]
    with open(app.static_folder + '/keyword/' + str(id) + 'r.csv') as f:
        reader = csv.reader(f)
        lisref = list(reader)[1:]
        edges = [{"source": int(e[0]) - 1, "target": int(e[1]) - 1} for e in lisref]
    return nodes, edges


# 用户主页
@user.route('/', methods=['GET', 'POST'])
@user_login_reg
def index():
    form = UserDetailForm()
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
            if not os.path.exists(app.config["UF_DIR"] + g.user.uuid + '/'):
                os.makedirs(app.config["UF_DIR"] + g.user.uuid + '/')
                # os.chmod(app.config["UF_DIR"] + g.user.uuid + '/', "rw")
            user.face = change_filename(file_face)
            form.face.data.save(app.config["UF_DIR"] + g.user.uuid + '/' + user.face)

        name_count = User.query.filter_by(name=data['name']).count
        if data['name'] != user.name and name_count == 1:
            flash("昵称已经存在了", 'err')
            return redirect('user.index')
        email_count = User.query.filter_by(email=data['email']).count

        if data['email'] != user.email and email_count == 1:
            flash("邮箱已经存在了", 'err')
            return redirect('user.index')
        phone_count = User.query.filter_by(phone=data['phone']).count

        if data['phone'] != user.phone and phone_count == 1:
            flash("手机号码已经存在了", 'err')
            return redirect('user.index')

        user.name = data['name']
        user.email = data['email']
        user.phone = data['phone']
        user.info = data['info']
        user.recommand_method = data['recommand']

        db.session.add(user)
        db.session.commit()
        flash('修改成功!', 'ok')
        return redirect(url_for('user.index'))
    return render_template('user/user.html', form=form)


# 修改密码
@user.route('/pwd/', methods=['GET', 'POST'])
@user_login_reg
def pwd():
    form = PwdForm()
    user = g.user
    if form.validate_on_submit():
        data = form.data
        if not user.check_pwd(data['old_pwd']):
            flash('密码错误', 'err')
            return redirect(url_for('user.pwd'))
        user.pwd = generate_password_hash(data["new_pwd"])
        db.session.add(user)
        db.session.commit()
        flash('修改密码成功,请重新登录', 'ok')
        return redirect(url_for('user.logout'))
    return render_template('user/pwd.html', form=form)


# 个人展示空间
@user.route('/zone/<int:user_id>', methods=['GET', 'POST'])
@person_login_reg
def zone(user_id=None):
    form = PortraitForm()
    # 用户画像部分
    from pyecharts import Radar
    score1 = []
    score2 = []
    score3 = []
    for cal in CAL_EVALUATE:
        score1.append(cal(user=None))
        score2.append(cal(user=None))
        score3.append(cal(user=None))

    c_schema = [{"name": e, "max": 100} for e in EVALUATE]  # 构建评价指标

    value_bj = [score1]
    radar1 = Radar(width=280, height=300)
    radar1.config(c_schema=c_schema)
    radar1.add("人才画像", value_bj, item_color="#f9713c", is_area_show=True, area_color="#f9713c", area_opacity=0.5)

    value_bj = [score2]
    radar2 = Radar(width=280, height=300)
    radar2.config(c_schema=c_schema)
    radar2.add("人才画像", value_bj, item_color="#f9713c", is_area_show=True, area_color="#f9713c", area_opacity=0.5)

    value_bj = [score3]
    radar3 = Radar(width=280, height=300)
    radar3.config(c_schema=c_schema)
    radar3.add("人才画像", value_bj, item_color="#f9713c", is_area_show=True, area_color="#f9713c", area_opacity=0.5)

    # 后端处理部分
    user = User.query.filter_by(id=user_id).first()
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
            me.follow(user)
            return redirect(url_for('user.zone', user_id=user.id))
        # 取消关注
        elif request.get_json()['mydata'] == 'unfollow':
            me.unfollow(user)
            return redirect(url_for('user.zone', user_id=user.id))
    return render_template('user/Zone.html', user=user, me=me,
                           myechart1=radar1.render_embed(), myechart2=radar2.render_embed(),
                           myechart3=radar3.render_embed(), form=form)


# 匹配结果
@user.route('/match/', methods=['GET', 'POST'])
@user_login_reg
def match():
    user_id = session.get('user_id')
    with open(app.static_folder + '/keyword/' + 'redemolist.dat', 'rb') as file:
        d = pickle.load(file)

    redic = {}
    demodic = {}

    for demo in Demo.query.filter_by(user_id=user_id):
        reid = d[demo.id]
        demodic[demo.id] = demo
        relist = []

        for id, score in reid:
            demand = Demand.query.filter_by(
                id=id
            ).first()
            relist.append(demand)
        redic[demo.id] = relist

    return render_template('user/match.html', demodic=demodic, redic=redic)


# 用户画像
@user.route('/portrait/', methods=['GET', 'POST'])
@user_login_reg
def portrait():
    form = PortraitForm()
    from pyecharts import Radar

    if request.method == 'GET':
        score = []
        for cal in CAL_EVALUATE:
            score.append(cal(user=g.user))
        value_bj = [score]
        c_schema = [{"name": e, "max": 100} for e in EVALUATE]
        radar = Radar(width=500, height=350)
        radar.config(c_schema=c_schema)
        radar.add("人才画像", value_bj, item_color="#f9713c", is_area_show=True, area_color="#f9713c", area_opacity=0.5)

        score = []
        for cal in CAL_EVALUATE:
            score.append(cal(user=g.user)+random.randint(2, 8))
        value_bj = [score]
        c_schema = [{"name": e, "max": 100} for e in EVALUATE]
        radar1 = Radar(width=500, height=350)
        radar1.config(c_schema=c_schema)
        radar1.add("人才画像", value_bj, item_color="#f9713c", is_area_show=True, area_color="#f9713c", area_opacity=0.5)
        # radar.render_embed()

    if request.method == 'POST':
        select = list(map(int, form.data['select']))    # 高阶函数 转换为int
        print(select)

        score = []
        c_schema = []
        for num in select:
            score.append(CAL_EVALUATE[num](user=g.user))
            c_schema.append({"name": EVALUATE[num], "max": 100})
        value_bj = [score]

        radar = Radar(width=500, height=350)
        radar.config(c_schema=c_schema)
        radar.add("人才画像", value_bj, item_color="#f9713c", is_area_show=True, area_color="#f9713c", area_opacity=0.5)

        score = []
        for cal in CAL_EVALUATE:
            score.append(cal(user=g.user) + random.randint(2, 8))
        value_bj = [score]
        c_schema = [{"name": e, "max": 100} for e in EVALUATE]
        radar1 = Radar(width=500, height=350)
        radar1.config(c_schema=c_schema)
        radar1.add("人才画像", value_bj, item_color="#f9713c", is_area_show=True, area_color="#f9713c", area_opacity=0.5)
        # radar.render_embed()

    # 更改用户的兴趣
    user = g.user
    my_tags = user.tags.all()

    q = Tag.query
    tags = q.all()
    count = q.count()

    # for tag in my_tags:
    #     tags.remove(tag)
    flag = False
    for i in range(count):
        if request.form.get(str(i)) is not None:
            flag = True
            break

    if request.method == 'POST' and flag:
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

    return render_template('user/portrait.html', form=form,
                           tags=tags, my_tags=my_tags, myechart=radar.render_embed(), myechart1=radar1.render_embed())


# 知识图谱
@user.route('/knowledge_graph/', methods=['GET', 'POST'])
@user_login_reg
def knowledge_graph():
    if request.method == 'GET':
        nodes, edges = generate_graph('ai')
    else:
        nodes, edges = generate_graph('nlp')

    return render_template('user/knowledge_graph.html', nodes=nodes, edges=edges)


# 游戏化机制
@user.route('/gamification/', methods=['GET', 'POST'])
@user_login_reg
def gamification():
    return render_template('user/gamification.html')


# 登录
@user.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    nexturl = request.args.get('next')

    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(email=data['email']).first()
        if not user.check_pwd(data['pwd']):
            flash('密码错误', 'err')
            return redirect(url_for('user.login'))
        session["is_user"] = True
        session["user_id"] = user.id

        return redirect(nexturl or url_for('user.index'))
    return render_template('user/login.html', form=form)


# 登出
@user.route('/logout/')
@user_login_reg
def logout():
    session.clear()
    return redirect(url_for("user.login"))


# 注册
@user.route('/register/', methods=['GET', 'POST'])
def register():
    q = Tag.query
    tags = q.all()
    count = q.count()

    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
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

    return render_template('user/register.html', form=form, tags=tags)


# 解决方案列表
@user.route('/resolve/', methods=['GET', 'POST'])
@user_login_reg
def resolve():
    return render_template('user/resolve.html')


# 改进方案列表
@user.route('/my_improve/', methods=['GET', 'POST'])
@user_login_reg
def my_improve():
    return render_template('user/my_improve.html')


# 收藏demo列表
@user.route('/demo_col/', methods=['GET', 'POST'])
@user_login_reg
def demo_col():
    return render_template('user/demo_col.html')


# 关注个人、企业列表
@user.route('/followed/', methods=['GET', 'POST'])
@user_login_reg
def followed():
    follows = Usercol.query.filter_by(user_id=g.user.id).filter_by(object=True).all()
    return render_template('user/followed.html', follows=follows)


# 关注企业列表
# @user.route('/ent_followed/', methods=['GET', 'POST'])
# @user_login_reg
# def ent_followed():
#     follows = Usercol.query.filter_by(user_id=g.user.id).filter_by(object=True).all()
#     return render_template('user/ent_followed.html', follows=follows)


# 参与众筹列表
@user.route('/crowd_funding/', methods=['GET', 'POST'])
@user_login_reg
def crowd_funding():
    return render_template('user/crowd_funding.html')


@user.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user


@user.context_processor
def my_context_processpr():
    if hasattr(g, 'user'):
        return {'user': g.user, 'is_user': True}
    return {}
