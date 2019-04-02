# -*- coding:utf-8 -*-
from datetime import datetime
from app import db

user_tag = db.Table('user_tag',
                    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), ),
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    extend_existing=True
                    )

enterprise_tag = db.Table('enterprise_tag',
                          db.Column('id', db.Integer, primary_key=True, autoincrement=True),
                          db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), ),
                          db.Column('enterprise_id', db.Integer, db.ForeignKey('enterprise.id')),
                          extend_existing=True
                          )

demo_tag = db.Table('demo_tag',
                    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                    db.Column('demo_id', db.Integer, db.ForeignKey('demo.id')),
                    extend_existing=True
                    )

demand_tag = db.Table('demand_tag',
                      db.Column('id', db.Integer, primary_key=True, autoincrement=True),
                      db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                      db.Column('demand_id', db.Integer, db.ForeignKey('demand.id')),
                      extend_existing=True
                      )

article_tag = db.Table("article_tag",
                       db.Column('id', db.Integer, primary_key=True, autoincrement=True),
                       db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")),
                       db.Column("article_id", db.Integer, db.ForeignKey("article.id"))
                       )


# 关注
class Follow(db.Model):
    __tablename__ = "follow"
    extend_existing = True
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                            primary_key=True)  # 关注者
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                            primary_key=True)  # 被关注者
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 关注时间

    def find_followed(self, follow):
        followed = User.query.filter_by(id=follow.followed_id).first()
        return followed


# 会员模型
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 电话
    info = db.Column(db.TEXT)  # 个人简介
    face = db.Column(db.String(255), unique=True)  # 头像
    gender = db.Column(db.String(15))
    age = db.Column(db.String(15))
    qq = db.Column(db.String(15), unique=True)  # qq
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标志符
    recommand_method = db.Column(db.Integer, default=1)  # 推荐方式
    fans = db.Column(db.Integer, index=True, default=0)  # 粉丝数

    tags = db.relationship(
        'Tag',
        secondary=user_tag,
        backref=db.backref('users', lazy='dynamic'),
        lazy='dynamic'
    )

    followeds = db.relationship('Follow',
                                foreign_keys=[Follow.follower_id],
                                backref=db.backref('follower', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')  # 被关注者外键关联
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')  # 关注者外键关联
    demos = db.relationship('Demo', backref='user')  # 用户demo外键关联
    resolves = db.relationship('Resolve', backref='user')  # 用户demo外键关联
    improves = db.relationship('Improve', backref='user')  # 用户demo外键关联

    democols = db.relationship('Democol', backref='user')  # 用户democol外键关联
    demandcols = db.relationship('Demandcol', backref='user')  # 用户demandcol外键关联
    democfs = db.relationship('Crowd_Funding', backref='user')  # 用户democf外键关联

    def __repr__(self):
        return "<User %r>" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            user.fans = user.fans + 1
        db.session.add(f)
        db.session.commit()

    def unfollow(self, user):
        f = self.followeds.filter_by(followed_id=user.id).first()
        if f:
            user.fans = user.fans - 1
            db.session.delete(f)
            db.session.commit()

    def is_following(self, user):
        return self.followeds.filter_by(followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.id).first() is not None

    def is_ent_following(self, enterprise):
        return Usercol.query.filter_by(enterprise_id=enterprise.id).filter_by(user_id=self.id).filter_by(
            object=True).first() is not None

    def ent_follow(self, enterprise):
        if not self.is_ent_following(enterprise):
            f = Usercol(
                enterprise_id=enterprise.id,
                user_id=self.id,
                object=True
            )
            self.fans = self.fans + 1
        db.session.add(f)
        db.session.commit()

    def ent_unfollow(self, enterprise):
        f = Usercol.query.filter_by(
            enterprise_id=enterprise.id
        ).filter_by(user_id=self.id).filter_by(object=True).first()
        if f:
            self.fans = self.fans - 1
            db.session.delete(f)
            db.session.commit()

    def democol(self, demo):
        dcol = Democol(
            demo_id=demo.id,
            user_id=self.id,
        )
        db.session.add(dcol)
        db.session.commit()

    def has_democol(self, demo):
        if Democol.query.filter_by(demo_id=demo.id).filter_by(user_id=self.id).first() is not None:
            return True
        else:
            return False

    def undemocol(self, demo):
        dcol = Democol.query.filter_by(demo_id=demo.id).first()
        if dcol:
            db.session.delete(dcol)
            db.session.commit()

    def demandcol(self, demand):
        dcol = Demandcol(
            demand_id=demand.id,
            user_id=self.id,
        )
        db.session.add(dcol)
        db.session.commit()

    def has_demandcol(self, demand):
        if Demandcol.query.filter_by(demand_id=demand.id).filter_by(user_id=self.id).first() is not None:
            return True
        else:
            return False

    def undemandcol(self, demand):
        dcol = Demandcol.query.filter_by(demand_id=demand.id).first()
        if dcol:
            db.session.delete(dcol)
            db.session.commit()

    def demo_cf(self, demo):
        dcf = Crowd_Funding(
            demo_id=demo.id,
            user_id=self.id,
        )
        db.session.add(dcf)
        db.session.commit()

    def a_and_r_count(self, user):
        return Article.query.filter_by(author_id=user.id).count() + Review.query.filter_by(author_id=user.id).count()

    def cf_count(self, user):
        return Crowd_Funding.query.filter_by(user_id=user.id).count()

    def ent_follow(self, user):
        return Usercol.query.filter_by(user_id=user.id).filter_by(object=False).count()

    def follow_ent(self, user):
        return Usercol.query.filter_by(user_id=user.id).filter_by(object=True).count()

    def demo_number(self, user):
        return len(user.demos)


# 标签
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 标签名称

    def __repr__(self):
        return "<Tag %r>" % self.name


# 企业
class Enterprise(db.Model):
    __tablename__ = "enterprise"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 企业名称
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 电话
    info = db.Column(db.TEXT)  # 企业简介
    face = db.Column(db.String(255), unique=True)  # 企业头像
    qq = db.Column(db.String(15), unique=True)  # qq
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标志符

    tags = db.relationship(
        'Tag',
        secondary=enterprise_tag,
        backref=db.backref('enterprises', lazy='dynamic'),
        lazy='dynamic'
    )

    demands = db.relationship('Demand', backref='enterprise')  # 企业需求外键关联

    democols = db.relationship('Democol', backref='enterprise')  # 用户enterprise外键关联
    democfs = db.relationship('Crowd_Funding', backref='enterprise')  # 用户democf外键关联

    def __repr__(self):
        return "<Enterprise %r>" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)

    def is_following(self, user):
        return Usercol.query.filter_by(enterprise_id=self.id).filter_by(user_id=user.id).filter_by(
            object=False).first() is not None

    def follow(self, user):
        if not self.is_following(user):
            f = Usercol(enterprise_id=self.id, user_id=user.id, object=False)
        db.session.add(f)
        db.session.commit()

    def unfollow(self, user):
        f = Usercol.query.filter_by(enterprise_id=self.id).filter_by(user_id=user.id).filter_by(object=False).first()
        if f:
            db.session.delete(f)
            db.session.commit()

    def democol(self, demo):
        dcol = Democol(
            demo_id=demo.id,
            enterprise_id=self.id,
        )
        db.session.add(dcol)
        db.session.commit()

    def has_democol(self, demo):
        if Democol.query.filter_by(demo_id=demo.id).filter_by(enterprise_id=self.id).first() is not None:
            return True
        else:
            return False

    def undemocol(self, demo):
        dcol = Democol.query.filter_by(demo_id=demo.id).first()
        if dcol:
            db.session.delete(dcol)
            db.session.commit()

    def demo_cf(self, demo):
        dcf = Crowd_Funding(
            demo_id=demo.id,
            enterprise_id=self.id,
        )
        db.session.add(dcf)
        db.session.commit()

    def cf_count(self, enterprise):
        return Crowd_Funding.query.filter_by(enterprise_id=enterprise.id).count()

    def ent_follow(self, enterprise):
        return Usercol.query.filter_by(enterprise_id=enterprise.id).filter_by(object=True).count()

    def follow_ent(self, enterprise):
        return Usercol.query.filter_by(enterprise_id=enterprise.id).filter_by(object=False).count()


# 需求
class Demand(db.Model):
    __tablename__ = "demand"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 编号
    name = db.Column(db.String(100))  # 需求名称
    finsh_time = db.Column(db.Date)  # 截止完成时间
    description = db.Column(db.Text)  # 需求描述
    picture = db.Column(db.Integer)  # demand的图片
    url = db.Column(db.String(255))  # 项目文件存放地址
    star = db.Column(db.Integer, default=0)  # 需求的默认星数/收藏量
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 需求发布时间

    enterprise_id = db.Column(db.Integer, db.ForeignKey('enterprise.id'))  # 所属企业

    tags = db.relationship(
        'Tag',
        secondary=demand_tag,
        backref=db.backref('demands', lazy='dynamic'),
        lazy='dynamic'
    )

    def __repr__(self):
        return "<Demand %r>" % self.name

    def col_number(self, demand):
        col = Demandcol.query.filter_by(demand_id=demand.id).all()
        return len(col)


# demo
class Demo(db.Model):
    __tablename__ = "demo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 编号
    name = db.Column(db.String(100))  # demo名称
    description = db.Column(db.Text)  # demo描述
    url = db.Column(db.String(255))  # 项目文件存放地址
    star = db.Column(db.Integer, default=0)  # demo的星数
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # demo发布时间
    picture = db.Column(db.Integer)  # demo的图片
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    per_price = db.Column(db.Integer, default=0)  # 单价
    price = db.Column(db.Integer, default=0)  # 总额

    tags = db.relationship(
        'Tag',
        secondary=demo_tag,
        backref=db.backref('demos', lazy='dynamic'),
        lazy='dynamic'
    )

    def __repr__(self):
        return "<Demo %r>" % self.name

    def calculate(self, demo):
        my_score = 0
        number = 0
        for review in Demo_Review.query.filter_by(is_big=True).filter_by(demo_id=demo.id).all():
            my_score += review.star
            number += 1
        if number == 0:
            return 0
        else:
            my_score = my_score / number
            return '%.2f' % my_score

    def number(self, demo):
        review = Demo_Review.query.filter_by(is_big=True).filter_by(demo_id=demo.id).all()
        return len(review)

    def col_number(self, demo):
        col = Democol.query.filter_by(demo_id=demo.id).all()
        return len(col)

    def cf_number(self, demo):
        col = Crowd_Funding.query.filter_by(demo_id=demo.id).all()
        return len(col)


# demo收藏
class Democol(db.Model):
    __tablename__ = "democol"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    demo_id = db.Column(db.Integer, db.ForeignKey('demo.id'))  # 所属demo
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    enterprise_id = db.Column(db.Integer, db.ForeignKey('enterprise.id'))  # 所属企业用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 添加时间

    def find_demo(self, democol):
        demo = Demo.query.filter_by(id=democol.demo_id).first()
        return demo


# demand收藏
class Demandcol(db.Model):
    __tablename__ = "demandcol"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    demand_id = db.Column(db.Integer, db.ForeignKey('demand.id'))  # 所属demo
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 添加时间

    def find_demand(self, demandcol):
        demand = Demand.query.filter_by(id=demandcol.demand_id).first()
        return demand


# 企业关注用户和用户关注企业
class Usercol(db.Model):
    __tablename__ = 'usercol'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    object = db.Column(db.Boolean)  # true为user关注企业 false为企业关注用户
    enterprise_id = db.Column(db.Integer, db.ForeignKey('enterprise.id'))  # 所属企业
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 添加时间

    def find_user(self, usercol):
        user = User.query.filter_by(id=usercol.user_id).first()
        return user

    def find_enterprise(self, usercol):
        enterprise = Enterprise.query.filter_by(id=usercol.enterprise_id).first()
        return enterprise


# 这里是后台系统管理部分的数据库 ###################################################
# 权限
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    url = db.Column(db.String(255), unique=True)  # 地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Auth %r>" % self.name


# 角色
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    auths = db.Column(db.String(600))  # 角色权限列表
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    admins = db.relationship("Admin", backref='role')  # 管理员外键关系关联

    def __repr__(self):
        return "<Role %r>" % self.name


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员账号
    pwd = db.Column(db.String(100))  # 管理员密码
    is_super = db.Column(db.SmallInteger)  # 是否为超级管理员，0为超级管理员
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 所属角色
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Admin %r>" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 这里是demand回复相关的模型 ###########################################################
class Demand_Discuss(db.Model):
    __tablename__ = "demand_discuss"
    extend_existing = True
    demand_discusser_id = db.Column(db.Integer, db.ForeignKey('demand_review.id'),
                                    primary_key=True)  # 对评论的评论
    demand_discussed_id = db.Column(db.Integer, db.ForeignKey('demand_review.id'),
                                    primary_key=True)  # 被评论的评论
    demand_discuss_addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 评论时间


# Review
class Demand_Review(db.Model):
    __tablename__ = "demand_review"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 编号

    description = db.Column(db.Text)  # 回复内容
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 回复发布时间
    is_big = db.Column(db.Boolean, index=True, default=False)  # 是否是大回复
    if_is_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # 回帖作者
    if_is_enterprise_id = db.Column(db.Integer, db.ForeignKey('enterprise.id'), nullable=True)  # 回帖作者
    demand_id = db.Column(db.Integer, db.ForeignKey('demand.id'), nullable=False)  # 回复对应的demo
    if_is_user = db.relationship("User", backref="demand_reviews")
    if_is_enterprise = db.relationship("Enterprise", backref="demand_reviews")
    demand = db.relationship("Demand", backref="demand_reviews")
    demand_discussed = db.relationship('Demand_Discuss',
                                       foreign_keys=[Demand_Discuss.demand_discusser_id],
                                       backref=db.backref('demand_discusser', lazy='joined'),
                                       lazy='dynamic',
                                       cascade='all, delete-orphan')  # 被回复的帖子外键关联
    demand_discusser = db.relationship('Demand_Discuss',
                                       foreign_keys=[Demand_Discuss.demand_discussed_id],
                                       backref=db.backref('demand_discussed', lazy='joined'),
                                       lazy='dynamic',
                                       cascade='all, delete-orphan')  # 回复的帖子外键关联

    def __repr__(self):
        return "<Demand_Review %r>" % self.description

    def discuss(self, demand_review):
        d = Demand_Discuss(demand_discusser=demand_review, demand_discussed=self)
        db.session.add(d)

    def del_discuss(self, demand_review):
        d = self.demand_discussed.filter_by(demand_discussed_id=demand_review.id).first()
        if d:
            db.session.delete(d)

    def is_discussing(self, demand_review):
        return self.demand_discussed.filter_by(demand_discussed_id=demand_review.id).first() is not None

    def is_discussed_by(self, demand_review):
        return self.demand_discusser.filter_by(demand_discusser_id=demand_review.id).first() is not None

    def is_user(self, demand_review):
        return demand_review.if_is_user is not None

    def is_enterprise(self, demand_review):
        return demand_review.if_is_enterprise is not None


# 这里是demo回复相关的模型 ###########################################################
class Demo_Discuss(db.Model):
    __tablename__ = "demo_discuss"
    extend_existing = True
    demo_discusser_id = db.Column(db.Integer, db.ForeignKey('demo_review.id'),
                                  primary_key=True)  # 对评论的评论
    demo_discussed_id = db.Column(db.Integer, db.ForeignKey('demo_review.id'),
                                  primary_key=True)  # 被评论的评论
    demo_discuss_addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 评论时间


# Review
class Demo_Review(db.Model):
    __tablename__ = "demo_review"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 编号
    star = db.Column(db.Integer, nullable=False)  # 分数
    qua_star = db.Column(db.Integer)  # 分数
    cre_star = db.Column(db.Integer)  # 分数
    description = db.Column(db.Text)  # 回复内容
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 回复发布时间
    is_big = db.Column(db.Boolean, index=True, default=False)  # 是否是大回复
    if_is_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # 回帖作者
    if_is_enterprise_id = db.Column(db.Integer, db.ForeignKey('enterprise.id'), nullable=True)  # 回帖作者
    demo_id = db.Column(db.Integer, db.ForeignKey('demo.id'), nullable=False)  # 回复对应的demo
    if_is_user = db.relationship("User", backref="demo_reviews")
    if_is_enterprise = db.relationship("Enterprise", backref="demo_reviews")
    demo = db.relationship("Demo", backref="demo_reviews")
    demo_discussed = db.relationship('Demo_Discuss',
                                     foreign_keys=[Demo_Discuss.demo_discusser_id],
                                     backref=db.backref('demo_discusser', lazy='joined'),
                                     lazy='dynamic',
                                     cascade='all, delete-orphan')  # 被回复的帖子外键关联
    demo_discusser = db.relationship('Demo_Discuss',
                                     foreign_keys=[Demo_Discuss.demo_discussed_id],
                                     backref=db.backref('demo_discussed', lazy='joined'),
                                     lazy='dynamic',
                                     cascade='all, delete-orphan')  # 回复的帖子外键关联

    def __repr__(self):
        return "<Demo_Review %r>" % self.description

    def discuss(self, demo_review):
        d = Demo_Discuss(demo_discusser=demo_review, demo_discussed=self)
        db.session.add(d)

    def del_discuss(self, demo_review):
        d = self.demo_discussed.filter_by(demo_discussed_id=demo_review.id).first()
        if d:
            db.session.delete(d)

    def is_discussing(self, demo_review):
        return self.demo_discussed.filter_by(demo_discussed_id=demo_review.id).first() is not None

    def is_discussed_by(self, demo_review):
        return self.demo_discusser.filter_by(demo_discusser_id=demo_review.id).first() is not None

    def is_user(self, demo_review):
        return demo_review.if_is_user is not None

    def is_enterprise(self, demo_review):
        return demo_review.if_is_enterprise is not None


# 这里是众筹相关的模型 ###########################################################
class Crowd_Funding(db.Model):
    __tablename__ = "crowd_funding"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 编号
    demo_id = db.Column(db.Integer, db.ForeignKey('demo.id'), nullable=False)  # 回复对应的demo
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    enterprise_id = db.Column(db.Integer, db.ForeignKey('enterprise.id'))  # 所属企业用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 添加时间

    def find_demo(self, crowd_funding):
        demo = Demo.query.filter_by(id=crowd_funding.demo_id).first()
        return demo


# 这里是解决方案相关的模型 ###########################################################

class Resolve(db.Model):
    __tablename__ = "resolve"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 编号
    score = db.Column(db.Integer)  # 分数
    qua_score = db.Column(db.Integer)  # 代码质量分数
    cre_score = db.Column(db.Integer)  # 项目创新分数
    com_score = db.Column(db.Integer)  # 沟通能力分数
    word_score = db.Column(db.Integer)  # 文档分数
    review = db.Column(db.Text)  # 企业评价内容
    description = db.Column(db.Text)  # 方案内容
    name = db.Column(db.String(100))  # 方案名称
    url = db.Column(db.String(255))  # 项目文件存放地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 方案发布时间
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    demand_id = db.Column(db.Integer, db.ForeignKey('demand.id'), nullable=False)  # 方案对应的demand
    demand = db.relationship("Demand", backref="demand_resolves")

    def find_demand(self, resolve):
        demand = Demand.query.filter_by(id=resolve.demand_id).first()
        return demand

    def number(self, demand):
        return len(demand.demand_resolves)


# 这里是论坛相关的模型 ###########################################################
# Article
class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 编号
    title = db.Column(db.String(100), nullable=False)  # 帖子标题
    description = db.Column(db.Text)  # 帖子内容
    url = db.Column(db.String(255), unique=True)  # 文件存放地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 帖子发布时间
    reviews_number = db.Column(db.Integer, index=True, default=0)  # 回复数
    last_review_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 最新回复时间
    is_elite = db.Column(db.Boolean, index=True, default=False)  # 是否是精华帖
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 文章作者
    plate_id = db.Column(db.Integer, db.ForeignKey('plate.id'), nullable=False)  # 所属版块
    plate = db.relationship("Plate", backref="articles")
    author = db.relationship("User", backref="articles")
    tags = db.relationship(
        'Tag',
        secondary=article_tag,
        backref=db.backref('articles', lazy='dynamic'),
        lazy='dynamic'
    )

    def __repr__(self):
        return "<Article %r>" % self.title


class Discuss(db.Model):
    __tablename__ = "discuss"
    extend_existing = True
    discusser_id = db.Column(db.Integer, db.ForeignKey('review.id'),
                             primary_key=True)  # 对评论的评论
    discussed_id = db.Column(db.Integer, db.ForeignKey('review.id'),
                             primary_key=True)  # 被评论的评论
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 评论时间


# Review
class Review(db.Model):
    __tablename__ = "review"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 编号
    description = db.Column(db.Text)  # 回复内容
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 回复发布时间
    is_big = db.Column(db.Boolean, index=True, default=False)  # 是否是大回复
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 回帖作者
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)  # 回复对应的主题帖
    author = db.relationship("User", backref="reviews")
    article = db.relationship("Article", backref="reviews")
    discussed = db.relationship('Discuss',
                                foreign_keys=[Discuss.discusser_id],
                                backref=db.backref('discusser', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')  # 被回复的帖子外键关联
    discusser = db.relationship('Discuss',
                                foreign_keys=[Discuss.discussed_id],
                                backref=db.backref('discussed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')  # 回复的帖子外键关联

    def __repr__(self):
        return "<Review %r>" % self.description

    def discuss(self, review):
        d = Discuss(discusser=review, discussed=self)
        db.session.add(d)

    def del_discuss(self, review):
        d = self.discussed.filter_by(discussed_id=review.id).first()
        if d:
            db.session.delete(d)

    def is_discussing(self, review):
        return self.discussed.filter_by(discussed_id=review.id).first() is not None

    def is_discussed_by(self, review):
        return self.discusser.filter_by(discusser_id=review.id).first() is not None


# Plate
class Plate(db.Model):
    __tablename__ = "plate"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 编号
    title = db.Column(db.Text)  # 版块标题

    def __repr__(self):
        return "<Plate %r>" % self.title


# Moderator
class Moderator(db.Model):
    __tablename__ = "moderator"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 编号
    moderator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 版主
    plate_id = db.Column(db.Integer, db.ForeignKey('plate.id'), nullable=False)  # 版主对应的版块
    moderator = db.relationship("User", backref="moderator")
    plate = db.relationship("Plate", backref="moderator")

    def __repr__(self):
        return "<Moderator %r>" % self.id


# Collect
class Collect(db.Model):
    __tablename__ = "collect"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 编号
    collector_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 收藏者
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)  # 收藏对应的主题帖
    collector = db.relationship("User", backref="collect")
    article = db.relationship("Article", backref="collect")

    def __repr__(self):
        return "<Collect %r>" % self.id


# Praise
class Praise(db.Model):
    __tablename__ = "praise"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 编号
    giver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 收藏者
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)  # 收藏对应的主题帖
    giver = db.relationship("User", backref="praise")
    article = db.relationship("Article", backref="praise")

    def __repr__(self):
        return "<Praise %r>" % self.id


# 这里是改进方案相关的模型 ###########################################################

class Improve(db.Model):
    __tablename__ = "improve"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 编号
    score = db.Column(db.Integer)  # 分数
    qua_score = db.Column(db.Integer)  # 代码质量分数
    cre_score = db.Column(db.Integer)  # 项目创新分数
    com_score = db.Column(db.Integer)  # 沟通能力分数
    word_score = db.Column(db.Integer)  # 文档分数
    review = db.Column(db.Text)  # 企业评价内容
    description = db.Column(db.Text)  # 方案内容
    name = db.Column(db.String(100))  # 方案名称
    url = db.Column(db.String(255))  # 项目文件存放地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 方案发布时间
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    demo_id = db.Column(db.Integer, db.ForeignKey('demo.id'), nullable=False)  # 方案对应的demand
    demo = db.relationship("Demo", backref="demo_improves")

    def find_demo(self, improve):
        demo = Demo.query.filter_by(id=improve.demo_id).first()
        return demo

    def number(self, demo):
        return len(demo.demo_improves)


if __name__ == '__main__':
    db.create_all()
