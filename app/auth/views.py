from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth
from .forms import Login, Register, PasswordChange, UserEdit
from ..models import User
from .. import db
from flask import current_app as app




@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email = form.email.data).first()
            if user:
                flash('The email address has already been used to register another user!', 'warning')
            else:
                role = 'user'
                if form.email.data == app.config['ADMIN_EMAIL']:
                    role = 'admin'
                new_user = User(name = form.name.data, email = form.email.data, password=generate_password_hash(form.password.data), role = role)
                db.session.add(new_user)
                db.session.commit()
                # login_user(new_user, remember=True)
                flash('The new user has been registered!', 'success')
                
                return redirect(url_for('main.index'))


    return render_template('auth/register.html', form=form, user=current_user)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()

    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            password = form.password.data

            user = User.query.filter_by(name=name).first()
            if user:
                if check_password_hash(user.password, password):
                    flash('Successfully logged in', 'success')
                    login_user(user, remember=True)
                    return redirect(url_for('main.index'))
            user = User.query.filter_by(email = name).first()
            if user:
                if check_password_hash(user.password, password):
                    flash('Successfully logged in', 'success')
                    login_user(user, remember=True)
                    return redirect(url_for('main.index'))
            else:
                flash('Invalid login data!', 'danger')

                
    if current_user:
        logout_user()
    return render_template('auth/login.html', form=form, user=current_user)
    

@auth.route('/password_change', methods=['GET', 'POST'])
def password_change():
    form = PasswordChange()
    user = current_user
    if request.method == "POST":
        if form .validate_on_submit():
            old_password = form.old_password.data
            if check_password_hash(user.password, old_password):
                user.password = generate_password_hash(form.password.data)
                db.session.commit()
                flash('Password has been changed', 'success')
                return redirect(url_for('main.index'))
            else:
                flash('Invalid password entered!', 'warning')
    
    return render_template('auth/password_change.html', form = form, user = current_user)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/delete_user/<int:id>')
@login_required
def delete_user(id):
    print(current_user.role)
    if current_user.role == 'admin':
        user = db.get_or_404(User, id)
        db.session.delete(user)
        db.session.commit()

        flash('The user has been deleted!ś', 'warning')
    return redirect(url_for('auth.user_list'))

@auth.route('/user_list')
@login_required
def user_list():
    if current_user.role == 'admin':
        # users = db.session.execute(select(User).order_by(User.role)).scalars()
        users = User.query.all()

        return render_template('auth/user_list.html', users = users, user = current_user)
    
    flash('You must be an administrator to view the user list!', 'warning')
    return redirect(url_for('main.index'))

@auth.route('/user_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def user_edit(id):
    form = UserEdit()
    user = current_user
    edited_user = db.get_or_404(User, id)

    if current_user.id == edited_user.id or current_user.role == 'admin':
        if request.method == 'POST':
            if form .validate_on_submit():
                edited_user.name = form.name.data
                edited_user.email = form.email.data
                if form.role.data != edited_user.role and user.role == 'admin':
                    edited_user.role = form.role.data
                elif form.role.data != edited_user.role:
                    flash('You do not have permission to change the user role!', 'warning')
                    return redirect(url_for('auth.user_edit', id=id))
                if form.password.data != 'supertajnehaslo':
                    edited_user.password = generate_password_hash(form.password.data)
                
                db.session.commit()
                flash('User data have been changed!', 'success')
                return redirect(url_for('auth.user_edit', id = id))
        
        form.id.data = id
        form.name.data = edited_user.name
        form.email.data = edited_user.email
        form.role.data = edited_user.role
        form.password.data = 'supertajnehaslo'
        form.password_2.data = 'supertajnehaslo'
        return render_template('auth/user_edit.html', user = current_user, form = form)
    
    flash('You do not have permission to change user data!', 'warning')
    return redirect(url_for('main.index'))