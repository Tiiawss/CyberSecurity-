from db import db

def add_rating(rating, course_id):
    sql = "INSERT INTO reviews (rating, course_id) VALUES (:rating, :course_id)"
    db.session.execute(sql, {"rating":rating, "course_id":course_id})
    """sql= "INSERT INTO courses SELECT rating FROM reviews WHERE course_id"""

    
    db.session.commit()
def rev(id):
    sql= "SELECT rating FROM reviews WHERE course_id=:id"
    result = db.session.execute(sql, {"id":id})
    result_list = db.session.execute(sql, {"id":id}).fetchall()
    if len(result_list) == 0:
        return None
    return result_list

def fit(id):
    sql= "SELECT fit FROM shape WHERE course_id=:id"
    topic = db.session.execute(sql, {"id":id})
    fit_list = db.session.execute(sql, {"id":id}).fetchall()
    if len(fit_list) == 0:
        return None
    return fit_list
