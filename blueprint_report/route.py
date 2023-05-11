import os

from flask import Blueprint, request, render_template, current_app, redirect, url_for

from access import group_required
from config.db_work import call_procedure, get_result, get_schema
from config.sql_provider import SQLProvider

blueprint_report = Blueprint('blueprint_report', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_report.route('/', methods=['GET', 'POST'])
@group_required
def start_report():
    report_list = current_app.config['report_list']
    report_url = current_app.config['report_url']
    if request.method == 'GET':
        return render_template('report_menu.html', report_list=report_list)
    else:
        rep_id = request.form.get('rep_id')
        if request.form.get('create_rep'):
            url_rep = report_url[rep_id]['create_rep']
        else:
            url_rep = report_url[rep_id]['view_rep']
        return redirect(url_for(url_rep))


def create_report(sql_name: str, procedure_name: str, redirect_name: str):
    if request.method == 'GET':
        return render_template(template_name_or_list='create_report.html')
    else:
        year_month = list(map(int, request.form.get('date').split('-')))
        if year_month:
            sql = provider.get(
                name=sql_name,
                report_year=year_month[0],
                report_month=year_month[1]
            )
            result = get_result(current_app.config['db_config'], sql)
            if len(result) != 0:
                return render_template(template_name_or_list="report_exist_info.html")
            call_procedure(
                current_app.config['db_config'],
                procedure_name,
                year_month[1],
                year_month[0]
            )
            return render_template(template_name_or_list="report_create_info.html")
        else:
            return redirect(location=url_for(redirect_name))


def get_table(sql_name: str, template_name: str, key: str):
    if request.method == 'GET':
        sql = provider.get(
            name=sql_name + '.sql',
        )
    else:
        year_month = list(map(int, request.form.get('date').split('-')))
        sql = provider.get(
            name=sql_name + "_by_date.sql",
            year=year_month[0],
            month=year_month[1]
        )
    product_result = get_result(dbconfig=current_app.config['db_config'], sql=sql)
    return render_template(
        template_name_or_list=template_name,
        result=product_result,
        key=key
    )


@blueprint_report.route('/report_view_menu/<int:year>&<int:month>', methods=['GET', 'POST'])
@group_required
def get_report(year: int, month: int):
    key = request.args.get('key')
    sql = provider.get(
        name='admin_' + key + '_report_table_by_date.sql',
        year=year,
        month=month
    )
    product_result, schema = get_schema(dbconfig=current_app.config['db_config'], sql=sql)
    return render_template(
        template_name_or_list='report_view_table.html',
        result=product_result,
        schema=schema
    )


@blueprint_report.route('/create_employee_report', methods=['GET', 'POST'])
@group_required
def create_employee_report():
    return create_report(
        sql_name='admin_employee_report_exist.sql',
        procedure_name='generate_employee_report',
        redirect_name='blueprint_report.create_employee_report'
    )


@blueprint_report.route('/view_employee_report', methods=['GET', 'POST'])
@group_required
def view_employee_report():
    return get_table(
        sql_name='admin_employee_report_view',
        template_name='report_view_menu.html',
        key='employee'
    )


@blueprint_report.route('/create_vacancy_report', methods=['GET', 'POST'])
@group_required
def create_vacancy_report():
    return create_report(
        sql_name='admin_vacancy_report_exist.sql',
        procedure_name='generate_vacancy_report',
        redirect_name='blueprint_report.create_vacancy_report'
    )


@blueprint_report.route('/view_vacancy_report', methods=['GET', 'POST'])
@group_required
def view_vacancy_report():
    return get_table(
        sql_name='admin_vacancy_report_view',
        template_name='report_view_menu.html',
        key='vacancy'
    )
