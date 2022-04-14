from crypt import methods
from flask import Blueprint, render_template

from .forms import ContractorForm

contractor = Blueprint('contractor', __name__, url_prefix='/contractor')

@contractor.route('/')
def index():
    return render_template('index.html')


@contractor.route('/register', methods=['GET', 'POST'])
def register():

    form = ContractorForm()

    if form.validate_on_submit():
        return 'おっけ'

    return render_template('contractor/register.html', form=form)
