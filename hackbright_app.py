import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT INTO Students VALUES (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s"%(first_name, last_name)

def get_project_by_title(title): 
    query = """SELECT title, description, max_grade FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
Title: %s 
Description: %s
Maximum Grade: %s"""%(row[0], row[1], row[2])

def make_new_project(title, description, max_grade):
    query = """INSERT INTO Projects (title, description, max_grade) VALUES (?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added project: %s" % title

def get_grade_by_project(student, project):
    query = """SELECT student_github, project_title, grade FROM Grades WHERE project_title = ? AND student_github = ?"""
    DB.execute(query, (project, student))
    row = DB.fetchone()
    print """\
    Student: %s
    Project: %s
    Grade: %s"""%(row[0], row[1], row[2])

def assign_grade(student, project, grade):
    query = """INSERT INTO Grades VALUES (?, ?, ?)"""
    DB.execute(query, (student, project, grade))
    CONN.commit()
    print "Successfully added a grade for student %s, project %s" % (student, project)

def get_grade_by_student(student):
    query = """SELECT student_github, project_title, grade FROM Grades WHERE student_github = ?"""
    for row in DB.execute(query, (student,)):
        print """\
        Student: %s
        Project: %s
        Grade: %s"""%(row[0], row[1], row[2])


def main():
    connect_to_db()
    command = None
    len_args = {
    "student": 1,
    "new_student": 3,
    "title": 1,
    "new_project": 3,
    "get_grade": 2,
    "assign_grade": 3,
    "all_grades": 1
    }
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        if len(tokens) == 0:
            print "Enter help for information, or quit"
            continue
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            if len(args) < len_args[command]:#should think of efficient way to expand this to all commands
                print "Enter help for information, or quit"
                continue
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "title":
            get_project_by_title(*args)
        elif command == "new_project":
            make_new_project(*args)
        elif command == "get_grade":
            get_grade_by_project(*args)
        elif command == "assign_grade":
            assign_grade(*args)
        elif command == "all_grades":
            get_grade_by_student(*args)
        else:
            print """Valid commands include: student, new_student, title, new_project, getgrade, assign_grade, all_grades\n
Format for using each command is:\n
To read about an existing student: student, [github username]\n
To add a new student: new_student, [first name], [last name], [github username]\n
To read about an existing project: title, [project name]\n
To add a new project: new_project, [project name], [project description], [maximum grade]\n
To get a student's grade from a project: get_grade, [github username], [project name]\n
To assign a grade to a student: assign_grade, [github username], [project name], [project grade]\n
To view all grades for a student: all_grades, [github username]"""

    CONN.close()

if __name__ == "__main__":
    main()
