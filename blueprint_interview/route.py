import os

from flask import Blueprint, render_template, current_app, session, redirect, url_for, request
from werkzeug import Response

from access import group_required
from config.db_work import get_schema, execute, get_dict, get_result
from config.sql_provider import SQLProvider

blueprint_interview = Blueprint('blueprint_interview', __name__, template_folder='templates')

provider = SQLProvider(file_path=os.path.join(os.path.dirname(__file__), 'sql'))


# external
# sign up for an interview
@blueprint_interview.route('/sign_up/<int:vacancy_id>&<int:portfolio_id>&<string:is_signed>', methods=['GET'])
@group_required
def sign_up_for_an_interview(vacancy_id: int, portfolio_id: int, is_signed: str) -> Response:
    if is_signed == "True":
        if portfolio_id == 0:
            sql = provider.get(
                name='user_interview_sign_up.sql',
                vacancy_id=vacancy_id,
                user_id=session.get('user_id')
            )
        else:
            sql = provider.get(
                name='user_interview_sign_up_with_portfolio.sql',
                vacancy_id=vacancy_id,
                portfolio_id=portfolio_id,
                user_id=session.get('user_id')
            )
        execute(dbconfig=current_app.config['db_config'], sql=sql)
    else:
        sql = provider.get(
            name='user_interview_sign_out.sql',
            vacancy_id=vacancy_id,
            user_id=session.get('user_id')
        )
        execute(dbconfig=current_app.config['db_config'], sql=sql)
    return redirect(location=url_for('blueprint_query.get_vacancy'))


# external
# sign out from an interview
@blueprint_interview.route('/sign_out/<int:vacancy_id>', methods=['GET'])
@group_required
def sign_out_from_an_interview(vacancy_id: int):
    sql = provider.get(
        name='user_interview_sign_out.sql',
        vacancy_id=vacancy_id,
        user_id=session.get('user_id')
    )
    execute(dbconfig=current_app.config['db_config'], sql=sql)
    return redirect(location=url_for('blueprint_interview.get_user_interview'))


# external
# interview results
@blueprint_interview.route('/results', methods=['GET'])
@group_required
def get_user_interview() -> str:
    sql = provider.get(
        name='user_interview.sql',
        user_id=session.get('user_id')
    )
    result, schema = get_schema(dbconfig=current_app.config['db_config'], sql=sql)
    return render_template(
        template_name_or_list='user_interview.html',
        schema=schema,
        result=result
    )


# typical
# main menu
@blueprint_interview.route('/menu', methods=['GET'])
@group_required
def interview_menu() -> str | Response:
    return render_template(
        template_name_or_list='typical_interview_menu.html',
    )


# typical
# unoccupied interview table
@blueprint_interview.route('/unoccupied', methods=['GET'])
@group_required
def interview_unoccupied_list() -> str:
    sql = provider.get(
        name='typical_interview_unoccupied_list.sql',
    )
    result, schema = get_schema(dbconfig=current_app.config['db_config'], sql=sql)
    return render_template(
        template_name_or_list='typical_interview.html',
        schema=schema,
        result=result,
        redirect='blueprint_interview.interview_unoccupied_list'
    )


# typical
# occupied interview table
@blueprint_interview.route('/occupied', methods=['GET'])
@group_required
def interview_occupied_list() -> str:
    sql = provider.get(
        name='typical_interview_occupied_list.sql',
    )
    result, schema = get_schema(dbconfig=current_app.config['db_config'], sql=sql)
    return render_template(
        template_name_or_list='typical_interview.html',
        schema=schema,
        result=result,
        redirect='blueprint_interview.interview_occupied_list'
    )


# typical
# all interview table
@blueprint_interview.route('/all', methods=['GET'])
@group_required
def interview_list() -> str:
    sql = provider.get(
        name='typical_interview_list.sql',
    )
    result, schema = get_schema(dbconfig=current_app.config['db_config'], sql=sql)
    return render_template(
        template_name_or_list='typical_interview.html',
        schema=schema,
        result=result,
        redirect='blueprint_interview.interview_list'
    )


def send_interview_info(sql_name: str, interview_id: int = -1):
    interview_interviewer = request.form.get('interview_interviewer')
    interview_enroll_id = request.form.get('interview_enroll_id')
    interview_date = request.form.get('interview_date')
    interview_result = request.form.get('interview_result')
    sql = provider.get(
        name=sql_name,
        interview_id=interview_id,
        interview_interviewer=interview_interviewer,
        interview_enroll_id=interview_enroll_id,
        interview_date=interview_date,
        interview_result=interview_result
    )
    execute(dbconfig=current_app.config['db_config'], sql=sql)


# typical
# update interview information
@blueprint_interview.route('/<int:interview_id>', methods=['GET', 'POST'])
@group_required
def update_interview_info(interview_id: int):
    if request.method == 'GET':
        sql = provider.get(
            name='typical_interview_get.sql',
            interview_id=interview_id
        )
        result = get_dict(dbconfig=current_app.config['db_config'], sql=sql)[0]

        sql = provider.get(
            name='admin_employee.sql'
        )
        interview_interviewers = get_dict(dbconfig=current_app.config['db_config'], sql=sql)

        sql = provider.get(
            name='typical_interview_enroll.sql'
        )
        interview_enrolls = get_result(dbconfig=current_app.config['db_config'], sql=sql)
        interview_enroll_ids = [interview_enroll[0] for interview_enroll in interview_enrolls]

        current_interviewer_id = result['interviewer_id']
        current_interviewer_name = result['interviewer']
        current_interview_enroll_id = result['interview_enroll_id']
        interview_date = result['date']
        current_interview_result = result['result']
        return render_template(
            template_name_or_list='typical_interview_info.html',
            current_interviewer_id=current_interviewer_id,
            current_interviewer_name=current_interviewer_name,
            interview_interviewers=interview_interviewers,
            current_interview_enroll_id=current_interview_enroll_id,
            interview_enroll_ids=interview_enroll_ids,
            interview_date=interview_date,
            current_interview_result=current_interview_result,
            redirect=request.referrer
        )
    else:
        redirect_url = request.form.get('redirect_url')
        send_interview_info(sql_name='typical_interview_update.sql', interview_id=interview_id)
        return redirect(redirect_url)
