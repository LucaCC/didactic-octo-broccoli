from flask import Flask, request, Markup, render_template, flash, Markup
import os
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

@app.route("/")
def render_main():
    with open('county_demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    return render_template('Home.html', states = get_state_options(counties))

def state_fun_fact(state, counties):
    state = {}
    state_fun_fact = ""
    for data in counties:
        if data["State"] in state:
            state[data["State"]]["Bach"] += data["Education"]["Bachelor's Degree or Higher"]
            state[data["State"]]["High"] += data["Education"]["High School or Higher"]
            state[data["State"]]["Count"] += 1
        else:
            state[data["State"]] = {}
            state[data["State"]]["Bach"] = data["Education"]["Bachelor's Degree or Higher"]
            state[data["State"]]["High"] = data["Education"]["High School or Higher"]
            state[data["State"]]["Count"] = 1
        state_fun_fact = data["State"]

    for data in state:
        state[data]["Bach"] = (state[data]["Bach"]/state[data]["Count"])*2 # Weighted because higher degree
        state[data]["High"] = (state[data]["High"]/state[data]["Count"])
        state[data]["Edu"] = state[data]["Bach"] + state[data]["High"]

    # for data in state:
    #     if state[data]["Edu"] > state[state_fun_fact]["Edu"]:
    #         state_fun_fact = data

    return state_fun_fact

def get_state_options(counties):
    states = []
    print("Render")
    for data in counties:
        if data["State"] not in states:
            states.append(data["State"])
    options = ""
    for data in states:
        options = options + Markup("<option value=\"" + data + "\">" + data + "</option>")
    return options

if __name__=="__main__":
    app.run(debug=True)
