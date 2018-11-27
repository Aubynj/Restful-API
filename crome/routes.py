from flask import request, redirect, url_for, jsonify, g
from crome import app, auth, db, bcrypt
from crome.models import Client, Credentials
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import secrets, json

@app.route("/", methods=['GET'])
def starter():
    return "<h1 style='text-align: center; margin-top: 100px'>RestFul Application</h1>"

# Connect application and get Authorization Code
@app.route('/authorization/connect', methods=['POST'])
@auth.login_required
def gain_authorization():

    if request.method == "POST":
        # Generate user authorization code
        if auth.username:
            # Authentication is successfully
            # Update user auth_code with authentication code
            auth_code = secrets.token_hex(16)
            g.user.auth_code = auth_code
            db.session.commit()
            
            return jsonify({"Authorization Code":f"{g.user.auth_code}"})
        else:
            return jsonify({"message":"Authorization Failed"})
    else:
        return jsonify({"message":"Bad Request"})
        


# Gain authentication token and refresh token
@app.route('/authorization/token', methods=['GET','POST'])
def gain_credentials():
    if request.method == "GET":
        # grant_type = authorization_code & code = auth_code
        # Check if user is authorize
        grant_type = request.args['grant']
        code = request.args['code']
        
        auth = Client.query.filter_by(auth_code=code).first()
        if auth and grant_type == "authorization_code":
            token = Serializer(app.config['SECRET_KEY'], expires_in=3600)
            access_token = token.dumps({'id':auth.id}).decode('ascii')
            refresh_token = secrets.token_hex(16)
            crend = Credentials(access_token=access_token, refresh_token=refresh_token, client_id=auth.id)

            # Save credentials in db
            db.session.add(crend)
            db.session.commit()
            
            return jsonify({
                'access_token' : access_token,
                'refresh_token' : refresh_token,
                'type' : 'bearer',
                'expires_in' : 3600
            })

        else:
            return jsonify({"message":"Invalid Authorization Code"})
    else:
        return jsonify({"message":"Bad Request"}), 405

# Refreshing token when expired
@app.route('/token/refresh', methods=['POST'])
@auth.login_required
def refresh_access_token():

    if request.method == "POST":
        try:
            grant_type = request.form['grant']
            refresh_token = request.form['refresh_token']

            clint = Credentials.query.filter_by(refresh_token=refresh_token).first()

            # Check if everything is good
            if clint and clint.client_id == g.user.id: #Client_id is equal to authentication username id
                token = Serializer(app.config['SECRET_KEY'], expires_in=3600)
                access_token = token.dumps({'id':g.user.id}).decode('ascii')
                refresh_token = secrets.token_hex(16)

                # Updating client informations
                clint.access_token = access_token
                clint.refresh_token = refresh_token
                db.session.commit()

                return jsonify({
                    'access_token' : access_token,
                    'refresh_token' : refresh_token,
                    'type' : 'bearer',
                    'expires_in' : 3600
                })

            else:
                return jsonify({"message":"Invalid refresh token"}), 405

        except KeyError:
            return jsonify({"message":"Invalid KeyError"}), 400
    else:
        return jsonify({"message":"Bad Request"}), 405

# Fetching all users
@app.route('/api/users', methods=['GET'])
def getUsers():
    if request.method == "GET":
        try:
            autho_header = request.headers['Authorization']
            api_key = autho_header.split(" ")
            se = Serializer(app.config['SECRET_KEY'])
            if api_key[0] != "Bearer":
                return jsonify({"message":"Authorization type required"}), 2005
            else:
                try:
                    data = se.loads(api_key[1])
                except SignatureExpired:
                    return jsonify({"message":"Access token expired"}), 5000
                except BadSignature:
                    return jsonify({"message":"Invalid Access token"}), 4000
                user = Client.query.get(data['id'])
                d = {
                    'username' : user.username,
                    'secret' : user.secret
                }
                return jsonify(d), 200
        except:
            return jsonify({"message":"API Authorization Failed"})            
        


# Creating a new client
@app.route('/client/create', methods=['POST'])
def createClient():
    if request.method == "POST":
        try:
            client_username = request.form['client_user']
            client_secret = request.form['client_password']

            hash_pass = bcrypt.generate_password_hash(client_secret).decode('utf-8')
            # Check if client id exist
            client_xt = client_exist(client_username)
            if client_xt:
                return jsonify({"message":f"{client_username} already exist"})
            else:
                # Add information to db
                newClient = Client(username=client_username, secret=hash_pass)
                db.session.add(newClient)
                db.session.commit()
                return jsonify({"message":"Account created successfully"}), 201
        except:
            return jsonify({'message': 'Invalid Data objects'}), 403
    else:
        return jsonify({"message":"Bad Request"}), 405

def client_exist(client_username):
    client = Client.query.filter_by(username=client_username).first()
    if client:
        return True
    else:
        return False

@auth.error_handler
def auth_error():
    return jsonify({"message":"Authorization Failed"})