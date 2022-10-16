from app import app
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from db import db
from os import getenv
import courses
import visits
import login



@app.route("/visitors")
def visitors():
    visits.add_visit()
    counter = visits.get_counter()
    return render_template("index.html", counter=counter)

@app.route("/")
def index():
    sql = "SELECT id, course_name, created_at FROM polls ORDER BY id DESC"
    result = db.session.execute(sql)
    polls = result.fetchall()
    return render_template("index.html", polls=polls)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/create", methods=["POST"])
def create():
    topic = request.form["name"]
    #sql = "INSERT INTO polls (topic, created_at) VALUES (:topic, NOW()) RETURNING id"
    #result = db.session.execute(sql, {"topic":topic})


    poll_id = result.fetchone()[0]
    choices = request.form.getlist("choice")
    course_name= request.form["name"]
    par = request.form["par"]
    lenght = request.form["lenght"]
    holes =request.form["holes"]
    city= request.form["city"]
    postcode=request.form["postnumber"]
    adress=request.form["adress"]

    """
    sql = "INSERT INTO courses (course_name, par, lenght, holes, city, postcode, adress) VALUES (:course_name, :par, :lenght, :holes, :city, :postcode, :adress)"
    db.session.execute(sql, {"course_name":course_name, "par":par, "lenght":lenght, "holes":holes, "city":city, "postcode":postcode, "adress":adress})
    """
    sql = "INSERT INTO polls (course_name, par, lenght, holes, city, postcode, adress, topic, created_at) VALUES (:course_name, :par, :lenght, :holes, :city, :postcode, :adress, :topic, NOW()) RETURNING id"
    db.session.execute(sql, {"course_name":course_name, "par":par, "lenght":lenght, "holes":holes, "city":city, "postcode":postcode, "adress":adress, "topic":topic})
    """for choice in choices:
        if choice != "":
            sql = "INSERT INTO choices (poll_id, choice) VALUES (:poll_id, :choice)"
            db.session.execute(sql, {"poll_id":poll_id, "choice":choice})
    """
    db.session.commit()

    return redirect("/")

@app.route("/poll/<int:id>")
def poll(id):
    sql = "SELECT topic FROM polls WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    topic = result.fetchone()[0]
    sql = "SELECT id, choice FROM choices WHERE poll_id=:id"
    result = db.session.execute(sql, {"id":id})
    choices = result.fetchall()
    return render_template("poll.html", id=id, topic=topic, choices=choices)

@app.route("/answer", methods=["POST"])
def answer():
    poll_id = request.form["id"]
    if "answer" in request.form:
        choice_id = request.form["answer"]
        sql = "INSERT INTO answers (choice_id, sent_at) VALUES (:choice_id, NOW())"
        db.session.execute(sql, {"choice_id":choice_id})
        db.session.commit()
    return redirect("/result/" + str(poll_id))

@app.route("/result/<int:id>")
def result(id):
    sql = "SELECT topic FROM polls WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    topic = result.fetchone()[0]
    sql = "SELECT c.choice, COUNT(a.id) FROM choices c LEFT JOIN answers a " \
          "ON c.id=a.choice_id WHERE c.poll_id=:poll_id GROUP BY c.id"
    result = db.session.execute(sql, {"poll_id":id})
    choices = result.fetchall()
    return render_template("result.html", topic=topic, choices=choices)



@app.route("/login",methods=["POST"])
def login1():
    username = request.form["username"]
    password = request.form["password"]
    # TODO: check username and password
    hash_value = generate_password_hash(password)
    login.login2(username, hash_value)
    #sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    #db.session.execute(sql, {"username":username, "password":hash_value})
    #db.session.commit()
    #sql = "SELECT id, password FROM users WHERE username=:username"
    #result = db.session.execute(sql, {"username":username})
    #user = result.fetchone()    
    #if not user:
    # TODO: invalid username sign in 
    #else:
    #hash_value = user.password
    #if check_password_hash(hash_value, password):
        # TODO: correct username and password
        #else:
        # TODO: invalid password

    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

"""@app.route("/order")
def order():
    return render_template("index.html")"""


"""
@app.route("/result", methods=["POST"])
def result2():
    course_name= request.form["course_name"]
    par = request.form["par"]
    lenght = request.form["lenght"]
    holes =request.form["holes"]
    city= request.form["city"]
    postcode=request.form["postcode"]
    adress=request.form["adress"]

    courses.add_course(course_name, par, lenght, holes, city, postcode, adress)
    #sql = "INSERT INTO courses (course_name, par, lenght, holes, city, postcode, adress) VALUES (:course_name, :par, :lenght, :holes, :city, :postcode, :adress)"
    #db.session.execute(sql, {"course_name":course_name, "par":par, "lenght":lenght, "holes":holes, "city":city, "postcode":postcode, "adress":adress})
    #db.session.commit()
    return redirect("/")"""