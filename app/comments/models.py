#definimos el modelo de la tabla Comments de la base de datos
from sqlalchemy.orm import relationship

from app import db


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    post = db.relationship('Posts', backref=db.backref('comments', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    users = relationship("Users", back_populates="comments")

#la manera en la que queremos mostrar el json
    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'content': self.content
        }