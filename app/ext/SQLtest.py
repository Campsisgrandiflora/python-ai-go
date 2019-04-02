from app.models import user_tag
import pymysql

# 创建连接
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='lkj123', db='aigo', charset='utf8')
# 创建游标
cursor = conn.cursor()

cursor.execute("select tag_id, user_id from user_tag WHERE id=2")
cursor.execute("SELECT user_id FROM user_tag WHERE ")
row_1 = cursor.fetchone()
print(type(row_1))
