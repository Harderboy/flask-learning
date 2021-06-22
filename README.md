# Flask Learning Notes

Python web 框架 flask 入门笔记

## 变量规则

视图函数传参（待补充）


## 模版标签

Django

```html
{% for X in Y %}
    语句1
<!-- 序列 Y 为空或者序列不存在，循环为空时（即 in 后面的参数布尔值为 False ）执行语句2，可选的 -->
{% empty %}  
    语句2
{% endfor %}
```

Flask

```html
{% for book in author.books %}
    <li>{{ book.name }}<a href="{{ url_for('delete_book',book_id=book.id) }}">删除</a></li>
{% else %}
    <li>无</li>
{% endfor %}
```


## 模版-过滤器

过滤器使用方式： 

`{{var(变量名)|过滤器}}`

`{{var|filter_name(*args)}}`

- 没有参数传递给过滤器的话，参数可以省略

链式调用：  
jinja2 中过滤器支持链式调用

`{{"hello"|upper|reverse}}`

常见内置过滤器


## 数据库相关

查询
filter     类名.字段   ==  更强大 支持多列、操作符等
filter_by  字段       =   只支持单列查询      

查询之后直接删除（批量删除）

`Book.query.filter_by(author_id=author_id).delete()`

- 此操作是否需要经过数据库（add、commit）

参考链接： 
- [快速入门](http://docs.jinkan.org/docs/flask/quickstart.html)
