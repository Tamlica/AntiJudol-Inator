import datetime

from flask_jwt_extended import create_access_token
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session

from app import db
from app.models import User
from app.utils.jwt import token_required, admin_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
@token_required
def index(current_user):
    if current_user.role == 'admin':
        return redirect(url_for('auth.register_streamer'))
    elif current_user.role == 'streamer':
        return redirect(url_for('main.manage_words'))
    else:
        flash("Unknown role. Please contact admin.")
        return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            
            access_token = create_access_token(identity=user.id)
            # access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(days=3))

            session['token'] = access_token
            print(session)
            
            if user.role == 'admin':
                return redirect(url_for('auth.register_streamer'))
            elif user.role == 'streamer':
                return redirect(url_for('main.manage_words'))
            else:
                flash("Unknown role. Please contact admin.")
                return redirect(url_for('auth.login'))
        else:
            flash('Invalid credentials, please try again.')
            return redirect(url_for('auth.login'))
    
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
@token_required
@admin_required
def register_streamer(current_user):
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('Username or Email already exists.')
            return redirect(url_for('auth.register_streamer'))
        
        new_streamer = User(
            name=name,
            username=username,
            email=email,
            role='streamer'
        )
        new_streamer.set_password(password)
        db.session.add(new_streamer)
        db.session.commit()
        
        flash('Streamer registered successfully.')
        return redirect(url_for('auth.register_streamer'))
    
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))