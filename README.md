# Personal Project - KARTFEST race results
## Overview
    This project looks to create a convenient way to show info for the history of races we have undertaken as a friendship group, including drivers & teams standings, as well as results. I've uploaded csv results of races to an sqlite3 database file used by the webapp.

    The means by which I've chosen to implement this project is through a web-based application using Python (Flask), Jinja, HTML, CSS, JavaScript and SQL. SQL was used initially to set up the database for users (results.db database containing the results table). This database is then used to send data to the webapp. The bulk of the web app is coded in python (in app.py) and uses multiple functions (in helpers.py). I chose to utlise Flask as a web framework for displaying pages and the data within. Flask uses HTML templates (set up from a 'parent' layout file) to render the web pages. I've also used Bootstrap as a CSS framework to style my web pages for consistency, aestetics and ease. There is also a small amount of additional, more custom CSS in a CSS styles file.

    On loading, the app displays the home page with information about historic races and upcoming races and pictures and map data for them.
    The Drivers page in the Nav-bar displays data for all the drivers in the friendship group based on each drivers fastest lap
    The Drivers' Championships page shows details of each driver standing for each year's final race / races.
    The Constructor's Championships page shows details of each driver standing for each year's final race / races.
    The race results page in the Nav-bar shows all time race data in a table, but also allows the user to search and select a specific year and race to look at, summarising the fastest driver and winner.

## Files & contents

### **Static**
    The static folder at the root of the project is for holding the folders for images returned from APi calls (for Driver, Race, Teams and Track pictures). This is in an aim to improve the efficiency of the app as these pictures can be pulled from here in the future rather than repeatadly doing API calls. There are then also a few image files for logos which are used in headers and footers on pages. Finally, the file styles.css holds the CSS for any custom CSS not being handled by Bootstrap. This is mainly for handling logos contained within certain bootstrap elements, as well as custom table styling and all the custom colour codes for the main and current Formula One teams.

### **Templates**
    The Templates folder holds all the flask template files to be interacted with and rendered, as well as for variables being passed through using placeholders and Jinja syntax.

    • drivers.html
    This template displays all the drivers, along with their information, in order of their fastest lap times. This is done utlising Flask to pass through a dictionary containing all the data, and then iterating through that and displaying data using Jinja syntax, onto Bootstrap cards.

    • index.html
    This is our home page and the first page you see once logged in. It uses bootstrap cards to show different race data based on races each year.
    For each card it displays info about the race as well as displaying map data via Bing Maps API & Google maps API also.

    • layout.html
    The main layout.html file which contains the navbar / header for any HTML file rendered, as well as the footer (basically anything that is the same across pages). Contains the stylesheets for the pages as well as Boostrap plugins for CSS and JavaScript.

    • results.html
    This file starts with some JavaScript for the drop down lists on the page. They work by being passed a dictionary which contains the list of seasons and races within. It then allows the first dropdown items to be populated from the seaons as the dictionary keys and then once selected the second drodown will populate from the values (races) associated with that key (season)
    By default it will display all race data, but on submit (POST) it will render and pass back the selected race's details in the tables below.
    There is also then some JavaScript which allows for the results table data above to be exported to csv and downloaded by the user

    • teams.html
    This template displays the results of each year by team along with their information, in order of their position within the constructor's championship. This is done utlising Flask to pass through a dictionary containing all the data, and then iterating through that and displaying data using Jinja syntax, onto Bootstrap cards.

    • drivers_championship.html
    This template displays the results of each year by driver along with their information, in order of their position within the drivers's championship. This is done utlising Flask to pass through a dictionary containing all the data, and then iterating through that and displaying data using Jinja syntax, onto Bootstrap cards.

### **app.py**
    This is perhaps our 'main' file doing most of the work of the webapp. It begins by importing the OS module for its functionality to be used later.
    It then imports from flask various modules to allow for the main functionalities of my webapp (e.g redirects and templates being rendered).
    Then all my helper functions are imported form my helpers.py file which will be used within my app.
    Still within the set up of the file at the top are my top level global variables (dictionaries etc). These are here to be written to as my app runs so they are only required to be created once and can be used across all routes and also reset when users log in and out.

### **helpers.py**
    This file contain all our functions to be pulled into app.py so that file is more streamlined.

### **results.db**
    This is our SQLite database for storing all the result data. It is interacted with by app.py in order to display data to all the routes through SQL queries and pandas dataframes as well as dictionaries.

### **README.md**
    This is the file you are reading right now, which contains a write up of the project. Here we aim to explain the project as well as giving an overview and description of what each of the files do and how it all works together. I also hope to explain why i made certain design choices and why I implemented things the way I have.
