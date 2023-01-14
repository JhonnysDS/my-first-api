from flask import Blueprint

comments_bp = Blueprint('comments', __name__, template_folder='templates')

from . import routes