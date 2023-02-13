from flask import jsonify, request, g

from app import db
from app.auth.models import Users
from app.comments import comments_bp
from app.comments.models import Comments
from app.decorators.decorators import token_required
from app.posts.models import Posts


@comments_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    post = Posts.query.get(post_id)
    comments = (db.session.query(Comments, Users.username)
                .join(Users, Comments.user_id == Users.id)
                .filter(Comments.post_id == post_id)
                .order_by(Comments.id.desc())
                .all())
    if len(comments) == 0:
        return jsonify({"message": "No yet commented on"})
    return jsonify([{**comment.to_dict(), 'username': username} for comment, username in comments])


@comments_bp.route('/posts/<int:post_id>/comments', methods=['GET', 'POST'])
@token_required
def create_comment(post_id):
    #obtenemos la id del usuario
    user_id= g.current_user.id
    #obtenemos los datos en Json
    data = request.get_json()
    #obtenemos el post por su id
    post = Posts.query.get(post_id)
    #seleccionamos el campo de comentario que se va a enviar datos
    if not data['content']:
        return jsonify({'error': 'The content field cannot be empty'})
    comment = Comments(content=data['content'], post=post, user_id=user_id)
    #guardamos
    try:
        db.session.add(comment)
        db.session.commit()
    except:
        return jsonify({'error': 'The comment was not able to be created'})
    #mostramos
    return jsonify({'comment': comment.to_dict()}), 201



@comments_bp.route('/comments/<int:comment_id>', methods=['GET'])
@token_required
def view_comment(comment_id):
    comment = Comments.query.filter_by(id=comment_id).first()
    return jsonify([comment.to_dict()])


@comments_bp.route('/comments/<int:comment_id>', methods=['PUT'])
@token_required
def edit_comment(comment_id):
    data = request.get_json()
    comment = Comments.query.filter_by(id=comment_id).first()
    if g.current_user.id != comment.user_id:
        return  jsonify({"message": "Unauthorized"}), 401
    comment.content = data['content']
    db.session.commit()
    return jsonify(comment.to_dict())


@comments_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@token_required
def delete_comment(comment_id):
    comment = Comments.query.get(comment_id)
    if g.current_user.id != comment.user_id:
        return jsonify({"message": "Unauthorized"}), 401
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "comment deleted successfully"})