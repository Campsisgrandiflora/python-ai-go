# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired

from app.models import Plate
from app.ext import flaskckeditor


class CKEditorForm(FlaskForm):
    title = StringField(
        label="帖子名称",
        validators=[
            DataRequired("请输入帖子名称")
        ],
        description="帖子名称",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入帖子名称",
            "id": "input_contact",
            # "required": "required"
        },
    )
    ckdemo = TextAreaField()
    belongedPlate = SelectField('所属版块:', coerce=int)
    url = FileField(
        label="附件",
        validators=[
            DataRequired("请上传附件")
        ],
        description="附件"
    )
    submit = SubmitField('submit')

    def __init__(self, *args, **kwargs):
        super(CKEditorForm, self).__init__(*args, **kwargs)
        self.belongedPlate.choices = [(belongedPlate.id, belongedPlate.title)
                                      for belongedPlate in Plate.query.all()]


class CommentForm(FlaskForm):
    ckdemo = TextAreaField()

    submit = SubmitField('submit')
