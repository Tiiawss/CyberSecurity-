from db import db

def add_course(course_name, par, lenght, holes, city, postcode, adress):
    sql = "INSERT INTO courses (course_name, par, lenght, holes, city, postcode, adress, created_at) VALUES (:course_name, :par, :lenght, :holes, :city, :postcode, :adress, NOW()) RETURNING id"
    db.session.execute(sql, {"course_name":course_name, "par":par, "lenght":lenght, "holes":holes, "city":city, "postcode":postcode, "adress":adress})

    
    db.session.commit()


def index_course():
    sql = "SELECT * FROM courses ORDER BY id DESC LIMIT 5"
    result = db.session.execute(sql)
    courses = result.fetchall()
    return courses

def find_course(id):
    sql ="SELECT course_name FROM courses WHERE id=:id"
    result = db.session.execute(sql, {"id":id}).fetchone()[0]
    return result

def filter_courses(query):
    if query=="1":
        sql = "SELECT * FROM courses ORDER BY id DESC LIMIT 5"
        result = db.session.execute(sql)
        courses = result.fetchall()
    elif query =="2":
        sql = "SELECT * FROM courses ORDER BY id LIMIT 5"
        result = db.session.execute(sql)
        courses = result.fetchall()
    elif query =="3":
        sql = "SELECT * FROM courses ORDER BY lenght LIMIT 5"
        result = db.session.execute(sql)
        courses = result.fetchall()
    elif query =="4":
        sql = "SELECT * FROM courses ORDER BY lenght DESC LIMIT 5"
        result = db.session.execute(sql)
        courses = result.fetchall()
    elif query =="5":
        sql = "SELECT * FROM courses ORDER BY par LIMIT 5"
        result = db.session.execute(sql)
        courses = result.fetchall()
    elif query =="6":
        sql = "SELECT * FROM courses ORDER BY par DESC LIMIT 5"
        result = db.session.execute(sql)
        courses = result.fetchall()
    
    


    
    
    return courses