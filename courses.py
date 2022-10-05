from db import db

def add_course(course_name, par, lenght, holes, city, postcode, adress):
    sql = "INSERT INTO courses (course_name, par, lenght, holes, city, postcode, adress) VALUES (:course_name, :par, :lenght, :holes, :city, :postcode, :adress)"
    db.session.execute(sql, {"course_name":course_name, "par":par, "lenght":lenght, "holes":holes, "city":city, "postcode":postcode, "adress":adress})
    db.session.commit()