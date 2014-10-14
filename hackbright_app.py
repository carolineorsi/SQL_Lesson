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
    #DB.execute(query, (project, student))
    for row in DB.execute(query, (student,)):
    #row = DB.fetchone()
        print """\
        Student: %s
        Project: %s
        Grade: %s"""%(row[0], row[1], row[2])


def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "title":
            get_project_by_title(*args)
        elif command == "new_project":
            make_new_project(*args)
        elif command == "getgrade":
            get_grade_by_project(*args)
        elif command == "assign_grade":
            assign_grade(*args)
        elif command == "all_grades":
            get_grade_by_student(*args)

    CONN.close()

if __name__ == "__main__":
    main()
