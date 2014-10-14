import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    if row is None:
        print "Student is not in records."
    else:
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
    if row is None:
        print "Project is not in records."
    else:
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
    if row is None:
        print "There is no record of that project for that student."
    else:
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
    DB.execute(query, (student,))
    if len(DB.fetchall()) == 0:
        print "That student has no grades or is not in the records."
    else:
        for item in DB.fetchall():
            print """\
    Student: %s
    Project: %s
    Grade: %s"""%(item[0], item[1], item[2])



def main():
    connect_to_db()
    command = None
    dict_args = {
    "student": (1, get_student_by_github),
    "new_student": (3, make_new_student),
    "title": (1, get_project_by_title),
    "new_project": (3, make_new_project),
    "get_grade": (2, get_grade_by_project),
    "assign_grade": (3, assign_grade),
    "all_grades": (1, get_grade_by_student),
    }
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split(", ")
        if len(tokens) == 0:
            print "Please enter a command.  Enter help for information, or quit"
            continue
        command = tokens[0]
        args = tokens[1:]

        if command in dict_args:
            if len(args) != dict_args[command][0]:#should think of efficient way to expand this to all commands
                print "Invalid input. Enter help for information, or quit"
            else:
                dict_args[command][1](*args)

        # if command == "student":
            # if len(args) < dict_args[command][0]:#should think of efficient way to expand this to all commands
            #     print "Enter help for information, or quit"
            #     continue
            #get_student_by_github(*args) 

        # elif command == "new_student":
        #     make_new_student(*args)
        # elif command == "title":
        #     get_project_by_title(*args)
        # elif command == "new_project":
        #     make_new_project(*args)
        # elif command == "get_grade":
        #     get_grade_by_project(*args)
        # elif command == "assign_grade":
        #     assign_grade(*args)
        # elif command == "all_grades":
        #     get_grade_by_student(*args)
        elif command != "quit":
            print """Valid commands: student, new_student, title, new_project, getgrade, assign_grade, all_grades\n
Format for using each command is:\n
Look up existing student: student, [github username]\n
Add new student: new_student, [first name], [last name], [github username]\n
Look up existing project: title, [project name]\n
Add new project: new_project, [project name], [project description], [maximum grade]\n
See student's grade from project: get_grade, [github username], [project name]\n
Assign grade to student: assign_grade, [github username], [project name], [project grade]\n
View all grades for student: all_grades, [github username]"""

    CONN.close()

if __name__ == "__main__":
    main()
