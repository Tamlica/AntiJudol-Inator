import jwt

from functools import wraps
from flask import request, jsonify, redirect, url_for, session, flash

from app.models import User
from app.config import Config

def decode_jwt_token():
    token = session.get('token')
    if not token:
        return None
    try:
        decoded_token = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        flash('Token expired. Please log in again.')
        return None
    except jwt.InvalidTokenError:
        flash('Invalid token. Please log in again.')
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        decoded_token = decode_jwt_token()
        if not decoded_token:
            return redirect(url_for('auth.login'))
        
        current_user_id = decoded_token.get('sub') 
        current_user = User.query.get(current_user_id)
        
        if not current_user:
            return redirect(url_for('auth.login'))
        
        return f(current_user, *args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.role != 'admin':
            flash('Admin access required.')
            return redirect(url_for('auth.login'))
        return f(current_user, *args, **kwargs)
    return decorated

def streamer_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.role != 'streamer':
            flash('Streamer access required.')
            return redirect(url_for('auth.login'))
        return f(current_user, *args, **kwargs)
    return decorated
