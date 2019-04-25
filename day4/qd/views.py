from flask import Blueprint, render_template, url_for

from hd.models import Article, Category

bp = Blueprint('blue',__name__)

@bp.route('/')
def index1():
    return 'hello'

@bp.route('/base_page/')
def base_page():
    return render_template('/web/base.html')

@bp.route('/about/')
def about1():
    return render_template('/web/about.html')

@bp.route('/gbook/')
def gbook():
    return render_template('/web/gbook.html')

@bp.route('/index/',methods=['GET'])
def index():
    articles = Article.query.all()
    categorys = Category.query.all()
    return render_template('/web/index.html',articles=articles,categorys=categorys)

@bp.route('/info/')
def about():
    return render_template('/web/info.html')

@bp.route('/infopic/')
def infopic():
    return render_template('/web/infopic.html')

@bp.route('/list/')
def list():
    return render_template('/web/list.html')

@bp.route('/share/')
def share():
    return render_template('/web/share.html')