from dataclasses import dataclass
from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.survey import Survey
from flask_app.models.user import User


@app.route('/new/survey')
def new_sighting():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template('survey.html', user=User.get_by_id(data))


@app.route('/create/survey', methods=['POST'])
def create_tree():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Survey.validate_survey(request.form):
        return redirect('/new/survey')
    data = {
        "impression": request.form["impression"],
        "feature": request.form["feature"],
        "value": request.form["value"],
        "useful": request.form["useful"],
        "available": request.form["available"],
        "recommend": request.form["recommend"],
        "comment": request.form["comment"],
        "user_id": session["user_id"]
    }
    Survey.save(data)
    return redirect('/dashboard')
