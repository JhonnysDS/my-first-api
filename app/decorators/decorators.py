from functools import wraps
from flask import request, g
import jwt


from app.auth.models import Users


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if token:
            token = token.split(" ")[1]

        if not token:
            return ({
                        "isLogged": False,
                        "messages": "Acceso no autorizado."
                    }, 401)

        from entrypoint import app
        dataAuthToken = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        currentUser = Users.get_by_id(dataAuthToken['id'])

        if currentUser is None:
            return ({
                        "isLogged": False,
                        "messages": "Acceso no autorizado."
                    }, 401)

        g.current_user = currentUser
        return f(*args, **kwargs)

    return decorated
