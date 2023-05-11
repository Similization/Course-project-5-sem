import os

from flask import Blueprint, render_template, current_app, session, redirect, url_for, request
from werkzeug import Response

from access import group_required
from config.db_work import get_dict, execute
from config.sql_provider import SQLProvider

blueprint_portfolio = Blueprint('blueprint_portfolio', __name__, template_folder='templates')

provider = SQLProvider(file_path=os.path.join(os.path.dirname(__file__), 'sql'))


# user portfolio
# get all user portfolios
@blueprint_portfolio.route('/all', methods=['GET'])
@group_required
def get_portfolio() -> str:
    sql = provider.get(name='user_portfolio.sql', user_id=session.get('user_id'))
    result = get_dict(dbconfig=current_app.config['db_config'], sql=sql)
    return render_template(
        template_name_or_list='user_portfolio.html',
        result=result
    )


def send_portfolio_info(sql_name: str, portfolio_id: int = 0):
    portfolio_name = request.form.get('portfolio_name')
    portfolio_birth_date = request.form.get('portfolio_birth_date')
    portfolio_address = request.form.get('portfolio_address')
    portfolio_sex = request.form.get('portfolio_sex')
    portfolio_about = request.form.get('portfolio_about').strip()
    sql = provider.get(
        name=sql_name,
        portfolio_id=portfolio_id,
        portfolio_user_id=session.get('user_id'),
        portfolio_name=portfolio_name,
        portfolio_birth_date=portfolio_birth_date,
        portfolio_address=portfolio_address,
        portfolio_sex=portfolio_sex,
        portfolio_about=portfolio_about,
    )
    execute(dbconfig=current_app.config['db_config'], sql=sql)


# user portfolio
# add new portfolio
@blueprint_portfolio.route('/new', methods=['GET', 'POST'])
@group_required
def add_portfolio_info() -> str | Response:
    if request.method == 'GET':
        return render_template(
            template_name_or_list='user_portfolio_info.html',
            redirect=request.referrer
        )
    else:
        send_portfolio_info(sql_name='user_portfolio_add.sql')
        return redirect(location=url_for('blueprint_portfolio.get_portfolio'))


# user portfolio
# update user portfolio
@blueprint_portfolio.route('/update/<int:portfolio_id>', methods=['GET', 'POST'])
@group_required
def update_portfolio_info(portfolio_id: int) -> str | Response:
    if request.method == 'GET':
        sql = provider.get(
            name='user_portfolio_get.sql',
            portfolio_id=portfolio_id,
            user_id=session.get('user_id')
        )
        result = get_dict(dbconfig=current_app.config['db_config'], sql=sql)[0]
        return render_template(
            template_name_or_list='user_portfolio_info.html',
            portfolio_id=portfolio_id,
            portfolio_name=result['name'],
            portfolio_birth_date=result['birth_date'],
            portfolio_address=result['address'],
            portfolio_sex=result['sex'],
            portfolio_about=result['about'],
            redirect=request.referrer
        )
    else:
        send_portfolio_info(sql_name='user_portfolio_update.sql', portfolio_id=portfolio_id)
        return redirect(location=url_for('blueprint_query.get_portfolio'))


# user portfolio
# delete user portfolio
@blueprint_portfolio.route('/delete/<int:portfolio_id>', methods=['GET'])
@group_required
def delete_portfolio_info(portfolio_id: int) -> str | Response:
    sql = provider.get(
        name='user_portfolio_delete.sql',
        portfolio_id=portfolio_id,
        user_id=session.get('user_id')
    )
    execute(dbconfig=current_app.config['db_config'], sql=sql)
    return redirect(location=url_for('blueprint_query.get_portfolio'))
