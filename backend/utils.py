from functools import wraps
from flask import make_response, request, render_template

def authentication_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == "admin1" and auth.password == "pass":
            return f(*args, **kwargs)
        return make_response(render_template('access_denied.html'), 401, {'WWW-Authenticate': 'Basic realm="LOGIN REQUIRED"'})
    
    return decorated