from db import db

def add_rating(rating, course_id):
    sql = "INSERT INTO reviews (rating, course_id) VALUES (:rating, :course_id)"
    db.session.execute(sql, {"rating":rating, "course_id":course_id})
    """sql= "INSERT INTO courses SELECT rating FROM reviews WHERE course_id"""

    
    db.session.commit()