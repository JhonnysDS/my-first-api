import jwt

from app import db

from app.decorators.decorators import token_required
from app.posts import posts_bp
from flask import request, jsonify, g

from app.posts.models import Posts
from app.comments.models import Comments


@posts_bp.route('/posts', methods=['GET'])
@token_required
def get_posts():

    # llamamos todos los registros de la tabla posts y los invertimos para que el último sea el primero
    posts = Posts.query.order_by(Posts.id.desc()).all()

    # los mostramos
    return jsonify([post.to_dict() for post in posts])



@posts_bp.route('/posts/<int:post_id>', methods=['GET'])
@token_required
def get_post(post_id):
    #Obtenemos un registro de la tabla posts por su id.
    post = Posts.query.get(post_id)
    #condicional que verifica si existe o no
    if post is None:
        #mostramos el mensaje de que no existe
        return jsonify({'error': 'Post not found'})
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
        for post_data in data:
            if not post_data['title'] or not post_data['content']:
                return jsonify({'message': 'Title and content are required'})
            post = Posts.query.filter_by(title=post_data['title'], content=post_data['content']).first()
            if Posts.query.filter_by(title=post_data['title']).first():
                return jsonify({'message': f'This post already exists'})
            try:
                post = Posts(title=post_data['title'],
                             content=post_data['content'],
                             user_id=user_id)
                db.session.add(post)
            except Exception:
                db.session.rollback()
                return jsonify({'Message': 'could not create a post'}), 500
        db.session.commit()
        return jsonify({'message': 'Posts created successfully'}), 201





@posts_bp.route('/posts/<int:post_id>', methods=['PUT'])
@token_required
def update_post(post_id):
    #Obtenemos el json de los datos del post
    data = request.get_json()
    try:
        #obtenemos el post por su id
        post = Posts.query.get(post_id)

        # Comprueba si el usuario actualmente autenticado es el mismo que creó el post
        if post.user_id != g.current_user.id:
            return jsonify({"Message": "No tienes permiso para actualizar este post"}), 401

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
    post = Posts.query.get(post_id)

    # Comprueba si el usuario actualmente autenticado es el mismo que creó el post
    if post.user_id != g.current_user.id:
        return jsonify({"Message": "No tienes permiso para eliminar este post"}), 401

    # Eliminar todos los comentarios relacionados con ese post
    Comments.query.filter_by(post_id=post.id).delete()

    # Eliminar el post
    db.session.delete(post)
    db.session.commit()
    return jsonify({"Message": "Post y sus comentarios relacionados eliminados con éxito"})

