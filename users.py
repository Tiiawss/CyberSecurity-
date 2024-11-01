import os
from werkzeug.security import check_password_hash, generate_password_hash
from flask import abort, request, session, render_template_string
from db import db
from markupsafe import escape

def register(name, password, role):
	#if not re.search(r"\d", password) or not re.search(r"[A-Z]", password):
        #return False
	hash_value = generate_password_hash(password)
	try:
		sql = """INSERT INTO users (name, password, role) VALUES (:name, :password, :role)"""
		db.session.execute(sql, {"name":name, "password":hash_value, "role":role})
		db.session.commit()
	except:
		return False
	return login(name, password)

def login(name, password):
	sql = """SELECT password, id, role FROM users WHERE name=:name"""
	result = db.session.execute(sql, {"name":name})
	user = result.fetchone()
	if not user:
		return False
	if not check_password_hash(user[0], password):
		return False
	session["user_id"] = user[1]
	session["user_name"] = name
	session["user_role"] = user[2]
	session["csrf_token"] = os.urandom(16).hex()
	return True

def logout():
	del session["user_id"]
	del session["user_name"]
	del session["user_role"]

def check_id(name):
	sql = """SELECT id FROM users WHERE name=:name"""
	return db.session.execute(sql, {"name":name}).fetchone()[0]

def person_id():
	return session.get("user_id", 0)    

def check_role(role):
	if role > session.get("user_role", 0):
		abort(403)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

def person_sosial_security_number_input():
    sosial_security_number = request.args.get("CC", "")
    html_content = f"<input name='sosial security number' type='TEXT' value='{sosial_security}'>"
    return render_template_string(html_content)

//def person_sosial_security_number_input():
//sosial_security_number = request.args.get("CC", "")
//safe_sosial_security = escape(sosial_security)
//html_content = f"<input name='sosial security number' type='TEXT' value='{sosial_security}'>"
//    return render_template_string(html_content)
