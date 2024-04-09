from flask import redirect, session
from functools import wraps


'''def login_required(f):
    """Decorate routes to require login.  https://flask.palletsprojects.com/en/2.3.x/patterns/viewdecorators/#view-decorators"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function'''


def fastest(dict):
    smallest = 20000
    fastest_person = []
    for x in dict:
        if float(dict[x][4]) < smallest:
            smallest = float(dict[x][4])
            fastest_person.clear()
            fastest_person.append(dict[x][1])
            fastest_person.append(dict[x][4])

    return fastest_person


def dict_creator(dataframe):
    dict = {}
    for ind in dataframe.index:
        my_list = []
        for x in dataframe.iloc[ind]:
            my_list.append(x)
        dict[ind] = my_list

    return dict
