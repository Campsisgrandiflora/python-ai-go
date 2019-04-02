# coding: utf-8
from flask import render_template, redirect, url_for, flash, session, request
from . import admin
from app.admin.forms import LoginForm, TagForm, AuthForm, RoleForm, AdminForm
from app.models import db, Admin, Tag, User, Auth, Role, Demo, Demand
from app.decorators import admin_login_reg
from app import app
from werkzeug.utils import secure_filename
import os, uuid, datetime


@admin.route('/')
@admin_login_reg
def index():
    return render_template('admin/index.html')


# 登录
@admin.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data['account']).first()
        if admin.pwd != data['pwd']:
            flash("密码错误！")
            return redirect(url_for('admin.login'))
        session['admin'] = data["account"]
        return redirect(request.args.get("next") or url_for("admin.index"))
    return render_template('admin/login.html', form=form)


# 登出
@admin.route('/logout/')
@admin_login_reg
def logout():
    session.clear()
    return redirect(url_for("admin.login"))


@admin.route('/pwd/')
@admin_login_reg
def pwd():
    return render_template("admin/pwd.html")


# 添加标签
@admin.route("/tag/add/", methods=["GET", "POST"])
@admin_login_reg
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag = Tag.query.filter_by(name=data['name']).count()
        if tag == 1:
            flash("标签已经存在", "err")
            return redirect(url_for('admin.tag_add'))
        tag = Tag(
            name=data['name']
        )
        db.session.add(tag)
        db.session.commit()
        flash("添加标签成功", "ok")
        redirect(url_for("admin.tag_add"))
    return render_template("admin/tag_add.html", form=form)


# 标签列表
@admin.route("/tag/list/<int:page>/", methods=['GET'])
@admin_login_reg
def tag_list(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(
        Tag.id.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/tag_list.html", page_data=page_data)


# 编辑标签
@admin.route("/tag/edit/<int:id>", methods=['GET', 'POST'])
@admin_login_reg
def tag_edit(id=None):
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data['name']).count()
        if tag.name != data["name"] and tag_count == 1:
            flash("标签已经存在", "err")
            return redirect(url_for('admin.tag_edit', id=id))
        tag.name = data['name']
        db.session.add(tag)
        db.session.commit()
        flash("修改标签成功", "ok")
        return redirect(url_for("admin.tag_add", id=id))
    return render_template("admin/tag_edit.html", form=form, tag=tag)


# 标签删除
@admin.route("/tag/del/<int:id>", methods=['GET'])
@admin_login_reg
def tag_del(id=None):
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash("删除标签成功", "ok")
    return redirect(url_for("admin.tag_list", page=1))


# demo列表
@admin.route("/demo/list/<int:page>", methods=['GET'])
@admin_login_reg
def demo_list(page=None):
    if page is None:
        page = 1
    page_data = Demo.query.order_by(
        Demo.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/demo_list.html", page_data=page_data)


# 需求列表
@admin.route("/demand/list/<int:page>", methods=['GET'])
@admin_login_reg
def demand_list(page=None):
    if page is None:
        page = 1
    page_data = Demand.query.order_by(
        Demand.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/demand_list.html", page_data=page_data)


# 用户列表
@admin.route("/user/list/<int:page>", methods=['GET'])
@admin_login_reg
def user_list(page=None):
    if page is None:
        page = 1
    page_data = User.query.order_by(
        User.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/user_list.html", page_data=page_data)


# 添加权限
@admin.route("/auth/add/", methods=["GET", "POST"])
@admin_login_reg
def auth_add():
    form = AuthForm()
    if form.validate_on_submit():
        data = form.data
        auth = Auth.query.filter_by(name=data['name']).count()
        if auth == 1:
            flash("权限已经存在", "err")
            return redirect(url_for('admin.tag_add'))
        auth = Auth(
            name=data['name'],
            url=data['url'],
        )
        db.session.add(auth)
        db.session.commit()
        flash("添加权限成功", "ok")
        redirect(url_for("admin.tag_add"))
    return render_template("admin/auth_add.html", form=form)


# 权限列表
@admin.route("/auth/list/<int:page>", methods=['GET'])
@admin_login_reg
def auth_list(page=None):
    if page is None:
        page = 1
    page_data = Auth.query.order_by(
        Auth.id.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/auth_list.html", page_data=page_data)


# 编辑权限
@admin.route("/auth/edit/<int:id>", methods=['GET', 'POST'])
@admin_login_reg
def auth_edit(id=None):
    form = AuthForm()
    auth = Auth.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        auth_count = Auth.query.filter_by(name=data['name']).count()
        if auth.name != data["name"] and auth_count == 1:
            flash("权限已经存在", "err")
            return redirect(url_for('admin.auth_edit', id=id))
        auth.name = data['name']
        db.session.add(auth)
        db.session.commit()
        flash("修改权限成功", "ok")
        return redirect(url_for("admin.auth_add", id=id))
    return render_template("admin/auth_edit.html", form=form, auth=auth)


# 权限删除
@admin.route("/auth/del/<int:id>", methods=['GET'])
@admin_login_reg
def auth_del(id=None):
    auth = Auth.query.filter_by(id=id).first_or_404()
    db.session.delete(auth)
    db.session.commit()
    flash("删除权限成功", "ok")
    return redirect(url_for("admin.auth_list", page=1))


# 添加角色
@admin.route("/role/add/", methods=['GET', 'POST'])
@admin_login_reg
def role_add():
    form = RoleForm()
    if form.validate_on_submit():
        data = form.data
        role = Role(
            name=data["name"],
            auths=",".join(map(lambda v: str(v), data["auths"]))
        )
        db.session.add(role)
        db.session.commit()
        flash("添加角色成功！", "ok")
    return render_template("admin/role_add.html", form=form)


# 角色列表
@admin.route("/role/list/<int:page>", methods=['GET'])
@admin_login_reg
def role_list(page=None):
    if page is None:
        page = 1
    page_data = Role.query.order_by(
        Role.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/role_list.html", page_data=page_data)


# 编辑角色
@admin.route("/role/edit/<int:id>", methods=['GET', 'POST'])
@admin_login_reg
def role_edit(id=None):
    form = RoleForm()
    role = Role.query.get_or_404(id)
    if request.method == "GET":
        auths = role.auths
        form.auths.data = list(map(lambda v: int(v), auths.split(",")))
    if form.validate_on_submit():
        data = form.data
        role.name = data["name"]
        role.auths = ",".join(map(lambda v: str(v), data["auths"]))
        db.session.add(role)
        db.session.commit()
        flash("修改角色成功", "ok")
        return redirect(url_for("admin.tag_add", id=id))
    return render_template("admin/role_edit.html", form=form, role=role)


# 角色删除
@admin.route("/role/del/<int:id>", methods=['GET'])
@admin_login_reg
def role_del(id=None):
    role = Role.query.filter_by(id=id).first_or_404()
    db.session.delete(role)
    db.session.commit()
    flash("删除角色成功", "ok")
    return redirect(url_for("admin.role_list", page=1))


# 添加管理员
@admin.route("/admin/add/", methods=['GET', 'POST'])
@admin_login_reg
def admin_add():
    form = AdminForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin(
            name=data["name"],
            pwd=data["pwd"],
        )
        db.session.add(admin)
        db.session.commit()
        flash("添加角色成功！", "ok")
    return render_template("admin/admin_add.html", form=form)


# 角色列表
@admin.route("/admin/list/<int:page>", methods=['GET'])
@admin_login_reg
def admin_list(page=None):
    if page is None:
        page = 1
    page_data = Admin.query.order_by(
        Admin.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/admin_list.html", page_data=page_data)
