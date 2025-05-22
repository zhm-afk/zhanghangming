#!/usr/bin/env python3
from werkzeug.security import generate_password_hash

admins = [
    {'username': '张航铭', 'nickname': '张航铭', 'password': 'zhanghangming', 'role': 'super'},
    {'username': '唐涛', 'nickname': '唐涛', 'password': 'tangtao', 'role': 'normal'},
    {'username': '蓝金桥', 'nickname': '蓝金桥', 'password': 'lanjinqiao', 'role': 'normal'},
    {'username': '肖欣芮', 'nickname': '肖欣芮', 'password': 'xiaoxinrui', 'role': 'normal'}
]

with open('admin_inserts.sql', 'w') as f:
    for admin in admins:
        password_hash = generate_password_hash(admin['password'])
        sql = f"INSERT INTO admins (username, nickname, password_hash, role) VALUES ('{admin['username']}', '{admin['nickname']}', '{password_hash}', '{admin['role']}');\n"
        f.write(sql)
        print(sql, end='')

print("\n管理员SQL语句已生成到 admin_inserts.sql 文件中") 