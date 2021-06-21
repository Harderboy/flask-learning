from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = "books"

# 配置数据库的地址 注意是：mysql+pymysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1/flask_books_demo'
# 跟踪数据库的修改-》不建议开启，未来的版本会移除
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

"""
1.配置数据库
2.导入书和作者模型
3.添加数据
4 使用模版显示数据库查询的数据
5 使用WTF显示表单
6 实现相关的增删逻辑
    a.增
    b.删 点击删除--》网页中删除--》点击需要发送书籍的id给删除书籍的路由——》路由需要接受参数
    
"""


class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)

    books = db.relationship('Book', backref='author')

    def __repr__(self):
        return "Author:%s" % self.name


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)

    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))

    def __repr__(self):
        return "Books:%s %s" % (self.name, self.author_id)


class AuthorForm(FlaskForm):
    author = StringField("作者：", validators=([DataRequired()]))
    book = StringField("书名：", validators=([DataRequired()]))
    submit = SubmitField("提交")


@app.route("/", )
def index():
    author_form = AuthorForm()

    authors = Author.query.all()
    return render_template("book.html", authors=authors, form=author_form)


@app.route("/add", methods=["POST", "GET"])
def add():
    author_form = AuthorForm()
    # 查询所有作者的信息，传递给模版
    authors = Author.query.all()

    '''
    验证逻辑
    1）调用WTF的函数实现验证
    2）验证通过获取数据
    3）判断作者是否存在
    4）作者存在 书籍是否存在，没有重复书籍就添加书籍，如果重复就提示错误
    5）作者不存在 添加作者和书籍
    6）验证不通过提示错误
    '''
    # 1）调用WTF的函数实现验证
    # get请求进不来，post请求才会进去
    if author_form.validate_on_submit():
        # 2）验证通过获取数据
        author_name = author_form.author.data
        book_name = author_form.book.data
        # 3）判断作者是否存在
        author = Author.query.filter_by(name=author_name).first()
        if author:
            # 4）作者存在 书籍是否存在，没有重复书籍就添加书籍，如果重复就提示错误
            book = Book.query.filter_by(name=book_name).first()
            if book:
                flash("已存在同名书籍")
            else:
                try:
                    new_book = Book(name=book_name, author_id=author.id)
                    db.session.add(new_book)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    flash("添加书籍出错")
                    db.session.rollback()
        else:
            # 5）作者不存在 添加作者和书籍
            try:
                new_author = Author(name=author_name)
                db.session.add(new_author)
                db.session.commit()
                new_book = Book(name=book_name, author_id=new_author.id)
                db.session.add(new_book)
                db.session.commit()
            except Exception as e:
                print(e)
                flash("添加作者和书籍出错")
                db.session.rollback()
    else:
        # 6）验证不通过提示错误
        if request.method == "POST":
            flash("参数不全")

    return render_template("book.html", authors=authors, form=author_form)

# 点击删除--》网页中删除--》点击需要发送书籍的id给删除书籍的路由——》路由需要接受参数
@app.route("/delete_book/<book_id>", methods=["POST", "GET"])
def delete_book(book_id):
    # 1 查询数据库，是否由该ID的书，如果有就删除
    book=Book.query.get(book_id)
    # 2.如果有就删除
    if book:
        try:
            db.session.delete(book)
            db.session.commit()
        except Exception as e:
            print(e)
            flash("删除数据出错")
            db.session.rollback()

    # redirect 重定向，需要传入网络/路由地址
    # url_for("index") 需要传入视图函数名，返回视图函数对应的路由地址
    # url_for('delete_book',book_id=book.id) 视图函数带有参数传参方式

    # 重定向 返回当前地址
    # return redirect("www.runnoob.com")
    # return redirect("/")
    # return redirect(url_for('index'))
    print(url_for('index'))  # /
    return redirect(url_for('index'))  # return redirect("/")

# 点击删除--》网页中删除--》点击需要发送作者的id给删除作者的路由——》路由需要接受参数
@app.route("/delete_author/<author_id>", methods=["POST", "GET"])
def delete_author(author_id):
    # 查询数据库，有该id的作者就删除（先删书再删作者），没有提示错误
    # 1 查数据库
    author=Author.query.get(author_id)
    # 2 如果有就删除，先删书再删人
    if author:
        try:
            # 查询之后直接删除
            Book.query.filter_by(author_id=author_id).delete()
            # 删除作者
            db.session.delete(author)
            db.session.commit()
        except Exception as e:
            print(e)
            flash("删除作者出错")
            db.session.rollback()
    else:
        # 3 没有提示错误
        flash("作者找不到")
    return redirect(url_for('index'))

if __name__ == "__main__":
    db.drop_all()

    # 创建表
    db.create_all()

    author1 = Author(name="老王")
    author2 = Author(name="恒大也")
    db.session.add_all([author1, author2])
    db.session.commit()

    book1 = Book(name="秀才遇到兵1", author_id=author1.id)
    book2 = Book(name="秀才遇到兵2", author_id=author1.id)
    book3 = Book(name="秀才遇到兵3", author_id=author2.id)
    book4 = Book(name="秀才遇到兵4", author_id=author1.id)
    book5 = Book(name="秀才遇到兵5", author_id=author2.id)
    db.session.add_all([book1, book2, book3, book4, book5])
    db.session.commit()

    app.run(debug=True)
