import base64
import json
import os
import re
from datetime import datetime, timedelta
import jwt
from flask import request, jsonify, current_app, g, Response
from app import db
from app.auth import auth_bp
from app.auth.models import Users
from app.decorators.decorators import token_required
from entrypoint import app
import demjson


file_dir = current_app.config['USER_IMAGES_DIR']
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@auth_bp.route("/register", methods=["POST", "GET"])
def register():
    try:
        # Obtenemos el objeto json que viene desde el frontend
        if request.data:
            userDatas = json.loads(request.data)

            # Declaramos las variables necesarias para actualizar la información
            username = userDatas['username']
            email = userDatas['email']
            password = userDatas['password']
            avatar = userDatas['avatar']

            existing_username = Users.query.filter_by(username=userDatas['username']).first()
            existing_email = Users.query.filter_by(email=userDatas['email']).first()
            if existing_username is not None:
                return jsonify({
                    "messages": "this user already exist"
                }, 400)
            else:
                photo = avatar
                photoAppended = {}
                if photo:
                    os.makedirs(file_dir, exist_ok=True)
                    result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", photo['imagePath'], re.DOTALL)

                    if result:
                        image_full_name = photo['imagenFullName']
                        image_name = photo['imageName']
                        image_ext = photo['imageExt']
                        image_size = photo['imageSize']

                        #se le contatena al nombre del archivo una fecha con tiempo
                        dateNow = datetime.now()
                        image_path = image_name + '-' + dateNow.strftime('%Y%m%d%H%M%S')

                        os.makedirs(file_dir, exist_ok=True)
                        photo_path = os.path.join(file_dir, (image_path + image_ext))

                        #creación de un groupdict
                        data = result.groupdict().get("data")

                        #bases64 decodificación
                        img = base64.urlsafe_b64decode(data)

                        with open(photo_path, "wb") as f:
                            f.write(img)

                        photoAppended = {
                            'imagenFullName': image_full_name,
                            'imageName': image_name,
                            'imageExt': image_ext,
                            'imageSize': image_size,
                            'imagePath': image_path,
                            'imageServer': 'true'
                        }


                user = Users(
                    username=username,
                    email=email,
                    avatar=photoAppended,
                    password=password,
                )

                # añadimos seguridad a la contraseña
                user.set_password(user.password)

                # Agregamos el usuario a la base de datos
                db.session.add(user)
                db.session.commit()
                return jsonify({
                    "messages": "Usuario registrado con exito"
                }, 200)

        return jsonify({
            "messages": "El usuario no pudo ser guardado."
        }, 400)
    except Exception as e:
        return jsonify({
            "messages": "Error al guardar Usuario.",
            "error": str(e)
        }, 500)

@auth_bp.route("/update/user/<int:user_id>", methods=["PUT"])
def updateUser(user_id):
    data = request.get_json()
    user = Users.query.filter_by(id=user_id).first()

    # Validar si el nombre de usuario ya existe
    if data.get('username'):
        existing_user = Users.query.filter(Users.username == data['username']).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({'message': 'This username already exist, please write other.'})
        user.username = data['username']

    # Validar si el correo electrónico ya existe
    if data.get('email'):
        existing_user = Users.query.filter(Users.email == data['email']).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({'message': 'This email already exist, please write other.'})
        user.email = data['email']


    if data.get('avatar') is not None:
        if user.avatar:
            delete_file(user_id)
        user.avatar = data['avatar']
        photo = user.avatar
        photoAppended = {}
        if photo:

            os.makedirs(file_dir, exist_ok=True)
            result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", photo['imagePath'], re.DOTALL)

            if result:
                image_full_name = photo['imagenFullName']
                image_name = photo['imageName']
                image_ext = photo['imageExt']
                image_size = photo['imageSize']

                # se le contatena al nombre del archivo una fecha con tiempo
                dateNow = datetime.now()
                image_path = image_name + '-' + dateNow.strftime('%Y%m%d%H%M%S')

                os.makedirs(file_dir, exist_ok=True)
                photo_path = os.path.join(file_dir, (image_path + image_ext))

                # creación de un groupdict
                data = result.groupdict().get("data")

                # bases64 decodificación
                img = base64.urlsafe_b64decode(data)

                with open(photo_path, "wb") as f:
                    f.write(img)

                photoAppended = {
                    'imagenFullName': image_full_name,
                    'imageName': image_name,
                    'imageExt': image_ext,
                    'imageSize': image_size,
                    'imagePath': image_path,
                    'imageServer': 'true'
                }

                user.avatar = photoAppended

    db.session.commit()
    return jsonify({'message': 'user updated successfully'})




@auth_bp.route('/deletefile/<int:user_id>', methods=['DELETE'])
def delete_file(user_id):
    user = Users.query.filter_by(id=user_id).first()
    avatar_dict = json.loads(user.avatar.replace("'", "\""))
    file_path = os.path.join(file_dir, avatar_dict["imagePath"] + avatar_dict["imageExt"])
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'message': 'Archivo eliminado con éxito'})
    else:
        return jsonify({'message': 'El archivo no existe'})


@auth_bp.route("/change/password/<int:user_id>", methods=["PUT"])
def change_password(user_id):
    user = Users.query.filter_by(id=user_id).first()
    data = request.get_json()

    if not user:
        return jsonify({'message':'User not found'})

    #Obtenemos la contraseña antigua y la nueva contraseña.
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    #verificamos que la contraseña antigua sea la correcta.
    if not user.check_password(old_password):
        return jsonify({'message':'The old password is incorrect'})

    #actualizar la contraseña del usuario.
    user.set_password(new_password)
    db.session.commit()

    return jsonify(
        {'message':'Password changed successfully'})




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
            return jsonify({'token': token}), 200
        else:
            # If the user doesn't exist or the password is incorrect, return an error
            return jsonify({'message': 'Invalid username or password'})
    except Exception as e:
        return jsonify({'message': 'Error logging in: {}'.format(str(e))}), 500


@auth_bp.route('/user/<int:user_id>', methods=['GET'])
@token_required
def get_user_by_id(user_id):
    user = Users.query.filter_by(id=user_id).first()
    if user is not None:
        return jsonify({'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'avatar': user.avatar}), 200
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