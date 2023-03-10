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
        #buscamos en la base de datos el correo y el nombre de usuarip para validar si existen
        existing_username = Users.query.filter_by(username=data['username']).first()
        existing_email = Users.query.filter_by(email=data['email']).first()

        # verificamos si el correo o el username existe
        if existing_username and existing_email:
            return jsonify({'message': 'sorry, the email and the username already exist'})

        #verificamos si el correo existe
        if existing_email:
            return jsonify({"message":"sorry, the email already exist"})

        #Verificamos si el nombre de usuario existe
        if existing_username:
            return jsonify({'message':'sorry, the username already exist'})

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
        return jsonify({'message': 'Error creating user'}), 200


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
            # Return the token to the client
            return jsonify({'token': token, 'user_id': user.id}), 200
        else:
            # If the user doesn't exist or the password is incorrect, return an error
            return jsonify({'message': 'Invalid username or password'})
    except Exception as e:
        return jsonify({'message': 'Error logging in: {}'.format(str(e))}), 500


@auth_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = Users.query.filter_by(id=user_id).first()
    if user is not None:
        return jsonify({'id': user.id,''
                                      'username': user.username}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@auth_bp.route('/users', methods=['GET'])
def get_all_users():
    users = Users.query.all()
    if not users:
        return jsonify({'message': 'No users found'}), 404
    user_list = []
    for user in users:
        user_list.append({'id': user.id, 'username': user.username})
    return jsonify(user_list)