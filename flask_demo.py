from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

app = Flask(__name__)
app.secret_key = "htomato"  # 使用flash时需要这一项配置

'''
通过把 URL 的一部分标记为 <variable_name> 就可以在 URL 中添加变量。标记的 部分会作为关键字参数传递给函数。
@app.route('/post/<int:post_id>')
通过使用 <converter:variable_name>，可以选择性的加上一个转换器，为变量指定规则。
https://dormousehole.readthedocs.io/en/latest/quickstart.html#id2
'''


@app.route("/order/<order_id>", methods=["GET"])
def get_order_id(order_id):
    return "order_id:%s" % order_id


@app.route("/index", methods=["GET"])
def index():
    # return "hello flask"
    url_str = "https://github.com/Harderboy/Python_notes/blob/main/Django/Django_Template_Notes.md"

    my_list = [1, 2, 3, 4, 5, 6]
    my_dict = {
        'name': 'github 学习笔记',
        'url': 'https://github.com/Harderboy/Python_notes/blob/main/Django/Django_Template_Notes.md',
    }
    my_int = 22
    return render_template("index.html", url_str=url_str, my_list=my_list, my_dict=my_dict, my_int=my_int)


'''
目的：实现一个j简单的登录逻辑处理
1.请求方式包括：get、post 需要判断请求方式
2.获取请求的参数
3.判断参数是否填写&密码是否一致
4.都没有问题返回一个success
'''
'''
给模版传递消息
flash-->需要对内容进行加密，因此需要设置secret_key,做加密消息的混淆
模版中需要遍历消息
'''


@app.route("/login", methods=["GET", "POST"])
def login():
    # 1.判断请求方式
    if request.method == "POST":
        # 2.获取表单数据
        username = request.form.get("username")
        passwd = request.form.get("passwd")
        confirm_passwd = request.form.get("confirm_passwd")
        # print(username,passwd,confirm_passwd)
        # 3.判断参数是否填写&密码是否一致
        if not all([username, passwd, confirm_passwd]):
            # print("参数不完整")
            flash("参数不完整")
        elif passwd != confirm_passwd:
            # print("密码不一致")
            flash("密码不一致")
        else:
            return "success"
    return render_template("login.html")


'''
使用WTF实现表单
自定义表单类
'''


class LoginForm(FlaskForm):
    username = StringField("用户名：", validators=[DataRequired()])
    passwd = PasswordField("密码：", validators=[DataRequired()])
    confirm_passwd = PasswordField("确认密码：", validators=[DataRequired(), EqualTo("passwd", "密码填入的不一致")])
    submit = SubmitField("提交:")


@app.route("/form", methods=["GET", "POST"])
def login2():
    login_form = LoginForm()
    # 1.判断请求方式
    if request.method == "POST":
        # 2.获取表单数据
        username = request.form.get("username")
        passwd = request.form.get("passwd")
        confirm_passwd = request.form.get("confirm_passwd")
        # print(username,passwd,confirm_passwd)
        # 3.判断参数是否填写&密码是否一致 WTF可以一句话就实现所有的校验
        # 模版中没有 crsf_token 的话，会报错，WTF自带完整的验证机制
        if login_form.validate_on_submit():
            print(username, passwd)
            return "success"
        else:
            flash("参数有误")
    return render_template("login.html", form=login_form)


if __name__ == '__main__':
    app.run(debug=True)
