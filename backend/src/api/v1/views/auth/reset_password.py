from flask import request, jsonify
from flask_mail import Message

import datetime
from os import getenv
from typing import Dict

from api.v1.views import app_views
from api.v1.models.user import User
from api.v1.utils.database import db
from api.v1.views.auth.decorator import authorize


SECRET_KEY = getenv('SECRET_KEY')


@app_views.post('/forgot-password', strict_slashes=False)
def verify_email():
    """Send an email containing authentication information to the user"""
    from api.v1.app import mail

    exp: datetime.Time = datetime.datetime.now() + datetime.timedelta(minutes=15)
    try:
        email: str = response.get_json()['email']
        user: User = dbClient.filter_by(email=email)
        token: str = jwt.encode({'email': user.email, 'exp': 'exp'}, SECRET_KEY, algorithm='HS256')
        verif_mail: Message = Message()
        verif_mail.subject = 'Password Reset Requested'
        verif_mail.sender = getenv('MAIL_USERNAME')
        verif_mail.recipients = [user.email]
        verif_mail.html = render_template('reset_password.html', user=user, token=token)
        mail.send(verif_mail)
        return jsonify({'message': 'Password reset token sent!'}), 200
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON'}), 400
    except KeyError:
        return jsonify({'error': 'Missing email'}), 400
    except AttributeError:
        return jsonify({'error': 'user does not exist'}), 400
    except Exception as e:
        return jsonify({'error': e}), 500


@app_views.post('/reset_password', strict_slashes=False)
@authorize
def reset_email(email):
    """Reset the user's email"""
    try:

        user = db.session.query(User).filter_by(email=email).first()
        password: str = request.get_json()['password']
        user.password = generate_password_hash(password)
        user.save()
        return jsonify({'message': 'password changed successfully'}), 200
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid json'}), 400
    except KeyError:
        return jsonify({'error': 'Missing password'}), 400
