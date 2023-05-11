import os

from flask import Blueprint, render_template, current_app, session, redirect, url_for, request
from werkzeug import Response

from access import group_required
from blueprint_interview.route import sign_up_for_an_interview
from config.db_work import get_dict
from config.sql_provider import SQLProvider

blueprint_query = Blueprint('blueprint_query', __name__, template_folder='templates')

provider = SQLProvider(file_path=os.path.join(os.path.dirname(__file__), 'sql'))


# user
# get vacancy list
@blueprint_query.route('/vacancy', methods=['GET'])
@group_required
def get_vacancy() -> str:
    sql = provider.get(name='user_vacancy.sql')
    result = get_dict(dbconfig=current_app.config['db_config'], sql=sql)
    return render_template(template_name_or_list='user_vacancy.html', result=result)


# user
# get vacancy information
@blueprint_query.route('/vacancy/<int:vacancy_id>', methods=['GET', 'POST'])
@group_required
def get_vacancy_info(vacancy_id: int) -> str | Response:
    if request.method == 'GET':
        sql = provider.get('user_vacancy_info.sql', vacancy_id=vacancy_id)
        result = get_dict(current_app.config['db_config'], sql)[0]

        sql = provider.get(
            name='user_vacancy_register.sql',
            vacancy_id=vacancy_id,
            user_id=session.get('user_id')
        )

        vacancy_register_info = get_dict(current_app.config['db_config'], sql)
        is_available = len(vacancy_register_info) == 0
        employee_id = None
        current_portfolio_id = None
        if not is_available:
            employee_id = vacancy_register_info[0]["employee_id"]
            current_portfolio_id = vacancy_register_info[0]["portfolio_id"]

        sql = provider.get('user_portfolio.sql', user_id=session.get('user_id'))
        portfolios = get_dict(current_app.config['db_config'], sql)
        portfolios_id = [portfolio['portfolio_id'] for portfolio in portfolios]

        return render_template(
            template_name_or_list='user_vacancy_info.html',
            result=result,
            vacancy_id=vacancy_id,
            employee_id=employee_id,
            func=sign_up_for_an_interview,
            is_available=is_available,
            current_portfolio_id=current_portfolio_id,
            portfolios_id=portfolios_id,
            redirect=request.referrer
        )
    else:
        portfolio_id = request.form.get('user_portfolio_id') or 0
        is_signed = request.form.get('is_signed')
        return redirect(location=url_for(
            'blueprint_interview.sign_up_for_an_interview',
            vacancy_id=vacancy_id,
            portfolio_id=portfolio_id,
            is_signed=is_signed
        ))


# typical
# watch user's portfolio
@blueprint_query.route('/portfolio/<int:user_id>&<int:portfolio_id>', methods=['GET'])
@group_required
def watch_portfolio(user_id: int, portfolio_id: int):
    sql = provider.get(
        name='user_portfolio_get.sql',
        user_id=user_id,
        portfolio_id=portfolio_id
    )
    portfolio_info = get_dict(dbconfig=current_app.config['db_config'], sql=sql)[0]
    return render_template(
        template_name_or_list="typical_user_portfolio.html",
        portfolio_info=portfolio_info,
        redirect=request.referrer
    )
