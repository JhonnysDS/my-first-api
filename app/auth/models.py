from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from app import db



class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255), nullable=True)  # nuevo campo para el avatar
    comments = relationship("Comments", back_populates="users")
    def __init__(self, username, email, password, avatar):
        self.username = username
        self.email = email
        self.password = password
        self.avatar = avatar

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return  check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'avatar': self.avatar,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    @staticmethod
    def get_by_id(id):
        return Users.query.get(id)


