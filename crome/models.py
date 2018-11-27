from crome import db, auth, bcrypt
from flask import g, jsonify

@auth.verify_password
def verify_password(username, secret):
    user = Client.query.filter_by(username = username).first()
    if user and bcrypt.check_password_hash(user.secret, secret):
        g.user = user
        return True
    else:
        print("Authorization Failed")
        return False

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    secret = db.Column(db.String(255), nullable=False)
    auth_code = db.Column(db.String(50), default=None)
            

class Credentials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(255), nullable=False)
    refresh_token = db.Column(db.String(50), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)