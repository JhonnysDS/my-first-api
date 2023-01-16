from flask import jsonify, request, g

from app import db
from app.comments import comments_bp
from app.comments.models import Comments
from app.decorators.decorators import token_required
from app.posts.models import Posts


@comments_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    post = Posts.query.get(post_id)
    comments = post.comments
    if len(comments) == 0:
        return  jsonify({"Message": "No yet commented on"})
    return jsonify([comment.to_dict() for comment in comments])


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
    comment = Comments(content=data['content'], post=post, user_id=user_id)
    #guardamos
    db.session.add(comment)
    db.session.commit()
    #mostramos
    return jsonify({'comment': comment.to_dict()}), 201

@comments_bp.route('/comments/<int:comment_id>', methods=['PUT'])
def edit_comment(comment_id):
    data = request.get_json()
    comment = Comments.query.filter_by(id=comment_id).first()
    comment.content = data['content']
    db.session.commit()
    return jsonify({'content': comment.to_dict()})


@comments_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = Comments.query.get(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "comment deleted successfully"})