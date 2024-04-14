from db import db


def login2(username, hash_value):
    #username = request.form["username"]
    #password = request.form["password"]
    # TODO: check username and password
    #hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    #if not user:
    # TODO: invalid username sign in 
    #else:
    hash_value = user.password
    #if check_password_hash(hash_value, password):
        # TODO: correct username and password
        #else:
        # TODO: invalid password

    #session["username"] = username
    #return redirect("/")