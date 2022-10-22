from tkinter import INSERT
from app import app
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from db import db
from os import getenv
import course_app
import visits
import login
import ratings
import users




@app.route("/visitors")
def visitors():
    visits.add_visit()
    counter = visits.get_counter()
    return render_template("index.html", counter=counter)

@app.route("/")
def index():
    visits.add_visit()
    counter = visits.get_counter()
    courses= course_app.index_course()
    
    return render_template("index.html", courses=courses, counter=counter)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/create", methods=["POST"])
def create():
    
  
    course_name= request.form["name"]
    par = request.form["par"]
    lenght = request.form["lenght"]
    holes =request.form["holes"]
    city= request.form["city"]
    postcode=request.form["postnumber"]
    adress=request.form["adress"]

    course_app.add_course(course_name, par, lenght, holes, city, postcode, adress)
    return redirect("/")
@app.route("/review/<int:id>")
def review(id):
    
    return render_template("review.html",id=id)

@app.route("/reviews", methods=["POST"])
def reviews(id):
    id=id
    sql= "SELECT rating FROM reviews"
    topic = db.session.execute(sql)
    result = topic.fetchall()

    return render_template("reviews.html",result=result)

@app.route("/create_review", methods=["POST"])
def create_review():
    
  
    rating= request.form["rating"]
    course_id = request.form["id"]
    fit= request.form["fit"]

    sql="INSERT INTO reviews (rating, course_id) VALUES (:rating, :course_id)"
    db.session.execute(sql, {"rating":rating, "course_id":course_id})
    db.session.commit()
   
    #ratings.add_rating(rating,course_id)

    """sql="INSERT INTO shape (fit, course_id) VALUES (:fit, :course_id)"
    db.session.execute(sql, {"fit":fit, "course_id":course_id})
    db.session.commit()
    sql= "INSERT INTO courses (hardness) SELECT fit FROM shape WHERE course_id=id"
    db.session.execute(sql, {"fit":fit, "course_id":course_id})
    db.session.commit()"""

   
    """sql = "INSERT INTO reviews (rating, course_id) VALUES (:rating, :course_id)"
    db.session.execute(sql, {"rating":rating, "course_id":course_id})
    sql= "INSERT INTO courses SELECT rating FROM reviews WHERE course_id"""

    
    

    return redirect("/")


@app.route("/filter", methods=["get"])
def search():
	if request.method == "GET":
		return render_template("filter.html")
		

@app.route("/filtert")
def result():
    query = request.args["filtering"]
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
    
    


    
    else:
        return render_template("error.html", message="Haullasi ei löytynyt aineistoa") 
    return render_template("filter.html", courses=courses)





@app.route("/login", methods=["get", "post"])
def login():
	if request.method == "GET":
		return render_template("login.html")
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		if users.login(username, password):
			return redirect("/")
		else:
			return render_template("error.html", message="Väärä käyttäjätunnus tai salasana")


@app.route("/register", methods=["get", "post"])
def register():
	if request.method == "GET":
		return render_template("register.html")

	if request.method == "POST":
		username = request.form["username"]
		if len(username) < 1 or len(username) > 15:
			return render_template("error.html", message="Käyttätunnuksen tulee olla 1-15 merkkiä pitkä")
		password1 = request.form["password1"]
		password2 = request.form["password2"]
		if password1 != password2:
			return render_template("error.html", message="Salasanat eroavat")
		if password1 == "":
			return render_template("error.html", message="Salasana ei voi olla tyhjä")
		
		role = request.form["role"]
		if role not in ("1", "2"):
			return render_template("error.html", message="Tuntematon käyttäjärooli")
		if not users.register(username, password1, role):
			return render_template("error.html", message="Rekisteröinti ei onnistunut")
		return redirect("/") 

@app.route("/logout")
def logout():
	users.logout()
	return redirect("/")