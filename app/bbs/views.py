# -*- coding:utf-8 -*-

import datetime
import os
import uuid
from datetime import datetime

from flask import render_template, redirect, url_for, flash, session, request, make_response, g

from app import db, app
from app.bbs.forms import CKEditorForm, CommentForm
from app.decorators import user_login_reg
from app.models import Tag, Enterprise, Article, Review, User, Plate, Collect, Praise, Moderator, Discuss
from . import bbs


# 生成文件名
def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(uuid.uuid4().hex))


# 论坛主页路由
@bbs.route('/', methods=['GET', 'POST'])
def index():
    # 分别过滤出四个版块最多评论的六篇文章
    articles1 = Article.query.filter_by(plate_id=1).order_by(Article.reviews_number.desc()).limit(6)
    articles2 = Article.query.filter_by(plate_id=2).order_by(Article.reviews_number.desc()).limit(6)
    articles3 = Article.query.filter_by(plate_id=3).order_by(Article.reviews_number.desc()).limit(6)
    articles4 = Article.query.filter_by(plate_id=4).order_by(Article.reviews_number.desc()).limit(6)
    return render_template('bbs/bbs.html', articles1=articles1, articles2=articles2, articles3=articles3,
                           articles4=articles4)


# 发帖页面路由
@bbs.route('/post/', methods=['GET', 'POST'])
@user_login_reg
def post_message():
    q = Tag.query
    tags = q.all()
    count = q.count()

    form = CKEditorForm()
    if form.validate_on_submit():
        data = form.data
        file_url = form.url.data.filename
        if not os.path.exists(app.config["UP_ARTICLE"] + g.user.uuid + '/'):  # 如果不存在，则创建文件
            os.makedirs(app.config["UP_ARTICLE"] + g.user.uuid + '/')
        url = file_url
        form.url.data.save(app.config["UP_ARTICLE"] + g.user.uuid + '/' + url)
        article = Article(
            title=data['title'],
            description=data['ckdemo'],
            url=url,
            author_id=g.user.id,
            plate_id=data['belongedPlate']
        )

        for tag_id in range(count):
            if request.form.get(str(tag_id)):
                tag = q.filter_by(id=tag_id).first()
                article.tags.append(tag)
        db.session.add(article)
        db.session.commit()
        flash("发布article成功", "ok")
        return redirect(url_for('bbs.index'))
    return render_template('bbs/post.html', form=form, tags=tags)


# 帖子详情页面路由，其中版块id与文章id是变量
@bbs.route('/article/detail/<int:plate_id>/<int:id>', methods=['GET', 'POST'])
@user_login_reg
def article_detail(plate_id=None, id=None):
    plate = Plate.query.get_or_404(int(plate_id))
    # 判断用户是否是版主
    is_moderator = False
    if not Moderator.query.filter_by(plate_id=plate.id).filter_by(moderator_id=g.user.id) == None:
        is_moderator = True
    article = Article.query.get_or_404(int(id))
    form = CommentForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            comment = Review(description=data['ckdemo'],
                             article_id=article.id,
                             author_id=g.user.id,
                             is_big=True)
            db.session.add(comment)
            article.reviews_number = article.reviews_number + 1
            article.last_review_time = datetime.today()
            db.session.commit()
            return redirect(url_for('bbs.article_detail', plate_id=plate.id, id=article.id, page=-1))
        # 点赞
        elif request.get_json()['mydata'] == 'add':
            userPraise = Praise.query.filter_by(giver_id=g.user.id).first()
            if userPraise == None:
                praise = Praise(article_id=article.id,
                                giver_id=g.user.id)
                db.session.add(praise)
                db.session.commit()
                return redirect(url_for('bbs.article_detail', plate_id=plate.id, id=article.id, page=-1))
        # 取消点赞
        elif request.get_json()['mydata'] == 'delete':
            userPraise = Praise.query.filter_by(giver_id=g.user.id).first()
            if not userPraise == None:
                db.session.delete(userPraise)
                db.session.commit()
                return redirect(url_for('bbs.article_detail', plate_id=plate.id, id=article.id, page=-1))
        # 收藏
        elif request.get_json()['mydata'] == 'favorite':
            userCollect = Collect.query.filter_by(giver_id=g.user.id).first()
            if userCollect == None:
                collect = Collect(article_id=article.id,
                                  giver_id=g.user.id)
                db.session.add(collect)
                db.session.commit()
                return redirect(url_for('bbs.article_detail', plate_id=plate.id, id=article.id, page=-1))
        # 取消收藏
        elif request.get_json()['mydata'] == 'unfavorite':
            userCollect = Collect.query.filter_by(giver_id=g.user.id).first()
            if not userCollect == None:
                db.session.delete(userCollect)
                db.session.commit()
                return redirect(url_for('bbs.article_detail', plate_id=plate.id, id=article.id, page=-1))
        # 删除评论，包括大评论和小评论
        elif request.get_json()['mydata'] == 'delete_review':
            delete_review = Review.query.filter_by(id=request.get_json()['review_id']).first()
            # 如果是大评论
            if delete_review.is_big == True:
                # 先找出大评论涉及到的关系
                delete_disscusses = Discuss.query.filter_by(discussed_id=delete_review.id).all()
                for discuss in delete_disscusses:
                    # 用关系找到小评论
                    small_reviews = Review.query.filter_by(id=discuss.discusser_id).first()
                    # 删删删
                    db.session.delete(small_reviews)
                    db.session.delete(discuss)
                    # 评论数减1
                    article.reviews_number = article.reviews_number - 1
            db.session.delete(delete_review)
            article.reviews_number = article.reviews_number - 1
            db.session.commit()
            return redirect(url_for('bbs.article_detail', plate_id=plate.id, id=article.id, page=-1))
        # 给大评论添加小评论
        elif request.get_json()['mydata'] == 'small_review':
            big_review = Review.query.filter_by(id=request.get_json()['review_id']).first()
            small_review = Review(description=request.get_json()['context'],
                                  article_id=article.id,
                                  author_id=g.user.id,
                                  )
            db.session.add(small_review)
            # 建立关系，用到models.py里的函数
            big_review.discuss(small_review)
            # 更新一下文章评论的情况
            article.reviews_number = article.reviews_number + 1
            article.last_review_time = datetime.today()
            db.session.commit()
            return redirect(url_for('bbs.article_detail', plate_id=plate.id, id=article.id, page=-1))
    # 找出所有大评论
    comment = Review.query.filter_by(article_id=article.id).filter_by(is_big=True).order_by(Review.addtime.desc())
    number = comment.count()
    # 获取收藏情况
    myCollect = Collect.query.filter_by(article_id=article.id)
    collectNumber = myCollect.count()
    # 获取点赞情况
    myPraise = Praise.query.filter_by(article_id=article.id)
    praiseNumber = myPraise.count()
    userPraise = Praise.query.filter_by(giver_id=g.user.id).first()
    userCollect = Collect.query.filter_by(collector_id=g.user.id).first()
    page = request.args.get('page', 1, type=int)
    pagination = comment.paginate(
        page, per_page=20,
        error_out=False)
    # 找出所有评论
    reviews = Review.query.filter_by(article_id=article.id).order_by(Review.addtime.desc())
    my_id = g.user.id
    return render_template('bbs/article_detail.html', article=article, plate=plate, is_moderator=is_moderator,
                           my_id=my_id,
                           form=form, reviews=reviews, pagination=pagination, userPraise=userPraise,
                           userCollect=userCollect,
                           number=number, collectNumber=collectNumber, praiseNumber=praiseNumber)


# 帖子列表的路由
@bbs.route('/article/list/<int:plate_id>', methods=['GET', 'POST'])
@user_login_reg
def article_list(plate_id=None):
    plate = Plate.query.get_or_404(int(plate_id))
    is_moderator = False
    if not Moderator.query.filter_by(plate_id=plate.id).filter_by(moderator_id=g.user.id) == None:
        is_moderator = True
    # 如果不是精华帖
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.filter_by(plate_id=plate.id).order_by(Article.last_review_time.desc()).paginate(
        page, per_page=20, error_out=False)
    posts = pagination.items
    # 如果是精华帖的情况
    pagination_elite = Article.query.filter_by(plate_id=plate.id).filter_by(is_elite=True).order_by(
        Article.last_review_time.desc()).paginate(
        page, per_page=20, error_out=False)
    posts_elite = pagination_elite.items

    if request.method == 'POST':
        # 加精
        if request.get_json()['mydata'] == 'highlight':
            highlight_article = Article.query.filter_by(id=request.get_json()['article_id']).first()
            highlight_article.is_elite = True
            db.session.commit()
            return redirect(url_for('bbs.article_list', plate_id=plate.id))
        # 取消加精
        elif request.get_json()['mydata'] == 'unhighlight':
            highlight_article = Article.query.filter_by(id=request.get_json()['article_id']).first()
            highlight_article.is_elite = False
            db.session.commit()
            return redirect(url_for('bbs.article_list', plate_id=plate.id))
        # 删除文章
        elif request.get_json()['mydata'] == 'delete':
            delete_article = Article.query.filter_by(id=request.get_json()['article_id']).first()
            # 删除文章内所有回复
            delete_reviews = Review.query.filter_by(article_id=request.get_json()['article_id']).all()
            for review in delete_reviews:
                db.session.delete(review)
            db.session.delete(delete_article)
            db.session.commit()
            return redirect(url_for('bbs.article_list', plate_id=plate.id))
    return render_template('bbs/article_list.html', plate=plate, is_moderator=is_moderator,
                           posts=posts, posts_elite=posts_elite,
                           Review=Review, pagination=pagination, pagination_elite=pagination_elite)


# 控制上传附件
@bbs.route('/article/detail/<int:id>/upcomment/', methods=['POST', 'OPTIONS'])
def upcomment():
    """CKEditor file upload"""
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")

    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)

        filepath = os.path.join(app.static_folder, 'upload/comment/', rnd_name)

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
            url = url_for('static', filename='%s/%s' % ('upload/comment/', rnd_name))
    else:
        error = 'post error'

    res = """<script type="text/javascript">
  window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
</script>""" % (callback, url, error)

    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response


@bbs.route('/post/ckupload/', methods=['POST', 'OPTIONS'])
def ckupload():
    """CKEditor file upload"""
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")

    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)

        filepath = os.path.join(app.static_folder, 'upload', rnd_name)

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
            url = url_for('static', filename='%s/%s' % ('upload', rnd_name))
    else:
        error = 'post error'

    res = """<script type="text/javascript">
  window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
</script>""" % (callback, url, error)

    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response


# 钩子函数
@bbs.before_request
def my_before_request():
    user_id = session.get('user_id')
    is_user = session.get('is_user')
    if user_id and is_user:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user
    elif user_id and not is_user:
        user = Enterprise.query.filter(Enterprise.id == user_id).first()
        if user:
            g.user = user


@bbs.context_processor
def my_context_processpr():
    if hasattr(g, 'user'):
        return {'user': g.user}
    return {}
