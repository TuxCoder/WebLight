from flask import request,  redirect, url_for
from flask.ext.admin import BaseView
from flask.ext.login import current_user
from flask.ext.admin.contrib.sqla import ModelView


class SecureView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_administrator()


class SecureModelView(ModelView):
    list_template = 'admin/list.html'
    create_template = 'admin/create.html'
    edit_template = 'admin/edit.html'
    # form_base_class = SecureForm  # CSRF Protection
    page_size = 50

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_administrator()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))

    # Override this function from flask-admin to disable the debug view for
    # exceptions. Print a flash message instead.
    def handle_view_exception(self, exc):
        return False
