from functools import wraps
from flask import current_app, make_response, request, render_template

def authentication_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == current_app.config["USER"] and auth.password == current_app.config["USER_PASSWORD"]:
            return f(*args, **kwargs)
        return make_response(render_template('denied.html'), 401, {'WWW-Authenticate': 'Basic realm="LOGIN REQUIRED"'})
    
    return decorated