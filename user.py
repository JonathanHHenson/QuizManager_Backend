from datetime import datetime


class User:
    def __init__(self, user_id, permission, expiration):
        self._id = user_id
        self._permission = permission
        self._expiration = expiration
        self._last_active = datetime.now()

    def report_activity(self):
        self._last_active = datetime.now()

    def is_active(self):
        return datetime.now() - self._last_active < self._expiration

    def get_id(self):
        return self._id

    def get_permission(self):
        return self._permission

    def __hash__(self):
        return self._id.__hash__()

    def __eq__(self, other):
        return self._id.__eq__(other)
