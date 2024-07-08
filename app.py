''' This is the main file running the logic for the web app, using Flask to run routes '''

import sqlite3
import pandas as pd

from flask import (
    Flask,
    render_template,
    request,
)

from helpers import (
    fastest,
    dict_creator,
)

# Configure application
app = Flask(__name__)

# Read sqlite query results into a pandas DataFrame
con = sqlite3.connect("results.db")
ndf = pd.read_sql_query("SELECT * from results", con)
pf24 = pd.read_sql_query(
    "SELECT team_name, ROUND(SUM(points), 0) as total_points from results WHERE year = '2024' GROUP BY team_name ORDER BY total_points desc", con)
pf23 = pd.read_sql_query(
    "SELECT team_name, ROUND(SUM(points), 0) as total_points from results WHERE year = '2023' GROUP BY team_name ORDER BY total_points desc", con)
pf22 = pd.read_sql_query(
    "SELECT team_name, ROUND(SUM(points), 0) as total_points from results WHERE year = '2022' GROUP BY team_name ORDER BY total_points desc", con)
driverdf = pd.read_sql_query(
    "SELECT *, MIN(fastest) as m, MAX(year), COUNT(DISTINCT(year)), MIN(position) FROM results GROUP BY driver_name ORDER BY m ASC", con)
driverdfw = pd.read_sql_query(
    "SELECT *, MIN(fastest) as m, MAX(year), COUNT(DISTINCT(year)), MIN(position) FROM results WHERE condition = 'Wet' GROUP BY driver_name ORDER BY m ASC", con)
driver22df = pd.read_sql_query(
    "SELECT driver_name, team_name, SUM(points) as total_points from results WHERE year = '2022' GROUP BY driver_name ORDER BY total_points desc", con)
driver23df = pd.read_sql_query(
    "SELECT driver_name, team_name, SUM(points) as total_points from results WHERE year = '2023' GROUP BY driver_name ORDER BY total_points desc", con)
driver24df = pd.read_sql_query(
    "SELECT driver_name, team_name, SUM(points) as total_points from results WHERE year = '2024' GROUP BY driver_name ORDER BY total_points desc", con)

# global variables - dictionaries etc - reset at login &
current_season = 2024
seasons_and_names = {
    "2024": ["Heat 1", "Heat 2", "Final"],
    "2023": ["Heat 1", "Heat 2", "Heat 3", "Heat 4", "F2 Final", "F1 Final"],
    "2022": ["Heat 1", "Heat 2", "Final"]
}


@app.route("/", methods=["GET"])
def index():
    ''' Show's main page including upcoming race info '''

    return render_template(
        "index.html",
        #username=username,
        current_season=current_season,
    )


@app.route("/drivers", methods=["GET"])
def drivers():
    ''' Gets info for current drivers and displays their info in order of fastest laps '''

    driver_data = dict_creator(driverdf)
    driver_data_wet = dict_creator(driverdfw)

    return render_template(
        "drivers.html",
        current_season=current_season,
        driver_data=driver_data,
        driver_data_wet=driver_data_wet,
        driverdf=driverdf,
    )


@app.route("/drivers_championship", methods=["GET"])
def drivers_championship():
    ''' Gets info for current drivers and displays their info in order of standings '''

    driver_data22 = dict_creator(driver22df)
    driver_data23 = dict_creator(driver23df)
    driver_data24 = dict_creator(driver24df)

    return render_template(
        "drivers_championship.html",
        current_season=current_season,
        driver_data22=driver_data22,
        driver_data23=driver_data23,
        driver_data24=driver_data24,
        driver22df=driver22df,
        driver23df=driver23df,
        driver24df=driver24df,
    )


@app.route("/teams", methods=["GET"])
def teams():
    ''' Gets info for current teams and displays their info in order of standings '''

    team_data22 = dict_creator(pf22)
    team_data23 = dict_creator(pf23)
    team_data24 = dict_creator(pf24)

    return render_template(
        "teams.html",
        current_season=current_season,
        seasons_and_names=seasons_and_names,
        pf22=pf22,
        pf23=pf23,
        pf24=pf24,
        team_data22=team_data22,
        team_data23=team_data23,
        team_data24=team_data24,
    )


@app.route("/results", methods=["GET", "POST"])
def results():
    ''' Show's results of all races and allows users to select historical races to view '''

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
