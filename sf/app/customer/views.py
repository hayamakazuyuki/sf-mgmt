from flask import Blueprint, render_template, request, flash, redirect, url_for

from ..extentions import db

# from ..models import Contractor, Satiscare

# from .forms import ContractorForm

customer = Blueprint('customer', __name__, url_prefix='/customer')

@customer.route('/')
def index():
    return render_template('customer/index.html')
