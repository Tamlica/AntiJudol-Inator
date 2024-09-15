from flask_jwt_extended import get_jwt_identity
from flask import Blueprint, render_template, request, redirect, url_for, flash

from app import db, socketio
from app.models import User, BadWord, GoodWord
from app.utils.cleaning_message import clean_text
from app.utils.jwt import token_required, streamer_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/manage_words', methods=['GET', 'POST'])
@token_required
@streamer_required
def manage_words(current_user):
    if request.method == 'POST':
        # Update clean option and fixed words
        clean_option = request.form.get('clean_option')
        fixed_supporter = request.form.get('fixed_supporter')
        fixed_message = request.form.get('fixed_message')
        
        current_user.clean_option = clean_option
        current_user.fixed_supporter_word = fixed_supporter
        current_user.fixed_message_word = fixed_message
        
        db.session.commit()
        flash('Filter option and fixed words updated successfully.')
        return redirect(url_for('main.manage_words'))
    
    return render_template('manage_words.html', user=current_user)

@main_bp.route('/add_bad_word', methods=['POST'])
@token_required
@streamer_required
def add_bad_word(current_user):
    word = request.form.get('bad_word')
    if word:
        new_bad_word = BadWord(word=word, user_id=current_user.id)
        db.session.add(new_bad_word)
        db.session.commit()
        flash('Bad word added successfully.')
    else:
        flash('No word entered.')
    return redirect(url_for('main.manage_words'))

@main_bp.route('/add_good_word', methods=['POST'])
@token_required
@streamer_required
def add_good_word(current_user):
    word = request.form.get('good_word')
    if word:
        new_good_word = GoodWord(word=word, user_id=current_user.id)
        db.session.add(new_good_word)
        db.session.commit()
        flash('Good word added successfully.')
    else:
        flash('No word entered.')
    return redirect(url_for('main.manage_words'))

@main_bp.route('/delete_bad_word/<int:word_id>', methods=['POST'])
@token_required
@streamer_required
def delete_bad_word(current_user, word_id):
    bad_word = BadWord.query.get_or_404(word_id)
    if bad_word.user_id != current_user.id:
        flash('Unauthorized action.')
        return redirect(url_for('main.manage_words'))
    db.session.delete(bad_word)
    db.session.commit()
    flash('Bad word deleted successfully.')
    return redirect(url_for('main.manage_words'))

@main_bp.route('/delete_good_word/<int:word_id>', methods=['POST'])
@token_required
@streamer_required
def delete_good_word(current_user, word_id):
    good_word = GoodWord.query.get_or_404(word_id)
    if good_word.user_id != current_user.id:
        flash('Unauthorized action.')
        return redirect(url_for('main.manage_words'))
    db.session.delete(good_word)
    db.session.commit()
    flash('Good word deleted successfully.')
    return redirect(url_for('main.manage_words'))


@main_bp.route('/webhook/<user_id>', methods=['POST'])
def webhook(user_id):
    current_user = User.query.get_or_404(user_id)
    
    data = request.json
    print("Received data:", data)
    
    if 'message' in data:
        amount = data['amount']
        original_message = data['message']
        original_supporter = data['supporter']
        
        cleaned_message = clean_text(message=original_message, user=current_user)
        cleaned_supporter = clean_text(supporter=original_supporter, user=current_user)

        show_alert_id = f"show_alert_{user_id}"
        
        socketio.emit(show_alert_id, {'amount': amount, 'supporter': cleaned_supporter, 'message': cleaned_message})
        
        return {'status': 'success', 'cleaned_message': cleaned_message}, 200
    
    return {'status': 'failed', 'reason': 'No message found'}, 400

@main_bp.route('/alert/<user_id>')
def alert(user_id):
    return render_template('index.html')