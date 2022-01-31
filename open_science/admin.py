from flask_admin.contrib import sqla
from flask_login import current_user
from flask_admin import expose
import flask_admin as admin
from flask import redirect, url_for


class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('login_page'))
        elif current_user.privileges_set != current_user.user_types_enum.ADMIN.value:
            return redirect(url_for('home_page'))
        return super(MyAdminIndexView, self).index()


class MyModelView(sqla.ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.privileges_set == current_user.user_types_enum.ADMIN.value


class UserView(MyModelView):
    can_create = True
    can_edit = True
    can_delete = False
    column_sortable_list = ['id', 'registered_on',
                            'confirmed', 'remarks', 'force_hide', 
                            ('first_name', 'second_name')]

    column_searchable_list = ['id', 'first_name', 'second_name', 'email']

    list_columns = ['id', 'first_name', 'second_name', 'email', 
                    'privileges_set', 'registered_on', 'confirmed',
                    'force_hide', 'remarks']
                    
    column_exclude_list = ['password_hash', 'confirmed_on',
                           'review_mails_limit', 'notifications_frequency',
                           'new_email', 'has_photo']


class MessageToStaffView(MyModelView):
    column_sortable_list = ['date',	'replied']
    can_create = False
    can_edit = True
    can_delete = True
