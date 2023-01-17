import jwt

from app import db

from app.decorators.decorators import token_required
from app.posts import posts_bp
from flask import request, jsonify

from app.posts.models import Posts


@posts_bp.route('/posts', methods=['GET'])
@token_required
def get_posts():

    #llamamos todos los registros de la tabla posts
    posts = Posts.query.all()
    #los mostramos
    return jsonify([post.to_dict() for post in posts])


@posts_bp.route('/posts/<int:post_id>', methods=['GET'])
@token_required
def get_post(post_id):
    #Obtenemos un registro de la tabla posts por su id.
    post = Posts.query.get(post_id)
    #condicional que verifica si existe o no
    if post is None:
        #mostramos el mensaje de que no existe
        return jsonify({'error': 'Post not found'}), 404
    return jsonify(post.to_dict())


@posts_bp.route('/create-posts', methods=['GET', 'POST'])
@token_required
def create_post():
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']

        if token:
            token = token.split(" ")[1]

        from entrypoint import app
        dataAuthToken = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        user_id = dataAuthToken['id']
        data = request.get_json()
        try:
            post = Posts(title=data['title'],
                         content=data['content'],
                         user_id=user_id)
            db.session.add(post)
            db.session.commit()
            return jsonify(post.to_dict()), 201
        except Exception:
            return jsonify({'Message': 'could not create a post'}), 500


@posts_bp.route('/posts/<int:post_id>', methods=['PUT'])
@token_required
def update_post(post_id):
    #Obtenemos el json de los datos del post
    data = request.get_json()
    try:
        #obtenemos el post por su id
        post = Posts.query.get(post_id)
        #estos son los campos que se modifican
        post.title = data['title']
        post.content = data['content']
        #guardamos los cambios
        db.session.commit()
        return jsonify({'post': post.to_dict()})
    except Exception:
        return jsonify({'Message': 'could update a post'}), 500


@posts_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@token_required
def delete_post(post_id):
    #Obtenemos el json de los datos del post
    data = request.get_json()
    post = Posts.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"Message": "post deleted successfully"})