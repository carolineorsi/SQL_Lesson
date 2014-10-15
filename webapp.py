from flask import Flask, render_template, request
import hackbright_app

app = Flask(__name__)

@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    student_name = hackbright_app.get_student_by_github(student_github)
    student_grades = hackbright_app.get_grade_by_student(student_github)
    html = render_template("student_info.html", first_name = student_name[0],
                                                last_name = student_name[1],
                                                github = student_name[2],
                                                projects = student_grades)
    return html

@app.route("/project_grades")
def get_grades():
    hackbright_app.connect_to_db()
    project = request.args.get("project")
    project_grades = hackbright_app.list_students_by_project(project)
    html = render_template("project_grades.html", project = project, grades = project_grades)
    return html

@app.route("/new_student")
def add_student():
    hackbright_app.connect_to_db()
    student_first_name = request.args.get("first_name")
    student_last_name = request.args.get("last_name")
    student_github = request.args.get("github")
    confirm = hackbright_app.make_new_student(student_first_name, student_last_name, student_github)
    html = render_template("get_github.html", add_student_successful = confirm)
    return html

@app.route("/new_project")
def add_project():
    hackbright_app.connect_to_db()
    project_title = request.args.get("project_title")
    project_description = request.args.get("project_description")
    max_grade = request.args.get("max_grade")
    confirm = hackbright_app.make_new_project(project_title, project_description, max_grade)
    html = render_template("get_github.html", add_project_successful = confirm)
    return html

@app.route("/assign_grade")
def assign_grade():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    project_title = request.args.get("project_title")
    grade = request.args.get("grade")
    confirm = hackbright_app.assign_grade(student_github, project_title, grade)
    html = render_template("get_github.html", assign_grade_successful = confirm)
    return html

@app.route("/")
def get_github():
    return render_template("get_github.html")

if __name__=="__main__":
    app.run(debug=True)