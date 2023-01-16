from datetime import datetime
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
        try:
            dataAuthToken = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"],verify=verify_expiration)
        except jwt.ExpiredSignatureError:
            return({
                        "isLogged": False,
                        "messages": "Token expirado."
                    }, 401)
        currentUser = Users.get_by_id(dataAuthToken['id'])

        if currentUser is None:
            return ({
                        "isLogged": False,
                        "messages": "Acceso no autorizado."
                    }, 401)

        g.current_user = currentUser
        return f(*args, **kwargs)

    return decorated




def verify_expiration(payload):
    """
    Function to verify the expiration time of the token. It receives the payload of the token and returns a boolean
    indicating whether the token has expired or not.
    """
    now = datetime.utcnow()
    exp = datetime.fromtimestamp(payload['exp'])
    if now > exp:
        return False
    return True

