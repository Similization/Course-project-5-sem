import os
from typing import Optional, Dict

from flask import (
    Blueprint, request,
    render_template, current_app,
    session, redirect, url_for
)

from config.db_work import get_dict
from config.sql_provider import SQLProvider

blueprint_auth = Blueprint('blueprint_auth', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_auth.route('/', methods=['GET', 'POST'])
def start_auth():
    if request.method == 'GET':
        return render_template('input_login.html', message='')
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        if login:
            user_info = define_user(login, password)
            if user_info:
                user_dict = user_info[0]
                session['user_id'] = user_dict['user_id']
                session['user_group'] = user_dict['user_group']
                session.permanent = True
                return redirect(location=url_for('main_menu'))
            else:
                return render_template(
                    template_name_or_list='input_login.html',
                    message='Пользователь не найден',
                    title="Аутентификация"
                )
        return render_template(
            template_name_or_list='input_login.html',
            message='Повторите ввод',
            title="Аутентификация"
        )


def define_user(login: str, password: str) -> Optional[Dict]:
    sql_internal = provider.get('internal_user.sql', login=login, password=password)
    sql_external = provider.get('external_user.sql', login=login, password=password)

    for sql_search in [sql_internal, sql_external]:
        user_info = get_dict(current_app.config['db_config'], sql_search)
        if user_info:
            return user_info
    return None
