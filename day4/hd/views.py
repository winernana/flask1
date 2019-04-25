from datetime import datetime

from flask import Blueprint, render_template, request, session, make_response
from flask import redirect, url_for
from werkzeug.security import generate_password_hash,check_password_hash

from hd.models import db, User, Article, Category

hbp = Blueprint('h_blue',__name__)

@hbp.route('/')
def home():
    return 'hello'

@hbp.route('/register/',methods=['POST','GET'])
def register():
    if request.method == 'GET':
        return render_template('/back/register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = generate_password_hash(request.form.get('password'))
        print(username,password)
        try:
            user = User()
            user.username = username
            user.password = password
            db.session.add(user)
            db.session.commit()
            res= make_response(render_template('back/index.html'))
            # 设置cookie
            res.set_cookie('username',user.username,max_age=60*60*60*24)
            return res
        except:
            return '注册失败(该账号已存在)'

@hbp.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('/back/login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('userpwd')
        #验证
        print('*' * 20)
        print(password)
        users = User.query.filter(User.username == username)
        user = users.first()
        if user:
            if  check_password_hash(user.password,password):
                res = redirect('/hd/index')
                print('*'*20)
                # # 登陆成功 设置cookie给客户端,做识别用
                res.set_cookie('username',user.username,max_age=60*60*60*24)
                return res
            else:
                return render_template('back/login.html',p_err='密码错误')
        else:
            return render_template('/back/login.html',u_err='用户不存在')

@hbp.route('/index/',methods=['GET','POST'])
def index():
    articles = Article.query.all()
    count = len(articles)
    time = datetime.now()
    username = request.cookies.get('username')
    print(username)
    return render_template('/back/index.html',username=username,time=time,count=count)

# **************************************************************

@hbp.route('/category/',methods=['GET','POST'])
def category():
    username = request.cookies.get('username')
    if username:
        if request.method =='GET':
            return render_template('/back/category.html',username=username)
        if request.method == 'POST':
            name=request.form.get('name')
            # name_list=['前端技术','后端程序','管理系统','授人以鱼','程序人生']
            category = Category()
            category.c_name = name
            db.session.add(category)
            db.session.commit()
            return '栏目添加成功'
    else:
        return render_template('back/login.html')
@hbp.route('/article/',methods=['GET','POST'])
def article():
    username = request.cookies.get('username')
    if request.method == 'GET':
        articles = Article.query.all()
        count = len(articles)
        return render_template('/back/article.html',username=username,articles=articles,count=count)

@hbp.route('/add-article/',methods=['GET','POST'])
def add_article():
    username = request.cookies.get('username')
    if username:
        if request.method=='GET':
            categorys = Category.query.all()
            print(categorys[0].c_name)
            return render_template('/back/add-article.html',username=username,categorys=categorys)
        if request.method=='POST':
            title = request.form.get('title')
            content = request.form.get('content')
            desc = request.form.get('describe')
            type = request.form.get('category')
            article = Article()
            article.title = title
            article.content = content
            article.desc = desc
            article.type = type
            db.session.add(article)
            db.session.commit()
            return redirect('/hd/article')
    else:
        return render_template('back/login.html')
# *************************************************************************
#根据文章对象获取文章id,在根据文章id进行查找,进行修改
@hbp.route('/update-article/<int:id>/',methods=['GET','POST'])
# @hbp.route('/update-article/',methods=['GET','POST'])
def update_article(id):
    username = request.cookies.get('username')
    categorys = Category.query.all()
    if username:
        if request.method == 'GET':
            article = Article.query.get(id)
            # print(article.title)
            return render_template('/back/update-article.html',article=article,username=username,categorys=categorys)
        #修改文章
        if request.method == 'POST':
            title = request.form.get('title')
            content = request.form.get('content')
            desc = request.form.get('describe')
            type = request.form.get('category')
            article = Article.query.filter(Article.id == id).first()
            article.title = title
            article.content = content
            article.desc = desc
            article.type = type
            db.session.add(article)
            db.session.commit()
            return redirect('/hd/article')
        # 删除文章
        # if request.method == 'DELETE':
        #     article = Article.query.get(id)
        #     db.session.delete(article)
        #     db.session.commit()
        #     msg={
        #         'state':200,
        #         'response':'删除成功'
        #     }
            return  '删除文章成功'
    else:
        return render_template('back/login.html')
    # 删除文章
@hbp.route('/del_artcle/<int:id>',methods=['GET'])
def del_artcle(id):
    if request.method == 'GET':
        article = Article.query.get(id)
        db.session.delete(article)
        db.session.commit()
        return redirect('/hd/article')


@hbp.route('/notice/')
def notice():
    return render_template('/back/notice.html')

@hbp.route('/comment/')
def comment():
    return render_template('/back/comment.html')

@hbp.route('/add-flink/')
def add_flink():
    return render_template('/back/add-flink.html')

@hbp.route('/loginlog/')
def artloginlogicle():
    return render_template('/back/loginlog.html')

@hbp.route('/update-category/')
def update_category():
    return render_template('/back/update-category.html')

@hbp.route('/update-flink/')
def update_flink():
    return render_template('/back/update-flink.html')

@hbp.route('/create_db/',methods=['GET'])
def create_db():
    db.create_all()
    return '表单创建中......'


