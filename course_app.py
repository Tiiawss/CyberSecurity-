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
