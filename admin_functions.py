from flask import Flask, request, flash, url_for, redirect, render_template
from app import app, admin_usernames, db
from models import *
from conference_functions import *
from user_functions import *



@app.route('/allusers')  # for admin to approve
def show_allusers():
    return render_template('allusers.html', UserInfo = UserInfo.query.all() )


@app.route('/newusers')  # unaffiliated users
def newusers():
    return render_template('newusers.html', UserInfo = UserInfo.query.join(NewUser, NewUser.NewUserID==UserInfo.AuthenticationID).all() )


@app.route('/confirm_new_user')  # unaffiliated users
def confirm_new_user():

    authenticationid = request.args.get('authenticationid')

    newuser = NewUser.query.filter_by(AuthenticationID=authenticationid).first()

    db.session.delete(newuser)
    db.session.commit()

    return render_template('newusers.html', UserInfo = UserInfo.query.filter_by(Affiliation=False) )


@app.route('/new_conferences')  # unaffiliated users
def new_conferences():
    return render_template('newusers.html', UserInfo = UserInfo.query.join(NewUser, NewUser.NewUserID==UserInfo.AuthenticationID).all() )


@app.route('/confirm_new_conference')  # unaffiliated users
def confirm_new_conference():

    confid = request.args.get('confid')

    newconference = NewConference.query.filter_by(ConfID=confid).first()

    db.session.delete(newconference)
    db.session.commit()

    return render_template('newusers.html', UserInfo = UserInfo.query.all() )

