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

from statistics import mean





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

@app.route("/reviews/<int:id>")
def reviews(id):
    
    
    rev_list=ratings.rev(id)
    s=0
    d=0
    if rev_list== None:
        result= "tätä rataa ei ole vielä arvioitu"
    else:
        for i in rev_list:
            s=s+i[0]
            d=d+1
        if s ==0 or d ==0:
            result=0
        else:
            result=round(s/d,2)

    fit_list=ratings.fit(id)
    s=0
    d=0
    if fit_list== None:
        fit= "tätä rataa ei ole vielä arvioitu"
    else:
        for i in fit_list:
            s=s+i[0]
            d=d+1
        if s ==0 or d ==0:
            fit=0
        else:
            fit=round(s/d,2)
    name=course_app.find_course(id)
    
    
    
    
    
   

    return render_template("reviews.html",result=result, fit=fit, name=name)

@app.route("/create_review", methods=["POST"])
def create_review():
    
  
    rating= request.form["rating"]
    course_id = request.form["id"]
    fit= request.form["fit"]

    sql="INSERT INTO reviews (rating, course_id) VALUES (:rating, :course_id)"
    db.session.execute(sql, {"rating":rating, "course_id":course_id})
    db.session.commit()
    
    sql="INSERT INTO shape (fit, course_id) VALUES (:fit, :course_id)"
    db.session.execute(sql, {"fit":fit, "course_id":course_id})
    db.session.commit()
    #ratings.add_rating(rating,course_id)

    

    return redirect("/")


@app.route("/filter", methods=["get"])
def search():
	if request.method == "GET":
		return render_template("filter.html")
		

@app.route("/filtert")
def result():
    query = request.args["filtering"]
    courses=course_app.filter_courses(query)
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