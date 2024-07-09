# admin_view.py
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, abort

class AdminModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_admin:
            return True
        else:
            abort(403)  # Forbidden access

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))


