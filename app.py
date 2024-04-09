import sqlite3
import pandas as pd

# from cs50 import SQL
from flask import Flask, render_template, request
# from flask import Flask, redirect, session
# from flask_session import Session
# from werkzeug.security import check_password_hash, generate_password_hash

from helpers import (
    #login_required,
    fastest,
    dict_creator,
)

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
''' app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app) '''

# Configure CS50 Library to use SQLite database
# db = SQL("sqlite:///project.db")

# Read sqlite query results into a pandas DataFrame
con = sqlite3.connect("results.db")
ndf = pd.read_sql_query("SELECT * from results", con)
pf23 = pd.read_sql_query(
    "SELECT team_name, ROUND(SUM(points), 0) as total_points from results WHERE year = '2023' GROUP BY team_name ORDER BY total_points desc", con)
pf22 = pd.read_sql_query(
    "SELECT team_name, ROUND(SUM(points), 0) as total_points from results WHERE year = '2022' GROUP BY team_name ORDER BY total_points desc", con)
driverdf = pd.read_sql_query(
    "SELECT *, MIN(fastest) as m, MAX(date), COUNT(DISTINCT(year)), MIN(position) FROM results GROUP BY driver_name ORDER BY m ASC", con)
driver22df = pd.read_sql_query(
    "SELECT driver_name, team_name, SUM(points) as total_points from results WHERE year = '2022' GROUP BY driver_name ORDER BY total_points desc", con)
driver23df = pd.read_sql_query(
    "SELECT driver_name, team_name, SUM(points) as total_points from results WHERE year = '2023' GROUP BY driver_name ORDER BY total_points desc", con)

# global variables - dictionaries etc - reset at login &
current_season = 2023
seasons_and_names = {
    "2023": ["Heat 1", "Heat 2", "Heat 3", "Heat 4", "F2 Final", "F1 Final"],
    "2022": ["Heat 1", "Heat 2", "Final"]
}


''' @app.context_processor
def inject_user():
    """to create dict of user session to make user available before templates are rendered"""
    try:
        x = session["user_id"]
    except:
        return {}
    else:
        username = db.execute(
            "SELECT username FROM users WHERE id = ?", session["user_id"]
        )[0]["username"].capitalize()
        return dict(user=username) '''


''' @app.after_request
def after_request(response):
    """This is to ensure that responses are not cached - caching responses
    is the default for Flask but may mean changes are not picked up by browser"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response '''


@app.route("/", methods=["GET"])
#@login_required  # decorator to ensure logged in
def index():
    """Show's main page including upcoming race info"""
    '''username = (
        #db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    )[0]["username"] '''

    return render_template(
        "index.html",
        #username=username,
        current_season=current_season,
    )


@app.route("/drivers", methods=["GET"])
#@login_required  # decorator to ensure logged in
def drivers():
    """Gets info for current drivers and displays their info in order of season standings"""

    driver_data = dict_creator(driverdf)

    return render_template(
        "drivers.html",
        current_season=current_season,
        driver_data=driver_data,
        driverdf=driverdf,
    )


@app.route("/drivers_championship", methods=["GET"])
#@login_required  # decorator to ensure logged in
def drivers_championship():
    """Gets info for current drivers and displays their info in order of season standings"""

    driver_data22 = dict_creator(driver22df)
    driver_data23 = dict_creator(driver23df)

    return render_template(
        "drivers_championship.html",
        current_season=current_season,
        driver_data22=driver_data22,
        driver_data23=driver_data23,
        driver22df=driver22df,
        driver23df=driver23df,
    )


@app.route("/teams", methods=["GET"])
#@login_required  # decorator to ensure logged in
def teams():
    """Gets info for current teams and displays their info in order of season standings"""

    team_data22 = dict_creator(pf22)
    team_data23 = dict_creator(pf23)

    return render_template(
        "teams.html",
        current_season=current_season,
        seasons_and_names=seasons_and_names,
        pf22=pf22,
        pf23=pf23,
        team_data22=team_data22,
        team_data23=team_data23,
    )


@app.route("/results", methods=["GET", "POST"])
#@login_required  # decorator to ensure logged in
def results():
    """Show's results of current race and allows users to select historical races to view"""

    data = dict_creator(ndf)
    fastest_person = fastest(data)

    if request.method == "POST":
        year = request.form.get("year")
        racename = request.form.get("racename")

        # if no year or race entered on submit or doesnt exist
        if not year:
            link = "/results"
            message = "Please select a year in the dropdown"
            return render_template("error_message.html", message=message, link=link)
        if not racename:
            link = "/results"
            message = "Please select a race in the dropdown"
            return render_template("error_message.html", message=message, link=link)

        # iterates and removes any rows not selected in data dictionary
        for x in list(data.keys()):
            if (data[x][8] != racename) or (data[x][10] != year):
                del data[x]

        fastest_person = fastest(data)

        return render_template(
            "results.html",
            year=year,
            racename=racename,
            seasons_and_names=seasons_and_names,
            fastest_person=fastest_person,
            ndf=ndf,
            data=data,
        )

    # if not post but get method
    else:

        return render_template(
            "results.html",
            seasons_and_names=seasons_and_names,
            fastest_person=fastest_person,
            ndf=ndf,
            data=data,
        )


''' @app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # resets these global variables if not already done

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            link = "/login"
            message = "Please provide a username"
            return render_template("error_message.html", message=message, link=link)

        # Ensure password was submitted
        elif not request.form.get("password"):
            link = "/login"
            message = "Please provide a password"
            return render_template("error_message.html", message=message, link=link)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            link = "/login"
            message = "Your username and password combination was incorrect"
            return render_template("error_message.html", message=message, link=link)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html") '''


''' @app.route("/logout")
def logout():
    """Log user out"""

    session.clear()  # Forget any user_id

    # resets these global variables

    # Redirect user to login form
    return redirect("/") '''


''' @app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Validate submission
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        hash_password = generate_password_hash(password)

        # if no username
        if not username:
            link = "/register"
            message = "Please enter a username in order to sign up"
            return render_template("error_message.html", message=message, link=link)

        already_exists = db.execute(
            "SELECT username FROM users WHERE username = ?", username
        )

        if already_exists:
            already_exists = already_exists[0]["username"]

        if username == already_exists:
            link = "/register"
            message = "That username already exists"
            return render_template("error_message.html", message=message, link=link)

        # if no password or password not match confirmation
        if not password or password != confirmation:
            link = "/register"
            message = "Please enter a password and make sure it matches the password confirmation"
            return render_template("error_message.html", message=message, link=link)
        # Remember registrant
        db.execute(
            "INSERT INTO users (username, hash) VALUES(?, ?)", username, hash_password
        )
        # once submitted it redirects to home
        return redirect("/")

    # if post not detected (i.e if GET) ask user to register
    else:
        return render_template("register.html") '''


''' @app.route("/deregister", methods=["GET", "POST"])
@login_required  # decorator to ensure logged in
def deregister():
    """deregister user"""

    if request.method == "POST":
        # Delete user from user table
        db.execute("DELETE FROM users WHERE id = ?", session["user_id"])
        # once submitted it redirects to home
        return redirect("/logout")

    else:
        #return render_template("deregister.html") '''
