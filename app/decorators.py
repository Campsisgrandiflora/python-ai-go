# -*- coding:utf-8 -*-

from flask import session, redirect, url_for, request, abort
from .models import Admin, Role, Auth
from functools import wraps


# 用户登录限制装饰器
def user_login_reg(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id') and session.get('is_user'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('user.login', next=request.url))

    return wrapper


# 企业登录限制装饰器
def enterprise_login_reg(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id') and not session.get('is_user'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('enterprise.login', next=request.url))

    return wrapper


# 使用者登录限制器
def person_login_reg(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('user.login', next=request.url))

    return wrapper


# 管理员登录装饰器
def admin_login_reg(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get('admin') is None:
            return redirect(url_for("admin.login", next=request.url))
        return func(*args, **kwargs)

    return decorated_function


# 权限控制装饰器
def admin_auth(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        admin = Admin.query.join(Role).filter(
            Role.id == Admin.role_id,
            Admin.id == session["admin_id"],
        ).first()
        auths = admin.role.auths
        auths = list(map(lambda v: int(v), auths.split(",")))
        auth_list = Auth.query.all()
        urls = [v.url for v in auth_list for val in auths if val == v.id]
        rule = request.url_rule
        if rule not in urls:
            abort(404)
        return func(*args, **kwargs)

    return decorated_function
