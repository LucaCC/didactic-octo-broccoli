from flask import Flask, request, Markup, render_template, flash, Markup
import os
import json

# __name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)
app = Flask(__name__)


@app.route("/")
def render_main():
    with open('county_demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    if 'states' in request.args:
        return render_template('Home.html', states=get_state_options(counties), s_fun_fact=state_fun_fact(request.args['states'], counties), s=request.args['states'], counties=get_counties_options(counties, request.args['states']))

    elif 'counties' in request.args:
        return render_template('Home.html', states=get_state_options(counties), c_fun_fact=county_fun_fact(request.args['counties'], counties), c=request.args['counties'])

    else:
        return render_template('Home.html', states=get_state_options(counties))


def state_fun_fact(state_chosen, counties):
    state_fun_fact = ""
    count = 0
    pct_under_18 = 0
    key = "Perecent Under 18: "
    for data in counties:
        if data["State"] == state_chosen:
            pct_under_18 += data["Age"]["Percent Under 18 Years"]
            count += 1
    pct_under_18 = round((pct_under_18 / count), 2)

    state_fun_fact = pct_under_18

    return key + str(state_fun_fact)


def county_fun_fact(county_chosen, counties):
    county_fun_fact = ""
    pct_under_18 = 0
    key = "Perecent Under 18: "
    for data in counties:
        if data["County"] == county_chosen:
            pct_under_18 += data["Age"]["Percent Under 18 Years"]

    county_fun_fact = round(pct_under_18, 2)

    return key + str(county_fun_fact)


def get_state_options(counties):
    states = []
    for data in counties:
        if data["State"] not in states:
            states.append(data["State"])
    options = ""
    for data in states:
        options = options + \
            Markup("<option value=\"" + data + "\">" + data + "</option>")
    return options


def get_counties_options(counties, state):
    county = []
    for data in counties:
        if data["State"] in state:
            if data["County"] not in county:
                county.append(data["County"])
    options = ""
    for data in county:
        options = options + \
            Markup("<option value=\"" + data + "\">" + data + "</option>")
    return options


if __name__ == "__main__":
    app.run(debug=True)
