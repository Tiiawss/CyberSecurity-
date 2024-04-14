from app import app
from flask import redirect, render_template, request
import course_app
import visits
import ratings
import users
#from flask_wtf.csrf import CSRFProtect
#csrf = CSRFProtect(app)

@app.route("/visitors")
def visitors():
    visits.add_visit()
    counter = visits.get_counter()
    return render_template("index.html", counter=counter)

@app.route("/")
def index():
    visits.add_visit()
    counter = visits.get_counter()
    courses = course_app.index_course()
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
    list_sum=0
    list_counter=0
    if rev_list is None:
        result= "tätä rataa ei ole vielä arvioitu"
    else:
        for i in rev_list:
            list_sum=list_sum+i[0]
            list_counter=list_counter+1
        if list_sum ==0 or list_counter ==0:
            result=0
        else:
            result=round(list_sum/list_counter,2)

    fit_list=ratings.fit(id)
    list_sum=0
    list_counter=0
    if fit_list is None:
        fit= "tätä rataa ei ole vielä arvioitu"
    else:
        for i in fit_list:
            list_sum=list_sum+i[0]
            list_counter=list_counter+1
        if list_sum ==0 or list_counter ==0:
            fit=0
        else:
            fit=round(list_sum/list_counter,2)
    name=course_app.find_course(id)
    return render_template("reviews.html",result=result, fit=fit, name=name)

@app.route("/create_review", methods=["POST"])
def create_review():
    rating= request.form["rating"]
    course_id = request.form["id"]
    fit= request.form["fit"]
    ratings.add_rating(rating, course_id)
    ratings.add_shape(fit, course_id)
    #Below is XSS vunerability and the comment below is a fix
    return f"<script>alert('Your review has been successfully submitted!');</script>"
    #return redirect("/")

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
        
		return render_template("error.html", message="Väärä käyttäjätunnus tai salasana")


@app.route("/register", methods=["get", "post"])
def register():
	if request.method == "GET":
		return render_template("register.html")

	if request.method == "POST":
		username = request.form["username"]
		if len(username) < 2 or len(username) > 15:
			return render_template("error.html", message="Käyttätunnuksen tulee olla vähintään kaksi merkkiä ja enintään viisistoista merkkiä pitkä")
		key1 = request.form["password1"]
		key2 = request.form["password2"]
		if key1 != key2:
			return render_template("error.html", message="Salasanat eroavat")
		if key1 == "":
			return render_template("error.html", message="Salasana ei voi olla tyhjä")
		role = request.form["role"]
		if role not in ("1"):
			return render_template("error.html", message="Tuntematon käyttäjärooli")
		if not users.register(username, key1, role):
			return render_template("error.html", message="Rekisteröinti ei onnistunut")
		return redirect("/") 

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")
