import os

from flask import Blueprint, render_template, current_app, redirect, url_for, request, session

from access import group_required
from config.db_work import get_dict, execute, get_schema
from config.sql_provider import SQLProvider

blueprint_employee = Blueprint('blueprint_employee', __name__, template_folder='templates')

provider = SQLProvider(file_path=os.path.join(os.path.dirname(__file__), 'sql'))


# admin
# all employee table
@blueprint_employee.route('/all', methods=['GET'])
@group_required
def get_employee():
    sql = provider.get(name='admin_employee.sql')
    result, schema = get_schema(dbconfig=current_app.config['db_config'], sql=sql)
    return render_template(
        template_name_or_list='admin_employee.html',
        schema=schema,
        result=result,
        user_group=session.get("user_group", None)
    )


# admin
# add new employee
@blueprint_employee.route('/new', methods=['GET', 'POST'])
@group_required
def add_employee_info():
    if request.method == 'GET':
        sql = provider.get(
            name='user_vacancy.sql'
        )
        unoccupied_vacancies = get_dict(current_app.config['db_config'], sql)
        available_jobs = [(vacancy['job_id'], vacancy['job_name']) for vacancy in unoccupied_vacancies]
        return render_template(
            template_name_or_list='admin_employee_info.html',
            available_jobs=available_jobs,
        )
    else:
        employee_name = request.form.get('employee_name')
        employee_birth_date = request.form.get('employee_birth_date')
        employee_address = request.form.get('employee_address')
        employee_education = request.form.get('employee_education')
        employee_job_id = request.form.get('employee_job_id')
        sql = provider.get(
            name='admin_employee_add.sql',
            employee_name=employee_name,
            employee_birth_date=employee_birth_date,
            employee_address=employee_address,
            employee_education=employee_education,
            employee_job_id=employee_job_id,
        )
        execute(dbconfig=current_app.config['db_config'], sql=sql)
        return redirect(location=url_for('blueprint_employee.get_employee'))


# admin
# update employee information
@blueprint_employee.route('/update/<int:employee_id>', methods=['GET', 'POST'])
@group_required
def update_employee_info(employee_id: int):
    if request.method == 'GET':
        sql = provider.get(
            name='admin_employee_get.sql',
            employee_id=employee_id
        )
        res = get_dict(current_app.config['db_config'], sql)[0]
        sql = provider.get(
            name='user_vacancy.sql'
        )
        unoccupied_vacancies = get_dict(current_app.config['db_config'], sql)
        available_jobs = [(vacancy['job_id'], vacancy['job_name']) for vacancy in unoccupied_vacancies]
        return render_template(
            template_name_or_list='admin_employee_info.html',
            employee_name=res['name'],
            employee_birth_date=res['birth_date'],
            employee_address=res['address'],
            employee_education=res['education'],
            employee_job_id=res['job_id'],
            employee_job_name=res['job_name'],
            employee_enrollment_date=res['enrollment_date'],
            employee_dismissal_date=res['dismissal_date'],
            available_jobs=available_jobs
        )
    else:
        employee_name = request.form.get('employee_name')
        employee_birth_date = request.form.get('employee_birth_date')
        employee_address = request.form.get('employee_address')
        employee_education = request.form.get('employee_education')
        employee_job_id = request.form.get('employee_job_id')
        sql = provider.get(
            name='admin_employee_update.sql',
            employee_id=employee_id,
            employee_name=employee_name,
            employee_birth_date=employee_birth_date,
            employee_address=employee_address,
            employee_education=employee_education,
            employee_job_id=employee_job_id,
        )
        execute(dbconfig=current_app.config['db_config'], sql=sql)
        return redirect(location=url_for('blueprint_employee.get_employee'))


# admin
# delete employee information
@blueprint_employee.route('/delete/<int:employee_id>', methods=['GET'])
@group_required
def delete_employee_info(employee_id: int):
    sql = provider.get(
        name='admin_employee_delete.sql',
        employee_id=employee_id
    )
    execute(dbconfig=current_app.config['db_config'], sql=sql)
    return redirect(location=url_for('blueprint_employee.get_employee'))
