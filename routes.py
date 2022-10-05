from app import app
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import courses
import visits
import login



@app.route("/")
def index():
    visits.add_visit()
    counter = visits.get_counter()
    return render_template("index.html", counter=counter)

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

@app.route("/order")
def order():
    return render_template("index.html")



@app.route("/result", methods=["POST"])
def result():
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
    return redirect("/")