from datetime import datetime, timedelta

import jwt
from flask import request, jsonify

from app import db
from app.auth import auth_bp
from app.auth.models import Users
from entrypoint import app


@auth_bp.route('/register', methods=['POST'])
def register():
    data=request.get_json()
    try:
        #Creamos el nuevo usuario
        user = Users(username=data['username'],
                     email=data['email'],
                     password=data['password'])

        #añadimos seguridad a la contraseña
        user.set_password(user.password)

        #Agregamos el usuario a la base de datos
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201
    except Exception:
        return jsonify({'message': 'Error creating user'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        # Try to find the user in the database
        user = Users.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            # If the user exists and the password is correct, generate a JWT token
            token = jwt.encode(
                {'id': user.id,
                 'username': user.username,
                 'exp': datetime.utcnow() +
                        timedelta(days=1),
                 "isLogged":True },
                app.config['SECRET_KEY'], algorithm='HS256')
            print(token)
            # Return the token to the client
            return jsonify({'token': token}), 200
        else:
            # If the user doesn't exist or the password is incorrect, return an error
            return jsonify({'message': 'Invalid username or password'}), 401
    except Exception as e:
        return jsonify({'message': 'Error logging in: {}'.format(str(e))}), 500