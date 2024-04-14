from db import db

def rev(id):
    sql= "SELECT rating FROM reviews WHERE course_id=:id"
    result = db.session.execute(sql, {"id":id})
    result_list = db.session.execute(sql, {"id":id}).fetchall()
    if len(result_list) == 0:
        return None
    return result_list