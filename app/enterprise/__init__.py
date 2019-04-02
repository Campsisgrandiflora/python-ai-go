# -*- coding:utf-8 -*-

from flask import Blueprint

enterprise = Blueprint("enterprise", __name__)

from . import views
