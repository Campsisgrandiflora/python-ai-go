# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, BooleanField, \
    IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Regexp
from app.ext.evaluate import EVALUATE


class DemoForm(FlaskForm):
    """demo发布表单"""
    name = StringField(
        label="demo名称",
        validators=[
            DataRequired("请输入demo名称")
        ],
        description="demo名称",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入demo名称",
            "id": "input_contact",
            # "required": "required"
        },
    )
    per_price = IntegerField(
        label="众筹单价",
        validators=[
            DataRequired("请输入众筹单价")
        ],
        description="众筹单价",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入众筹单价",
            "id": "input_contact",
            # "required": "required"
        },
    )
    price = IntegerField(
        label="众筹总价",
        validators=[
            DataRequired("请输入众筹总价")
        ],
        description="众筹总价",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入众筹总价",
            "id": "input_contact",
            # "required": "required"
        },
    )

    description = TextAreaField(
        label="demo描述",
        validators=[
            DataRequired("请输入描述")
        ],
        description="描述",
        render_kw={
            "class": "form-control",
            "id": "input-description",
            "row": 10,
        }
    )

    url = FileField(
        label="附件",
        # validators=[
        #     DataRequired("请上传附件")
        # ],
        description="附件"
    )

    submit = SubmitField(
        "提交demo",
        render_kw={
            "class": "btn btn-primary btn-block",
            "action": "/demo/",
        }
    )


class ResolveForm(FlaskForm):
    """解决方案发布表单"""
    name = StringField(
        label="解决方案名称",
        validators=[
            DataRequired("请输入解决方案名称")
        ],
        description="解决方案名称",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入解决方案名称",
            "id": "input_contact",
            # "required": "required"
        },
    )

    description = TextAreaField(
        label="解决方案描述",
        validators=[
            DataRequired("请输入描述")
        ],
        description="描述",
        render_kw={
            "class": "form-control",
            "id": "input-description",
            "row": 10,
        }
    )

    url = FileField(
        label="附件",
        # validators=[
        #     DataRequired("请上传附件")
        # ],
        description="附件"
    )

    submit = SubmitField(
        "提交解决方案",
        render_kw={
            "class": "btn btn-primary btn-block",
            "action": "/resolve/",
        }
    )


class GradeForm(FlaskForm):
    qua_score = SelectField(coerce=int,
                            render_kw={

                                "id": "input-description",
                                'display': 'inline'
                            }
                            )
    cre_score = SelectField(coerce=int,
                            render_kw={

                                "id": "input-description",
                                'display': 'inline'
                            }
                            )
    score = SelectField(coerce=int,
                        render_kw={

                            "id": "input-description",
                            'display': 'inline'
                        }
                        )
    submit = SubmitField('submit')

    def __init__(self, *args, **kwargs):
        super(GradeForm, self).__init__(*args, **kwargs)
        self.score.choices = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'),
                              (10, '10')]
        self.qua_score.choices = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'),
                                  (9, '9'), (10, '10')]
        self.cre_score.choices = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'),
                                  (9, '9'), (10, '10')]


class CommentForm1(FlaskForm):
    ckdemo = TextAreaField()
    submit = SubmitField('submit')


class CommentForm(FlaskForm):
    qua_score = SelectField(coerce=int,
                            render_kw={

                                "id": "input-description",
                                'display': 'inline'
                            }
                            )
    cre_score = SelectField(coerce=int,
                            render_kw={

                                "id": "input-description",
                                'display': 'inline'
                            }
                            )
    score = SelectField(coerce=int,
                        render_kw={

                            "id": "input-description",
                            'display': 'inline'
                        }
                        )
    ckdemo = TextAreaField()
    submit = SubmitField('submit')

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.score.choices = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'),
                              (10, '10')]
        self.qua_score.choices = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'),
                                  (9, '9'), (10, '10')]
        self.cre_score.choices = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'),
                                  (9, '9'), (10, '10')]


class DemandForm(FlaskForm):
    """demand发布表单"""
    name = StringField(
        label="需求名称",
        validators=[
            DataRequired("请输入需求名称")
        ],
        description="需求名称",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入需求名称",
            "id": "input_contact",
            # "required": "required"
        },
    )

    description = TextAreaField(
        label="需求描述",
        validators=[
            DataRequired("请输入描述")
        ],
        description="需求描述",
        render_kw={
            "class": "form-control",
            "id": "input-description",
            "row": 10,
        }
    )

    finish_time = StringField(
        label="截止时间",
        validators=[
            DataRequired("请输入截止时间")
        ],
        description="截止时间",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入截止时间",
            "id": "datepicker",
        }
    )

    url = FileField(
        label="附件",
        # validators=[
        #     DataRequired("请上传附件")
        # ],
        description="附件"
    )

    submit = SubmitField(
        "提交需求",
        render_kw={
            "class": "btn btn-primary btn-block",
            "action": "/demand/",
        }
    )


class CodeForm(FlaskForm):
    code = TextAreaField(
        render_kw={
            "id": "code",
        }
    )

    submit = SubmitField(
        "运行",
        render_kw={
            "class": "btn btn-default",
            "id": "btn-submit",
            "value": "测试",
            # "action": "/coderunning/",
        }
    )

    test = StringField(
        '输入需要<br>测试的函数',
        render_kw={
            "class": "",
            "style": "width: 500px",
            "id": "btn-submit",
        }
    )

    # category = SelectField(
    #     coerce=int,
    #     choices=[(1,' '), (2, '分类问题'), (3, '智能信息检索'), (4, '模式识别'),
    #              (5, '深度学习'), (6, '推荐系统')]
    # )

    # index = SelectField(
    #     coerce=int,
    #     choices=[(1, ' '), (2, '准确度'), (3, '覆盖率'), (4, '新颖性'), (5, '多样性'),
    #              (6, '流行度')]
    # )

    # aitest = SubmitField(
    #     "选择需要<br>测试指标",
    #     render_kw={
    #         "class": "btn btn-default",
    #         "id": "btn-submit",
    #         "value": "测试",
    #         # "action": "/coderunning/",
    #     }
    # )


class GradeForm(FlaskForm):
    com_score = SelectField(coerce=int,
                            render_kw={
                                'class': 'form-group',
                                "id": "input-description",
                                'display': 'inline',
                                'style': 'width:300px;'
                            }
                            )
    word_score = SelectField(coerce=int,
                             render_kw={
                                 'class': 'form-group',
                                 "id": "input-description",
                                 'display': 'inline',
                                 'style': 'width:300px;'
                             }
                             )
    qua_score = SelectField(coerce=int,
                            render_kw={
                                'class': 'form-group',
                                "id": "input-description",
                                'display': 'inline',
                                'style': 'width:300px;'
                            }
                            )
    cre_score = SelectField(coerce=int,
                            render_kw={
                                'class': 'form-group',
                                "id": "input-description",
                                'display': 'inline',
                                'style': 'width:300px;'
                            }
                            )
    score = SelectField(coerce=int,
                        render_kw={
                            'class': 'form-group',
                            "id": "input-description",
                            'display': 'inline',
                            'style': 'width:300px;'
                        }
                        )
    review = TextAreaField(
        label="评价",
        validators=[
            DataRequired("请输入评价")
        ],
        description="评价",
        render_kw={
            "class": "form-control",
            "id": "input-description",
            "row": 20,
            'style': 'width:300px;height:180px'
        }
    )
    submit = SubmitField('submit')

    def __init__(self, *args, **kwargs):
        super(GradeForm, self).__init__(*args, **kwargs)
        self.score.choices = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'),
                              (10, '10')]
        self.qua_score.choices = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'),
                                  (9, '9'), (10, '10')]
        self.cre_score.choices = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'),
                                  (9, '9'), (10, '10')]
        self.com_score.choices = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'),
                                  (9, '9'), (10, '10')]
        self.word_score.choices = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'),
                                   (9, '9'), (10, '10')]


class ImproveForm(FlaskForm):
    """改进方案发布表单"""
    name = StringField(
        label="改进方案名称",
        validators=[
            DataRequired("请输入改进方案名称")
        ],
        description="改进方案名称",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入改进方案名称",
            "id": "input_contact",
            # "required": "required"
        },
    )

    description = TextAreaField(
        label="改进方案描述",
        validators=[
            DataRequired("请输入描述")
        ],
        description="描述",
        render_kw={
            "class": "form-control",
            "id": "input-description",
            "row": 10,
        }
    )

    url = FileField(
        label="附件",
        # validators=[
        #     DataRequired("请上传附件")
        # ],
        description="附件"
    )

    submit = SubmitField(
        "提交改进方案",
        render_kw={
            "class": "btn btn-primary btn-block",
            "action": "/improve/",
        }
    )


class PortraitForm(FlaskForm):
    choice = []
    i = 0
    for e in EVALUATE:
        choice.append((i, e))
        i = i + 1

    select = SelectMultipleField(
        '请选择要查看的指标',
        choices=choice,
        render_kw={
            "class": "form-group",
        }
    )

    submit = SubmitField(
        '筛选',
        render_kw={
            "class": "btn btn-info",
        }
    )
