# -*- coding:utf-8 -*-

from flask import render_template, redirect, url_for, flash, session, request, make_response, g, jsonify
from app.main.forms import DemoForm, DemandForm, CodeForm, CommentForm, CommentForm1, ResolveForm, GradeForm, \
    ImproveForm, PortraitForm
from app.models import User, Enterprise, Tag, Demo, Demand, Demo_Review, Demo_Discuss, Demand_Review, Demand_Discuss, \
    Resolve, Improve
from . import main
from app import db, app
from app.decorators import user_login_reg, enterprise_login_reg, person_login_reg
import uuid, os, datetime, pickle, random
from app.ext.ext import remove_tag, change_list_to_dic, runningcode
from app.ext.interest_recommand import interest_recommmand_demand, interest_recommmand_demo
from app.ext.generator import generate_graph


def scatter3d():
    from pyecharts import Scatter3D

    data = [[random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)] for _ in range(80)]
    range_color = ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
                   '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
    scatter3D = Scatter3D("3D scattering plot demo", width=1200, height=600)
    scatter3D.add("", data, is_visualmap=True, visual_range_color=range_color)
    return scatter3D.render_embed()


# import jieba.analyse


# jieba.analyse.set_stop_words(app.static_folder+'/keyword/'+'stopword.txt')
# jieba.load_userdict(app.static_folder+'/keyword/'+'ai.txt')


def change_filename(filename):
    fname, fext = os.path.splitext(filename)
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s%s' % (filename_prefix, str(uuid.uuid4().hex), fext)


# 测试echarts用
@main.route('/echartstest/')
def echartstest():
    return render_template('base/echarts.html', myechart=scatter3d())


# 测试charts用
@main.route('/test/')
def test():
    return render_template('base/test.html')


# 主页
@main.route('/')
def index():
    if hasattr(g, 'user'):
        re_demos = interest_recommmand_demo(g.user)
        re_demands = interest_recommmand_demand(g.user)
        re_users = User.query.all()
        if len(re_demos) < 9:
            l = len(re_demos)
            for demo in Demo.query.order_by(Demo.addtime.asc()).all():
                if l == 8:
                    break
                if demo not in re_demos:
                    re_demos.append(demo)
                    l = l + 1
        if len(re_demands) < 9:
            for demand in Demand.query.order_by(Demand.addtime.asc()).all():
                l = len(re_demands)
                if l == 8:
                    break
                if demand not in re_demands:
                    re_demands.append(demand)
                    l = l + 1
    else:
        re_demos = Demo.query.all()
        re_demands = Demand.query.all()
        re_users = User.query.all()

    new_demos = Demo.query.order_by(
        Demo.addtime.desc()
    ).all()
    new_demands = Demand.query.order_by(
        Demand.addtime.desc()
    ).all()
    new_users = User.query.order_by(
        User.addtime.desc()
    ).all()

    hot_demos = Demo.query.order_by(
        Demo.star.desc()
    ).all()
    hot_demands = Demand.query.order_by(
        Demand.star.desc()
    ).all()
    hot_users = User.query.order_by(
        User.fans.desc()
    ).all()

    return render_template('main/index.html', re_demos=re_demos[0:8], re_demands=re_demands[0:8],
                           re_users=re_users[0:8],
                           new_demos=new_demos[0:8], new_demands=new_demands[0:8], new_users=new_users[0:8],
                           hot_demos=hot_demos[0:8], hot_demands=hot_demands[0:8], hot_users=hot_users[0:8])


# demo
@main.route('/resolve/release/<int:demand_id>/', methods=['GET', 'POST'])
@user_login_reg
def resolve_release(demand_id=None):
    demand = Demand.query.get_or_404(int(demand_id))
    form = ResolveForm()
    if form.validate_on_submit():
        data = form.data
        url = ""
        if form.url.data:
            file_url = form.url.data.filename
            if not os.path.exists(app.config["UP_RESOLVE"] + g.user.uuid + '/'):  # 如果不存在，则创建文件
                os.makedirs(app.config["UP_RESOLVE"] + g.user.uuid + '/')
                # os.chmod(app.config["UP_RESOLVE"] + g.user.uuid + '/', "rw")  # 授权
            url = file_url
            form.url.data.save(app.config["UP_RESOLVE"] + g.user.uuid + '/' + url)
        resolve = Resolve(
            name=data['name'],
            description=data['description'],
            url=url,
            user_id=g.user.id,
            demand_id=demand.id
        )
        db.session.add(resolve)
        db.session.commit()
        flash("发布resolve成功", "ok")
        return redirect(url_for('main.resolve_release', demand_id=demand.id))
    return render_template('main/resolve_release.html', form=form)


@main.route('/improve/detail/<int:id>', methods=['GET', 'POST'])
@person_login_reg
def improve_detail(id=None):
    improve = Improve.query.get_or_404(int(id))
    form = GradeForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            improve.score = data['score']
            improve.qua_score = data['qua_score']
            improve.com_score = data['com_score']
            improve.cre_score = data['cre_score']
            improve.word_score = data['word_score']
            improve.review = data['review']

            db.session.commit()
            return redirect(url_for('main.improve_detail', id=improve.id, page=-1))
    me = g.user
    is_user = session.get('is_user')
    return render_template('main/improve_detail.html', me=me, improve=improve, is_user=is_user,
                           form=form)


# demo
@main.route('/improve/release/<int:demo_id>', methods=['GET', 'POST'])
@user_login_reg
def improve_release(demo_id=None):
    demo = Demo.query.get_or_404(int(demo_id))
    form = ImproveForm()
    if form.validate_on_submit():
        data = form.data
        url = ""
        if form.url.data:
            file_url = form.url.data.filename
            if not os.path.exists(app.config["UP_IMPROVE"] + g.user.uuid + '/'):  # 如果不存在，则创建文件
                os.makedirs(app.config["UP_IMPROVE"] + g.user.uuid + '/')
                # os.chmod(app.config["UP_RESOLVE"] + g.user.uuid + '/', "rw")  # 授权
            url = file_url
            form.url.data.save(app.config["UP_IMPROVE"] + g.user.uuid + '/' + url)
        improve = Improve(
            name=data['name'],
            description=data['description'],
            url=url,
            user_id=g.user.id,
            demo_id=demo.id
        )
        db.session.add(improve)
        db.session.commit()
        flash("发布resolve成功", "ok")
        return redirect(url_for('main.improve_release', demo_id=demo.id))
    return render_template('main/improve_release.html', form=form)


@main.route('/resolve/detail/<int:id>/', methods=['GET', 'POST'])
@person_login_reg
def resolve_detail(id=None):
    resolve = Resolve.query.get_or_404(int(id))
    form = GradeForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            resolve.score = data['score']
            resolve.qua_score = data['qua_score']
            resolve.com_score = data['com_score']
            resolve.cre_score = data['cre_score']
            resolve.word_score = data['word_score']
            resolve.review = data['review']

            db.session.commit()
            return redirect(url_for('main.resolve_detail', id=resolve.id, page=-1))
    me = g.user
    is_user = session.get('is_user')
    return render_template('main/resolve_detail.html', me=me, resolve=resolve, is_user=is_user,
                           form=form)


# demo
@main.route('/demo/release/', methods=['GET', 'POST'])
@user_login_reg
def demo_release():
    q = Tag.query
    tags = q.all()
    count = q.count()

    form = DemoForm()

    if form.validate_on_submit():
        data = form.data
        url = ""
        if form.url.data:
            file_url = form.url.data.filename
            if not os.path.exists(app.config["UP_DEMO"] + g.user.uuid + '/'):  # 如果不存在，则创建文件
                os.makedirs(app.config["UP_DEMO"] + g.user.uuid + '/')
                # os.chmod(app.config["UP_DEMO"] + g.user.uuid + '/', "rw")  # 授权
            url = file_url
            form.url.data.save(app.config["UP_DEMO"] + g.user.uuid + '/' + url)
        demo = Demo(
            name=data['name'],
            description=data['description'],
            per_price=data['per_price'],
            price=data['price'],
            url=url,
            user_id=g.user.id,
        )
        select = request.form.get("logo")
        demo.picture = select
        # 将文本提取关键词 转换成字典存储
        # txt = remove_tag(data['description'])
        # keywordlist = jieba.analyse.extract_tags(txt, topK=10, withWeight=True, allowPOS=('nz', 'n'))
        # dic = change_list_to_dic(keywordlist)
        # with open(app.static_folder + '/keyword/' + 'demokey.dat') as file:
        #     d = pickle.load(file)
        #     d[demo.id] = dic
        #     pickle.dump(d, file)
        #
        for tag_id in range(count):
            if request.form.get(str(tag_id)):
                tag = q.filter_by(id=tag_id).first()
                demo.tags.append(tag)

        db.session.add(demo)
        db.session.commit()
        flash("发布demo成功", "ok")
        return redirect(url_for('main.demo_release'))
    return render_template('main/demo_release.html', form=form, tags=tags)


# demo细节页面
@main.route('/demo/detail/<int:id>', methods=['GET', 'POST'])
@person_login_reg
def demo_detail(id=None):
    demo = Demo.query.get_or_404(int(id))
    form = CommentForm()
    picture = str(demo.picture)
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            is_user = session.get('is_user')
            if is_user:
                comment = Demo_Review(description=data['ckdemo'],
                                      demo_id=demo.id,
                                      star=data['score'],
                                      qua_star=data['qua_score'],
                                      cre_star=data['cre_score'],
                                      if_is_user_id=g.user.id,
                                      is_big=True)
            else:
                comment = Demo_Review(description=data['ckdemo'],
                                      demo_id=demo.id,
                                      star=data['score'],
                                      qua_star=data['qua_score'],
                                      cre_star=data['cre_score'],
                                      if_is_enterprise_id=g.user.id,
                                      is_big=True)
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('main.demo_detail', id=demo.id, page=-1))
        # 删除评论，包括大评论和小评论
        elif request.get_json()['mydata'] == 'delete_review':
            delete_review = Demo_Review.query.filter_by(id=request.get_json()['review_id']).first()
            # 如果是大评论
            if delete_review.is_big == True:
                # 先找出大评论涉及到的关系
                delete_disscusses = Demo_Discuss.query.filter_by(demo_discussed_id=delete_review.id).all()
                for discuss in delete_disscusses:
                    # 用关系找到小评论
                    small_reviews = Demo_Review.query.filter_by(id=discuss.demo_discusser_id).first()
                    # 删删删
                    db.session.delete(small_reviews)
                    db.session.delete(discuss)

            db.session.delete(delete_review)
            db.session.commit()
            return redirect(url_for('main.demo_detail', id=demo.id, page=-1))
        # 给大评论添加小评论
        elif request.get_json()['mydata'] == 'small_review':
            big_review = Demo_Review.query.filter_by(id=request.get_json()['review_id']).first()
            is_user = session.get('is_user')
            if is_user:
                small_review = Demo_Review(description=request.get_json()['context'],
                                           demo_id=demo.id,
                                           star=0,
                                           if_is_user_id=g.user.id
                                           )
            else:
                small_review = Demo_Review(description=request.get_json()['context'],
                                           demo_id=demo.id,
                                           star=0,
                                           if_is_enterprise_id=g.user.id,
                                           )
            db.session.add(small_review)
            # 建立关系，用到models.py里的函数
            big_review.discuss(small_review)
            # 更新一下文章评论的情况
            db.session.commit()
            return redirect(url_for('main.demo_detail', id=demo.id, page=-1))
        elif request.get_json()['mydata'] == 'favourite_demo':
            if not g.user.has_democol(demo):
                g.user.democol(demo)
                return redirect(url_for('main.demo_detail', id=demo.id, page=-1))
        # 取消收藏
        elif request.get_json()['mydata'] == 'unfavourite_demo':
            g.user.undemocol(demo)
            return redirect(url_for('main.demo_detail', id=demo.id, page=-1))
        elif request.get_json()['mydata'] == 'cfunding':
            g.user.demo_cf(demo)
            return redirect(url_for('main.demo_detail', id=demo.id, page=-1))
    # 找出所有大评论
    comment = Demo_Review.query.filter_by(demo_id=demo.id).filter_by(is_big=True).order_by(Demo_Review.addtime.desc())
    number = comment.count()
    page = request.args.get('page', 1, type=int)
    pagination = comment.paginate(
        page, per_page=3,
        error_out=False)
    # 找出所有评论
    reviews = Demo_Review.query.filter_by(demo_id=demo.id).order_by(Demo_Review.addtime.desc())
    page_reviews = pagination.items
    is_user = session.get('is_user')

    # 生成一个知识图谱
    nodes, edges = generate_graph('image')
    return render_template('main/demo_detail.html', picture=picture, demo=demo,
                           form=form, reviews=reviews, page_reviews=page_reviews, pagination=pagination,
                           number=number, nodes=nodes, edges=edges)


# 交易市场页面
@main.route('/mail/list/<int:page>/', methods=['GET', 'POST'])
def mail_list(page):
    page_data = Demo.query
    tags = Tag.query.all()

    if page is None:
        page = 1

    # 用户名称
    dn = request.args.get('dn', 0)
    if int(dn) != 0:
        if int(dn) == 1:
            page_data = page_data.order_by(
                Demo.name.desc()
            )
        else:
            page_data = page_data.order_by(
                Demo.name.acs()
            )
    # 时间
    time = request.args.get('time', 0)
    if int(time) != 0:
        if int(time) == 1:
            page_data = page_data.order_by(
                Demo.addtime.desc()
            )
        else:
            page_data = page_data.order_by(
                Demo.addtime.acs()
            )

    # 星级
    star = request.args.get('star', 0)
    if int(star) != 0:
        if int(star) == 1:
            page_data = page_data.order_by(
                Demo.star.desc()
            )
        else:
            page_data = page_data.order_by(
                Demo.star.acs()
            )

    p = dict(
        dn=dn,
        star=star,
        time=time,
    )
    page_data = page_data.paginate(page=page, per_page=10)
    return render_template('main/mail.html', page_data=page_data, tags=tags, p=p)


# demo列表页面
@main.route('/demo/list/<int:page>/', methods=['GET', 'POST'])
def demo_list(page):
    page_data = Demo.query
    tags = Tag.query.all()

    if page is None:
        page = 1

    # 用户名称
    dn = request.args.get('dn', 0)
    if int(dn) != 0:
        if int(dn) == 1:
            page_data = page_data.order_by(
                Demo.name.desc()
            )
        else:
            page_data = page_data.order_by(
                Demo.name.acs()
            )
    # 时间
    time = request.args.get('time', 0)
    if int(time) != 0:
        if int(time) == 1:
            page_data = page_data.order_by(
                Demo.addtime.desc()
            )
        else:
            page_data = page_data.order_by(
                Demo.addtime.acs()
            )

    # 星级
    star = request.args.get('star', 0)
    if int(star) != 0:
        if int(star) == 1:
            page_data = page_data.order_by(
                Demo.star.desc()
            )
        else:
            page_data = page_data.order_by(
                Demo.star.acs()
            )

    p = dict(
        dn=dn,
        star=star,
        time=time,
    )
    page_data = page_data.paginate(page=page, per_page=10)
    return render_template('main/demo_list.html', page_data=page_data, tags=tags, p=p)


# demo筛选页面
@main.route('/demo/filter/<int:page>/', methods=['POST'])
def demo_filter(page):
    q = Tag.query
    tags = q.all()
    count = q.count()

    if page is None:
        page = 1

    # 将tag的demo筛选出来，然后set取交集
    demolis = set()
    if request.method == 'POST':
        first = True
        for tag_id in range(count):
            if request.form.get(str(tag_id)) and first:
                tag = q.filter_by(id=tag_id).first()
                demos = tag.demos.all()
                demolis = set(demos)
                first = False
            elif request.form.get(str(tag_id)) and not first:
                tag = q.filter_by(id=tag_id).first()
                demos = tag.demos.all()
                demolis.intersection(set(demos))
    return render_template('main/demo_filter.html', demolis=demolis, tags=tags)


# 用户列表页面
@main.route('/user/list/<int:page>/', methods=['GET', 'POST'])
def user_list(page):
    form = PortraitForm()
    page_data = User.query
    tags = Tag.query.all()

    if page is None:
        page = 1

    # 用户名称
    dn = request.args.get('dn', 0)
    if int(dn) != 0:
        if int(dn) == 1:
            page_data = page_data.order_by(
                User.name.desc()
            )
        else:
            page_data = page_data.order_by(
                User.name.acs()
            )
    # 时间
    time = request.args.get('time', 0)
    if int(time) != 0:
        if int(time) == 1:
            page_data = page_data.order_by(
                User.addtime.desc()
            )
        else:
            page_data = page_data.order_by(
                User.addtime.acs()
            )

    # 星级
    star = request.args.get('star', 0)
    if int(star) != 0:
        if int(star) == 1:
            page_data = page_data.order_by(
                User.fans.desc()
            )
        else:
            page_data = page_data.order_by(
                User.fans.acs()
            )

    p = dict(
        dn=dn,
        star=star,
        time=time,
    )
    page_data = page_data.paginate(page=page, per_page=10)
    return render_template('main/user_list.html', page_data=page_data, tags=tags, p=p, form=form)


# 用户筛选页面
@main.route('/user/filter/<int:page>/', methods=['POST'])
def user_filter(page):
    q = Tag.query
    tags = q.all()
    count = q.count()

    if page is None:
        page = 1

    # 将tag的demo筛选出来，然后set取交集
    userlis = set()
    if request.method == 'POST':
        first = True
        for tag_id in range(count):
            if request.form.get(str(tag_id)) and first:
                tag = q.filter_by(id=tag_id).first()
                users = tag.users.all()
                userlis = set(users)
                first = False
            elif request.form.get(str(tag_id)) and not first:
                tag = q.filter_by(id=tag_id).first()
                users = tag.user.all()
                userlis.intersection(set(users))
    return render_template('main/user_filter.html', userlis=userlis, tags=tags)


@main.route('/demand/release/', methods=['GET', 'POST'])
@enterprise_login_reg
def demand_release():
    q = Tag.query
    tags = q.all()
    count = q.count()

    form = DemandForm()
    select = request.form.get("logo")
    if form.validate_on_submit():
        data = form.data
        url = ""
        if form.url.data:
            file_url = form.url.data.filename
            if not os.path.exists(app.config["UP_DEMAND"] + g.user.uuid + '/'):  # 如果不存在，则创建文件
                os.makedirs(app.config["UP_DEMAND"] + g.user.uuid + '/')
                # os.chmod(app.config["UP_DEMAND"] + g.user.uuid + '/', "rw")  # 授权
            url = file_url
            form.url.data.save(app.config["UP_DEMAND"] + g.user.uuid + '/' + url)
        demand = Demand(
            name=data['name'],
            finsh_time=data['finish_time'],
            description=data['description'],
            url=url,
            enterprise_id=g.user.id,
        )
        demand.picture = select
        # 将文本提取关键词 转换成字典存储
        # txt = remove_tag(data['description'])
        # keywordlist = jieba.analyse.extract_tags(txt, topK=10, withWeight=True, allowPOS=('nz', 'n'))
        # dic = change_list_to_dic(keywordlist)
        # with open(app.static_folder + '/keyword/' + 'demandkey.dat') as file:
        #     d = pickle.load(file)
        #     d[demand.id] = dic
        #     pickle.dump(d, file)

        for tag_id in range(count):
            if request.form.get(str(tag_id)):
                tag = q.filter_by(id=tag_id).first()
                demand.tags.append(tag)

        db.session.add(demand)
        db.session.commit()
        flash("发布demand成功", "ok")
    return render_template('main/demand_release.html', form=form, tags=tags)


@main.route('/demand/detail/<int:id>', methods=['GET', 'POST'])
@person_login_reg
def demand_detail(id=None):
    demand = Demand.query.get_or_404(int(id))
    picture = str(demand.picture)
    form = CommentForm1()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            is_user = session.get('is_user')
            if is_user:
                comment = Demand_Review(description=data['ckdemo'],
                                        demand_id=demand.id,
                                        if_is_user_id=g.user.id,
                                        is_big=True)
            else:
                comment = Demand_Review(description=data['ckdemo'],
                                        demand_id=demand.id,
                                        if_is_enterprise_id=g.user.id,
                                        is_big=True)
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('main.demand_detail', id=demand.id, page=-1))
        # 删除评论，包括大评论和小评论
        elif request.get_json()['mydata'] == 'delete_review':
            delete_review = Demand_Review.query.filter_by(id=request.get_json()['review_id']).first()
            # 如果是大评论
            if delete_review.is_big == True:
                # 先找出大评论涉及到的关系
                delete_disscusses = Demand_Discuss.query.filter_by(demand_discussed_id=delete_review.id).all()
                for discuss in delete_disscusses:
                    # 用关系找到小评论
                    small_reviews = Demand_Review.query.filter_by(id=discuss.demand_discusser_id).first()
                    # 删删删
                    db.session.delete(small_reviews)
                    db.session.delete(discuss)
            db.session.delete(delete_review)
            db.session.commit()
            return redirect(url_for('main.demand_detail', id=demand.id, page=-1))
        # 给大评论添加小评论
        elif request.get_json()['mydata'] == 'small_review':
            big_review = Demand_Review.query.filter_by(id=request.get_json()['review_id']).first()
            is_user = session.get('is_user')
            if is_user:
                small_review = Demand_Review(description=request.get_json()['context'],
                                             demand_id=demand.id,
                                             if_is_user_id=g.user.id
                                             )
            else:
                small_review = Demand_Review(description=request.get_json()['context'],
                                             demand_id=demand.id,

                                             if_is_enterprise_id=g.user.id,
                                             )
            db.session.add(small_review)
            # 建立关系，用到models.py里的函数
            big_review.discuss(small_review)
            # 更新一下文章评论的情况
            db.session.commit()
            return redirect(url_for('main.demand_detail', id=demand.id, page=-1))
        elif request.get_json()['mydata'] == 'favourite_demand':
            if not g.user.has_demandcol(demand):
                g.user.demandcol(demand)
                return redirect(url_for('main.demand_detail', id=demand.id, page=-1))
        # 取消收藏
        elif request.get_json()['mydata'] == 'unfavourite_demand':
            g.user.undemandcol(demand)
            return redirect(url_for('main.demand_detail', id=demand.id, page=-1))

    # 找出所有大评论
    comment = Demand_Review.query.filter_by(demand_id=demand.id).filter_by(is_big=True).order_by(
        Demand_Review.addtime.desc())
    number = comment.count()
    page = request.args.get('page', 1, type=int)
    pagination = comment.paginate(
        page, per_page=3,
        error_out=False)
    # 找出所有评论
    reviews = Demand_Review.query.filter_by(demand_id=demand.id).order_by(Demand_Review.addtime.desc())
    page_reviews = pagination.items

    # 生成一个知识图谱
    nodes, edges = generate_graph('image')
    return render_template('main/demand_detail.html', picture=picture, demand=demand,
                           form=form, reviews=reviews, page_reviews=page_reviews, pagination=pagination,
                           number=number, nodes=nodes, edges=edges)


@main.route('/demand/list/<int:page>/')
def demand_list(page):
    page_data = Demand.query
    tags = Tag.query.all()

    if page is None:
        page = 1

    # 用户名称
    dn = request.args.get('dn', 0)
    if int(dn) != 0:
        if int(dn) == 1:
            page_data = page_data.order_by(
                Demand.name.desc()
            )
        else:
            page_data = page_data.order_by(
                Demand.name.acs()
            )
    # 时间
    time = request.args.get('time', 0)
    if int(time) != 0:
        if int(time) == 1:
            page_data = page_data.order_by(
                Demand.addtime.desc()
            )
        else:
            page_data = page_data.order_by(
                Demand.addtime.acs()
            )

    # 星级
    star = request.args.get('star', 0)
    if int(star) != 0:
        if int(star) == 1:
            page_data = page_data.order_by(
                Demand.star.desc()
            )
        else:
            page_data = page_data.order_by(
                Demand.star.acs()
            )

    p = dict(
        dn=dn,
        star=star,
        time=time,
    )
    page_data = page_data.paginate(page=page, per_page=10)
    return render_template('main/demand_list.html', page_data=page_data, tags=tags, p=p)


# demand筛选页面
@main.route('/demand/filter/<int:page>/', methods=['POST'])
def demand_filter(page):
    q = Tag.query
    tags = q.all()
    count = q.count()

    if page is None:
        page = 1

    # 将tag的demand筛选出来，然后set取交集
    demandlis = set()
    if request.method == 'POST':
        first = True
        for tag_id in range(count):
            if request.form.get(str(tag_id)) and first:
                tag = q.filter_by(id=tag_id).first()
                demands = tag.demands.all()
                demandlis = set(demands)
                first = False
            elif request.form.get(str(tag_id)) and not first:
                tag = q.filter_by(id=tag_id).first()
                demands = tag.demands.all()
                demandlis.intersection(set(demands))
    return render_template('main/demand_filter.html', demandlis=demandlis, tags=tags)


# 题库列表页面
@main.route('/question/list/<int:page>/')
def question_list(page):
    page_data = Demand.query
    tags = Tag.query.all()

    if page is None:
        page = 1

    return render_template('main/question_list.html', tags=tags)


# 题目细节页面
@main.route('/question/detail/<int:id>', methods=['GET', 'POST'])
@person_login_reg
def question_detail(id=None):
    form = CommentForm()

    return render_template('main/question_detail.html', form=form)


# 代码在线运行
@main.route('/codeditor/', methods=['GET', 'POST'])
def codeditor():
    form = CodeForm()
    result = {}

    if not form.validate_on_submit() and request.form:
        print(request.form)
        index = request.form
        type = index['type']
        dtype = index['dtype']
        text = index['text']
        result['output'] = '该'+type+'的'+dtype+'指标为'+ str(0.7+random.random()*0.3)
        print(random.randint(0, 3)/10)
        if ')' not in text:
            result['output'] = "输入格式错误，请重新输入"
        return render_template('main/codeditor.html', form=form, result=result)

    if form.validate_on_submit():
        code = form.data['code']
        test = form.data['test']
        # print(form.data)
        if test:
            code += '''
import cProfile
cProfile.run("%s")
            ''' % test
        # print(code)
        filename = app.static_folder + '/uploads/code/code.py'
        with open(filename, 'w') as file:
            file.writelines(code)
        result = runningcode(filename)
        # 使用div作为容器的时候，需要将换行符转换为br并且使用safe过滤器进行输出
        # 使用textarea作为容器的时候，则不需要这个操作，会按照格式自动进行转换
        # result['output'] = result['output'].replace('\r\n', '<br>')
        # print(result)
        redirect(url_for('main.codeditor'))
    return render_template('main/codeditor.html', form=form, result=result)


# 搜索页面
@main.route('/search/<int:page>', methods=['GET', 'POST'])
def search(page):
    if page is None:
        page = 1

    key = request.form.get('key')
    methods = request.form.get('methods')
    if methods == '1':
        page_data = Demo.query.filter(
            Demo.name.ilike("%" + key + "%")
        ).order_by(
            Demo.addtime.desc()
        ).paginate(page=page, per_page=10)
        page_data.key = key

        return render_template('main/demo_search.html', page_data=page_data)

    if methods == '2':
        page_data = Demand.query.filter(
            Demand.name.ilike("%" + key + "%")
        ).order_by(
            Demand.addtime.desc()
        ).paginate(page=page, per_page=10)
        page_data.key = key
        return render_template('main/demand_search.html', page_data=page_data)


@main.route('/chat/', methods=['GET', 'POST'])
def chat():
    # from app.chatbot.basic_rob import chat
    #
    # print(chat.get_response("吃了吗？"))
    return render_template('main/chat.html')


@main.route('/chatresponse/', methods=['GET', 'POST'])
def chatresponse():
    from app.chatbot.basic_rob import chat
    if request.method == 'POST':
        question = str(request.get_json()['data'])
        # print(question)
        res = chat.get_response(question)
        # print(res)
    d = {"res": res}
    # print(request.get_json()['data'])
    return jsonify(d)


@main.route('/resultresponse/', methods=['GET', 'POST'])
def resultresponse():
    if request.method == 'POST':
        aspects = []
        aspect_lis = Tag.query.all()
        text = str(request.get_json()['data'])
        find = False
        print("收到文本", text)
        for tag in aspect_lis:
            if tag.name in text:
                aspects.append(tag.name)
                find = True
        # print(res)
        if find:
            d = {"res": render_template('main/result.html', aspects=aspects)}
        else:
            d = {"res": '没有找到'}
    # print(request.get_json()['data'])
    return jsonify(d)


@app.route('/demoupload/', methods=['POST'])
def demoupload():
    """CKEditor file upload"""
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")
    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        # fname, fext = os.path.splitext(fileobj.filename)
        new_name = change_filename(fileobj.filename)
        filepath = os.path.join(app.static_folder, 'uploads/demo/' + g.user.uuid + '/', new_name)
        # 检查路径是否存在，不存在则创建
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'
        if not error:
            fileobj.save(filepath)
            url = url_for('static', filename='%s/%s' % ('uploads/demo/' + g.user.uuid + '/', new_name))
    else:
        error = 'post error'
    res = """

<script type="text/javascript">
  window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
</script>

""" % (callback, url, error)
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response


@app.route('/demandupload/', methods=['POST'])
def demandupload():
    """CKEditor file upload"""
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")
    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        # fname, fext = os.path.splitext(fileobj.filename)
        new_name = change_filename(fileobj.filename)
        filepath = os.path.join(app.static_folder, 'uploads/demand/' + g.user.uuid + '/', new_name)
        # 检查路径是否存在，不存在则创建
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'
        if not error:
            fileobj.save(filepath)
            url = url_for('static', filename='%s/%s' % ('uploads/demand/' + g.user.uuid + '/', new_name))
    else:
        error = 'post error'
    res = """

<script type="text/javascript">
  window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
</script>

""" % (callback, url, error)
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response


@main.before_request
def my_before_request():
    user_id = session.get('user_id')
    is_user = session.get('is_user')
    g.is_user = is_user

    if user_id and is_user:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user
    elif user_id and not is_user:
        user = Enterprise.query.filter(Enterprise.id == user_id).first()
        if user:
            g.user = user


@main.context_processor
def my_context_processpr():
    if hasattr(g, 'user'):
        return {'user': g.user, 'is_user': g.is_user}
    return {}
