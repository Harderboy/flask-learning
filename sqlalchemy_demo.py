from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 配置数据库的地址 注意是：mysql+pymysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1/flask_sql_demo'
# 跟踪数据库的修改-》不建议开启，未来的版本会移除
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

'''
两张表
角色：管理员 普通用户
用户（角色id）
'''
'''
>>>from  sqlalchemy_demo import *
# 添加
>>> role=Role(name='admin')
>>> db.session.add(role)
>>> db.session.add_all([user1,user2])
>>> db.session.commit()
>>> user=User(name="he",role_id=role.id)
>>> db.session.add(user)
>>> db.session.commit()
# 修改
>>> user.name='chengxuyuan'
>>> db.session.commit()
# 删除
>>> db.session.delete(user)
>>> db.session.commit()
# 数据库回滚
db.session.rollback()
'''


# 数据库模型 需要继承db.Model
class Role(db.Model):
    # 定义表
    __tablename__ = 'roles'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)

    # 在一的一方，写关联
    # db.relationship('User') 表示和User模型发生了关联，增加了一个User属性
    # backref="role": 表示role是User要用的属性
    users = db.relationship('User', backref="role")

    def __repr__(self):
        return '<Role:%s %s>' % (self.name, self.id)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    email = db.Column(db.String(32), unique=True)
    passwd = db.Column(db.String(32))
    # db.ForeignKey("roles.id") 表示是外键，表名.id
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    # User希望有role属性，但是这个属性的定义需要在另一个模型中定义

    def __repr__(self):
        return 'User:%s %s %s %s>' % (self.name, self.id, self.email, self.passwd)


@app.route("/")
def index():
    return "hello world"


if __name__ == "__main__":
    # 删除表
    db.drop_all()

    # 创建表
    db.create_all()

    role1 = Role(name='admin')
    role2 = Role(name='normal')
    db.session.add_all([role1, role2])
    db.session.commit()
    user1 = User(name="essa", role_id=role1.id, email="111", passwd="111")
    user2 = User(name="isi", role_id=role2.id, email="222", passwd="222")
    user3 = User(name="wigwag", role_id=role1.id, email="333", passwd="333")
    user4 = User(name="Elihu", role_id=role2.id, email="444", passwd="444")
    user5 = User(name="maxi", role_id=role1.id, email="555", passwd="555")
    db.session.add_all([user1, user2, user3, user4, user5])
    db.session.commit()
    app.run(debug=True)
