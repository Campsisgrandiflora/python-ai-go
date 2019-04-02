# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Regexp
from app.models import Enterprise


class LoginForm(FlaskForm):
    """企业登录表单"""
    email = StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号")
        ],
        description="账号",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入邮箱",
            "id": "input_contact",
            # "required": "required"
        },
    )

    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码"),
        ],
        description="密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入密码",
            "id": "input_pwd",
            # "required": "required"
        }
    )

    submit = SubmitField(
        '登录',
        render_kw={
            "class": "btn btn-lg btn-info",
            "style": "margin-left: 20px;",
        }
    )

    def validate_email(self, field):
        email = field.data
        user = Enterprise.query.filter_by(email=email).count()
        if user == 0:
            raise ValidationError('账号不存在')


class RegisterForm(FlaskForm):
    """企业注册表单"""
    name = StringField(
        label="企业名称",
        validators=[
            DataRequired("请输入企业名称")
        ],
        description="企业名称",
        render_kw={
            "id": "input_name",
            "class": "form-control input-lg",
            "placeholder": "请输入企业名称",
        },
    )

    email = StringField(
        label="邮箱",
        validators=[
            DataRequired("请输入邮箱"),
            Email("邮箱格式不正确")
        ],
        description="邮箱",
        render_kw={
            "id": "input_email",
            "class": "form-control input-lg",
            "placeholder": "请输入邮箱",

        },
    )

    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码"),
        ],
        description="密码",
        render_kw={
            "id": "input_password",
            "class": "form-control input-lg",
            "placeholder": "请输入密码",
        }
    )

    repwd = PasswordField(
        label="确认密码",
        validators=[
            DataRequired("请输入确认密码"),
            EqualTo('pwd', message="两次密码不相等")
        ],
        description="确认密码",
        render_kw={
            "id": "input_repassword",
            "class": "form-control input-lg",
            "placeholder": "请输入确认密码",
        }
    )

    submit = SubmitField(
        '注册',
        render_kw={
            "class": "btn btn-lg btn-success btn-block",
        }
    )


    def validate_name(self, field):
        name = field.data
        user = Enterprise.query.filter_by(name=name).count()
        if user == 1:
            raise ValidationError("企业名称已经存在")

    def validate_email(self, field):
        email = field.data
        user = Enterprise.query.filter_by(email=email).count()
        if user == 1:
            raise ValidationError("邮箱已经存在")


class EnterpriseDetailForm(FlaskForm):
    """企业信息表单"""
    name = StringField(
        label="企业名称",
        validators=[
            DataRequired("请输入企业名称")
        ],
        description="企业名称",
        render_kw={
            "id": "input_name",
            "class": "form-control input-lg",
            "placeholder": "请输入企业名称",
        },
    )

    email = StringField(
        label="邮箱",
        validators=[
            DataRequired("请输入邮箱"),
            Email("邮箱格式不正确")
        ],
        description="邮箱",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入邮箱",
            "id": "input_contact",
            # "required": "required"
        },
    )

    phone = StringField(
        label="手机",
        # validators=[
        #     DataRequired("请输入手机"),
        #     Regexp("1[3458]\\d{9}", message='手机格式不正确！')
        # ],
        description="手机",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入手机",
            "id": "input_contact",
            # "required": "required"
        },
    )

    face = FileField(
        label="头像",
        # validators=[
        #     DataRequired("请上传头像")
        # ],
        description="头像"
    )

    qq = StringField(
        label="qq",
        validators=[
            DataRequired("请输入qq"),
        ],
        description="qq",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入qq",
            "id": "input_contact",
            # "required": "required"
        },
    )

    info = TextAreaField(
        label="简介",
        # validators=[
        #     DataRequired("请输入简介")
        # ],
        description="简介",
        render_kw={
            "class": "form-control",
            "row": 10,
        }
    )

    submit = SubmitField(
        ' 保存修改',
        render_kw={
            "class": "btn btn-success",
        }
    )

    def validate_email(self, field):
        email = field.data
        user = Enterprise.query.filter_by(email=email).count()
        if user == 0:
            raise ValidationError('账号不存在')


class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label='旧密码',
        validators=[
            DataRequired("请输入旧密码"),
        ],
        description="旧密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入旧密码",
        }
    )

    new_pwd = PasswordField(
        label='新密码',
        validators=[
            DataRequired("请输入新密码"),
        ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入新密码",
        }
    )

    submit = SubmitField(
        ' 修改密码',
        render_kw={
            "class": "btn btn-success",
        }
    )
