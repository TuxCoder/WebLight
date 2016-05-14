from wtforms.fields import PasswordField, StringField
from wtforms.widgets import PasswordInput

from ..admin_base import SecureModelView
from ..extensions import admin_models
from ..models.auth import  User


class UserAdminView(SecureModelView):

    column_list = ('login_name', 'role', 'contest', 'active')
    column_searchable_list = ['login_name']
    form_excluded_columns = ['last_login', 'password_hash', 'posts',
                             'challenges_solutions', 'challenges_attempts']
    form_overrides = {
        'login_name': StringField,
    }
    form_extra_fields = {
        'new_password': PasswordField(widget=PasswordInput())
    }
    can_view_details = True
    # column_editable_list = ['active', 'role', 'contest']

    def on_model_change(self, form, model, is_created):
        if model.new_password:
            set_pwd = model.new_password
            del model.new_password
            model.password = set_pwd


class RoleAdminView(SecureModelView):

    form_overrides = {
        'role_name': StringField
    }


admin_models.append([User, UserAdminView])
