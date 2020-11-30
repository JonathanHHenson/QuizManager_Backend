from datetime import timedelta
from timeloop import Timeloop
import traceback
from uuid import uuid4
from user import User
from flask import request, abort, g
import functools

USER_SESSION_EXPIRATION = timedelta(hours=1)
active_user_sessions = dict()


def get_session_id():
    if 'session_id' not in g:
        g.session_id = request.cookies.get('session_id')
    return g.session_id


def get_user_session(session_id):
    if not is_user_session_valid(session_id):
        return None
    return active_user_sessions[session_id]


def new_user_session(username, permission):
    session_user = User(username, permission, USER_SESSION_EXPIRATION)
    session_id = uuid4().hex
    active_user_sessions[session_id] = session_user
    return session_id


def is_user_session_valid(session_id):
    if session_id in active_user_sessions:
        if active_user_sessions[session_id].is_active():
            return True
        else:
            del active_user_sessions[session_id]
            print('deleted', session_id)
    return False


def delete_user_session(session_id):
    if session_id in active_user_sessions:
        del active_user_sessions[session_id]


def clean_sessions():
    for sess_id, _ in list(active_user_sessions.items()):
        is_user_session_valid(sess_id)


def require_login(_func=None, *, permissions=[], get_permission=False):
    def decorator_require_login(func):
        @functools.wraps(func)
        def wrapper_require_login(*args, **kwargs):
            user = get_user_session(get_session_id())
            if not user:
                return abort(401)
            user_permission = user.get_permission()
            authorized_perms = [p.lower() for p in permissions]
            if user and (not permissions or user_permission in authorized_perms):
                if get_permission:
                    kwargs['permission'] = user_permission
                return func(*args, **kwargs)
            else:
                return abort(401)
        return wrapper_require_login

    if _func:
        return decorator_require_login(_func)
    else:
        return decorator_require_login


def report_activity(func):
    @functools.wraps(func)
    def wrapper_report_activity(*args, **kwargs):
        user = get_user_session(get_session_id())
        user.report_activity()
        return func(*args, **kwargs)
    return wrapper_report_activity


def start_cleaning(period):
    _t1 = Timeloop()

    @_t1.job(interval=period)
    def clean_user_sessions():
        try:
            clean_sessions()
        except:
            traceback.print_tb()

    _t1.start(block=False)


