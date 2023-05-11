import json

from flask import Flask, render_template, session, redirect, url_for

from access import login_required
from blueprint_auth.route import blueprint_auth
from blueprint_query.route import blueprint_query
from blueprint_report.route import blueprint_report
from blueprint_interview.route import blueprint_interview
from blueprint_portfolio.route import blueprint_portfolio
from blueprint_employee.route import blueprint_employee

app = Flask(__name__)
app.secret_key = "SuperKey"

app.register_blueprint(blueprint_auth, url_prefix="/auth")
app.register_blueprint(blueprint_query, url_prefix="/queries")
app.register_blueprint(blueprint_report, url_prefix="/report")
app.register_blueprint(blueprint_interview, url_prefix="/interview")
app.register_blueprint(blueprint_portfolio, url_prefix="/portfolio")
app.register_blueprint(blueprint_employee, url_prefix="/employee")

with open("data_files/db_config.json", "r") as file:
    db_config = json.load(file)
with open("data_files/access.json", "r") as file:
    access_config = json.load(file)
with open("data_files/report_list.json", "r", encoding="utf-8") as file:
    report_list = json.load(file)
with open("data_files/report_url.json", "r", encoding="utf-8") as file:
    report_url = json.load(file)

app.config["db_config"] = db_config
app.config["access_config"] = access_config
app.config["report_list"] = report_list
app.config["report_url"] = report_url


@app.route("/", methods=["GET", "POST"])
def main_menu():
    if "user_id" in session:
        if session.get("user_group", None):
            return render_template(
                template_name_or_list="internal_user_menu.html",
                title="Меню внутреннего пользователя",
                user_group=session.get("user_group", None)
            )
        else:
            return render_template(
                template_name_or_list="external_user_menu.html",
                title="Меню внешнего пользователя",
            )
    else:
        return redirect(location=url_for("blueprint_auth.start_auth"))


@app.route("/exit")
@login_required
def exit_function():
    session.clear()
    return render_template(template_name_or_list="exit.html", title="Выход")


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True, port=5005)
