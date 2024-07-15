from flask import render_template, url_for, redirect, flash, request, jsonify, json
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime, date
import os
from flask_mail import Message
from . import main
from ..models import User
from .. import db, mail




basedir = os.getcwd()+"/app/xls"

@main.route('/')
@login_required
def index():
    
    return render_template('index.html', user=current_user)
