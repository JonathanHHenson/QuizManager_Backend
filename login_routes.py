import models
from flask import Blueprint, jsonify, request, abort, make_response
import sqlalchemy as sa
import user_session_manager

login_routes = Blueprint('login_routes', __name__, template_folder='templates')


def encrypt_password(password):
    results = models.db.session.execute(sa.text('SELECT encryptPassword(:param)'), dict(param=password)).fetchone()
    if results:
        return results[0]
    else:
        return None


@login_routes.route('/_apis/login', methods=['POST'])
def login():
    body = request.get_json()
    user = models.Authentication.query.filter_by(username=body['username']).first()
    if not user:
        return abort(401)

    body_password_encrypted = encrypt_password(body['password'])
    if body_password_encrypted != user.password:
        return abort(401)

    permission = models.Permission.query.get(user.permission_id)

    username = user.username
    session_id = user_session_manager.new_user_session(username, permission.label)

    response = make_response(jsonify(dict(username=username, permission=permission.label.lower(), success=True)))
    response.set_cookie('session_id', session_id)
    return response


@login_routes.route('/_apis/isLoggedIn', methods=['POST'])
def is_logged_in():
    current_session = request.cookies.get('session_id')

    user = user_session_manager.get_user_session(current_session)
    if not user:
        return abort(401)
    permission = user.get_permission()

    user.report_activity()
    return jsonify(dict(username=user.get_id(), permission=permission.lower(), success=True))


@login_routes.route('/_apis/logout', methods=['POST'])
def logout():
    current_session = request.cookies.get('session_id')
    user_session_manager.delete_user_session(current_session)
    return jsonify(dict(success=True))

