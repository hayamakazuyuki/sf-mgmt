from flask import Blueprint, session, render_template, request

from .models import Shop

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if 'user' in session:
        
        page = request.args.get('page', 1, type=int)
        shops = Shop.query.paginate(page=page, per_page=20)
        count = len(Shop.query.all())

        return render_template('home.html', shops=shops, count=count)
   
    else:

        return render_template('index.html')
