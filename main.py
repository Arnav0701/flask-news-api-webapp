from flask import Flask, request, render_template, redirect, flash, json, session
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import os
    
app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("SECRET_KEY not found in environment variables!")

API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY not found in environment variables!")

# app.secret_key = ""
# APIKey = ""

@app.route("/" , methods=["GET","POST"])
def login():
    with open("data.json","r") as f:
        users = json.load(f)

    if request.method == "POST":
        
        login_user_id = request.form["loginUserId"]
        login_user_password = request.form["loginPassword"]

        if login_user_id not in users:
            flash("User not found!","fail")
            return redirect("/")

        # Checking hashed password with user input password
        stored_password = users[login_user_id]["password"]

        if check_password_hash(stored_password, login_user_password):
            session["user_id"] = login_user_id   # store user id in session
            return redirect("/home")
        else:
            flash("User ID and Password does not match" ,"fail")
            return redirect("/")
    else:       
        return render_template("login.html")
    

@app.route("/signup" , methods=["GET","POST"])
def signup():
    if request.method == "POST":
        user_name = request.form["signupName"]
        user_name = user_name.title()
        user_id = request.form["signupID"]
        user_email = request.form["signupemail"]

        user_password = request.form["signupPassword"]
        confirm_password = request.form["confirmPassword"]

        with open("data.json","r") as f:
            users = json.load(f)

        if user_id in users:
            flash("User already exist! Try doing login or create a unique Id" ,"fail")
            return redirect("/signup")
        else:
            pass
        
        #storing section .
        if user_password != confirm_password :
            flash("password confirmation failed! Try again" ,"fail")
            return redirect("/signup")
        else:
            # hashing the password.
            hashed_password = generate_password_hash(user_password)
            users[user_id] = {"name":user_name,"password": hashed_password,"email":user_email, "preference":[]}
            with open("data.json","w") as f:
                json.dump(users,f,indent=4)

            flash("SIGNUP SUCCESSFUL" ,"success")
            return redirect("/")
    else:    
        return render_template("signup.html")


@app.route("/home", methods=["GET", "POST"])
def home():

    if "user_id" not in session:
        flash("Please login first", "fail")
        return redirect("/")

    user_id = session["user_id"]

    with open("data.json", "r") as f:
        users = json.load(f)

    preferences = users[user_id]["preference"]

    # Default category (first preference)
    category = preferences[0] if preferences else "Latest"

    #  Handle Search From Navbar (GET request)
    if request.method == "GET":
        searched_category = request.args.get("category")

        if searched_category:
            category = searched_category

    #  Handle Category Selection From Form (POST)
    if request.method == "POST":
        category = request.form.get("category", category)

    url = f"https://newsapi.org/v2/everything?q={category}&from=2026-01-20&sortBy=publishedAt&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    articles = [
        article
        for article in data.get("articles", [])
        if article.get("description") and article.get("urlToImage")
    ]
    return render_template("home.html", preferences=preferences, articles=articles, category=category)


@app.route("/newstoday", methods=["GET", "POST"])
def newstoday():
    if "user_id" not in session:
        flash("Please login first", "fail")
        return redirect("/")

    # Default values (for GET request)
    articles = []
    category = "Latest"

    if request.method == "POST":
        category = request.form.get("category", "Latest")
        
        url = f"https://newsapi.org/v2/everything?q={category}&from=2026-01-20&sortBy=publishedAt&apiKey={API_KEY}"
        # Send a request to News API
        response = requests.get(url)
        data = response.json()

        # Filter articles: Only include articles with description and urlToImage
        articles = [
            article for article in data.get("articles", [])
            if article.get("description") and article.get("urlToImage")
        ]
        
        return render_template("newstoday.html", articles=articles, category=category)
    
    if request.method == "GET":
        
        url = f"https://newsapi.org/v2/everything?q={category}&from=2026-01-20&sortBy=publishedAt&apiKey={API_KEY}"
        # Send a request to News API
        response = requests.get(url)
        data = response.json()

        # Filter articles: Only include articles with description and urlToImage
        articles = [
            article for article in data.get("articles", [])
            if article.get("description") and article.get("urlToImage")
        ]
        
        return render_template("newstoday.html", articles=articles, category=category)


@app.route("/about")
def about():
    if "user_id" not in session:
        flash("Please login first", "fail")
        return redirect("/")

    return render_template("about.html")


@app.route("/contact", methods=["GET","POST"])
def contact():
    if "user_id" not in session:
        flash("Please login first", "fail")
        return redirect("/")

    if request.method=="POST":
        ID = request.form["id"]
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]
        with open("contact.txt","a") as f:
            temp_str = f"\n\nID: {ID}\nName: {name}\nEmail: {email}\n"
            f.write(temp_str)
            temp_str = f"Message: {message}"
            f.write(temp_str)

    return render_template("contact.html")


@app.route("/profile")
def profile():
    if "user_id" not in session:
        flash("Please login first", "fail")
        return redirect("/")
    
    user_id = session["user_id"]
    with open("data.json", "r") as f:
        users = json.load(f)

    user = users[user_id]
    preferences = users[user_id]["preference"]
    return render_template("profile.html", preferences=preferences, user_id=user_id, user=user)


@app.route("/edit_preferences", methods=["GET", "POST"])
def edit_preferences():

    if "user_id" not in session:
        flash("Please login first", "fail")
        return redirect("/")

    user_id = session["user_id"]

    with open("data.json", "r") as f:
        users = json.load(f)

    if request.method == "POST":

        #  THIS is where you write it
        selected_preferences = request.form.getlist("preferences")

        users[user_id]["preference"] = selected_preferences

        with open("data.json", "w") as f:
            json.dump(users, f, indent=4)

        flash("Preferences updated successfully!", "success")
        return redirect("/edit_preferences")

    else:
        preferences = users[user_id]["preference"]

        AVAILABLE_CATEGORIES = ["Latest", "Trending", "Breaking News", "Top Stories", "Local News", "International News", "Technology", "Artificial Intelligence", "Machine Learning", "Cybersecurity", "Blockchain", "Startups", "Programming", "Gadgets", "Mobile Tech", "Cloud Computing", "Business", "Finance", "Stock Market", "Cryptocurrency", "Economy", "Investing", "Personal Finance", "Banking", "Real Estate", "Entrepreneurship", "Health", "Fitness", "Nutrition", "Mental Health", "Medical Research", "Yoga", "Lifestyle", "Entertainment", "Movies", "TV Shows", "Celebrities", "Music", "OTT Platforms", "Hollywood", "Bollywood", "Sports", "Cricket", "Football", "Tennis", "Basketball", "Olympics", "Esports", "Formula 1", "Science", "Space", "Astronomy", "Environment", "Climate Change", "Research", "Biotechnology", "Politics", "Government", "Elections", "Policy", "Law", "Social Issues", "World Affairs", "Education", "Career", "Job Market", "Competitive Exams", "Study Abroad", "Skill Development", "Gaming", "PC Games", "Mobile Games", "Console Games", "Game Reviews", "Automobile", "Electric Vehicles", "Car Reviews", "Bike Reviews", "Auto Industry", "Fashion", "Travel", "Food", "Art", "Photography", "Culture", "Books"]

        return render_template("edit_preferences.html", user_id=user_id, preferences=preferences, available_categories=AVAILABLE_CATEGORIES)


@app.route("/edit_profile", methods=["GET","POST"])
def edit_profile():
    if "user_id" not in session:
        flash("Please login first", "fail")
        return redirect("/")

    user_id = session["user_id"]

    # Load users
    with open("data.json", "r") as f:
        users = json.load(f)

    if request.method == "POST":
        nname = request.form["newName"]
        nemail = request.form["newEmail"]
        confpassword = request.form["ConfPassword"]

        # Verify password using hash
        if user_id in users and check_password_hash(users[user_id]["password"], confpassword):
            users[user_id]["name"] = nname
            users[user_id]["email"] = nemail

            # Save updated users
            with open("data.json", "w") as f:
                json.dump(users, f, indent=4)

            flash("Changes saved successfully", "success")
            return redirect("/profile")
        else:
            flash("Wrong password!", "fail")
            return redirect("/edit_profile")

    user = users[user_id]
    preferences = users[user_id].get("preference", [])

    return render_template("edit_profile.html", preferences=preferences, user_id=user_id, user=user)


@app.route("/logout",methods=["GET","POST"])
def logout():
    if request.method=="POST":
        choice = request.form.get("category")
        if choice=="yes":
            session.clear()
            flash("You have been logged out", "success")
            return redirect("/")
        else:
            return redirect("/profile")
    return render_template("logout.html")

app.run(debug=True)