# -*- coding:utf-8 -*-
from app import app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.models import *

# init
# migrate
# upgrade
# 模型 -> 迁移文件 -> 表

manage = Manager(app)

# 要使用migrate必须绑定app和db
# 使用migrate绑定app和db
migrate = Migrate(app, db)

# 把MigrateCommand命令添加到manage中
# 添加迁移脚本的命令到manage
manage.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manage.run()
