from flask import Flask, request, flash, url_for, redirect, render_template
from app import app, admin_usernames, db
from models import *
from admin_functions import *
from user_functions import *
import datetime


@app.route('/create_conference_page', methods=['POST', 'GET'])
def create_conference_page():
    return render_template('new_conference.html')


@app.route('/create_conference_submit', methods=['POST', 'GET'])
def create_conference():

    userid = request.cookies.get('authid')
    admin = request.cookies.get('admin')

    print(userid,admin)

    if request.method == 'POST':
        if  not request.form['Name'] or \
            not request.form['ShortName'] or not request.form['Year'] or \
            not request.form['StartDate'] or not request.form['EndDate'] or \
            not request.form['SubmissionDeadLine'] :
            flash('Please enter all the fields', 'error')
        else:


            name = request.form.get('Name')
            shortname = request.form.get('ShortName')
            year = request.form.get('Year')
            startdate = request.form.get('StartDate')
            enddate = request.form.get('EndDate')
            submissiondeadline = request.form.get('SubmissionDeadLine')
            website = request.form.get('Website')

            old_confid=request.args.get('old_confid')
            print(datetime.datetime.now())

            conference = Conference(
                        '_{}_{}'.format(shortname, year),
                        datetime.datetime.now(),
                        name,
                        shortname,
                        year,
                        startdate,
                        enddate,
                        submissiondeadline,
                        userid,
                        website)

            conference_role = ConferenceRole(conference.ConfID, userid, 0)

            newconference= NewConference('_{}_{}'.format(shortname, year))

            db.session.add(conference)
            db.session.commit()

            #db.session.add(newconference)
            #db.session.add(conference_role)
            db.session.commit()


            return render_template('crud_conference.html', Conference=Conference.query.filter(
                Conference.CreatorUser == userid and Conference.ConfID.in_(NewUser.query.all())).all())

    #print(request.args.get('confid'),request.args.get('name'),request.args.get('year'),)
    #return 'hello world'

@app.route('/delete_conference', methods=['POST', 'GET'])
def delete_conference():
    #return render_template('crud_conference.html', Conference = Conference.query.all() )

    userid = request.cookies.get('authid')
    admin = request.cookies.get('admin')

    confid=request.args.get('confid')
    conference = Conference.query.filter_by(ConfID=confid).first()

    if conference:
        db.session.delete(conference)
        db.session.commit()

    return render_template('crud_conference.html', Conference=Conference.query.filter(
        Conference.CreatorUser == userid and Conference.ConfID.in_(NewUser.query.all())).all())

    #print(request.args.get('confid'),request.args.get('name'),request.args.get('year'),)
    #return 'hello world'



@app.route('/update_conference_page', methods=['POST', 'GET'])
def update_conference_page():
    #return render_template('crud_conference.html', Conference = Conference.query.all() )

    userid = request.cookies.get('authid')
    admin = request.cookies.get('admin')


    conference = Conference(
                request.args.get('confid'),
                request.args.get('creationdatetime'),
                request.args.get('name'),
                request.args.get('shortname'),
                request.args.get('year'),
                request.args.get('startdate'),
                request.args.get('enddate'),
                request.args.get('submissiondeadline'),
                request.args.get('creatoruser'),
                request.args.get('website'))

    return render_template('update_conference.html', Conference = conference )
    #print(request.args.get('confid'),request.args.get('name'),request.args.get('year'),)
    #return 'hello world'

@app.route('/update_conference_submit', methods=['POST', 'GET'])
def update_conference_submit():
    #return render_template('crud_conference.html', Conference = Conference.query.all() )

    userid = request.cookies.get('authid')
    admin = request.cookies.get('admin')

    if request.method == 'POST':
        if  not request.form['Name'] or \
            not request.form['ShortName'] or not request.form['Year'] or \
            not request.form['StartDate'] or not request.form['EndDate'] or \
            not request.form['SubmissionDeadLine'] :
            flash('Please enter all the fields', 'error')
        else:


            name = request.form.get('Name')
            shortname = request.form.get('ShortName')
            year = request.form.get('Year')
            startdate = request.form.get('StartDate')
            enddate = request.form.get('EndDate')
            submissiondeadline = request.form.get('SubmissionDeadLine')
            website = request.form.get('Website')

            old_confid=request.args.get('confid')

            conference2 = Conference.query.filter_by(ConfID=old_confid).first()

            conference2.ConfID = '_{}_{}'.format(shortname, year)
            conference2.Name = name
            conference2.ShortName = shortname
            conference2.Year = year
            conference2.StartDate = startdate
            conference2.EndDate = enddate
            conference2.SubmissionDeadLine = submissiondeadline
            conference2.Website = website

            db.session.commit()

            return render_template('crud_conference.html', Conference=Conference.query.filter(Conference.CreatorUser == userid and Conference.ConfID.in_(NewUser.query.all())).all())


    #print(request.args.get('confid'),request.args.get('name'),request.args.get('year'),)
    #return 'hello world'



@app.route('/showall_conferences', methods=['POST', 'GET'])
def showall_conferences():

    userid = request.cookies.get('authid')
    admin = request.cookies.get('admin')

    search_criteria = request.form['Name']



    return render_template('crud_conference.html', Conference = Conference.query.\
                           filter_by((Conference.Name.contains(search_criteria) or \
                                      Conference.ShortName.contains(search_criteria) or \
                                      Conference.ConfID.contains(search_criteria)) and \
                                     Conference.SubmissionDeadLine<datetime.datetime.now()).all())
    #print(request.args.get('confid'),request.args.get('name'),request.args.get('year'),)
    #return 'hello world'


@app.route('/show_users_to_assign_role')  # for admin to approve
def show_users_to_assign_role():
    userid = request.cookies.get('authid')

    conference = Conference(
        request.args.get('confid'),
        request.args.get('creationdatetime'),
        request.args.get('name'),
        request.args.get('shortname'),
        request.args.get('year'),
        request.args.get('startdate'),
        request.args.get('enddate'),
        request.args.get('submissiondeadline'),
        request.args.get('creatoruser'),
        request.args.get('website'))

    return render_template('allusers.html', UserInfo = UserInfo.query.filter_by(UserInfo.AuthenticationID!=userid).all(), Conference=conference )



@app.route('/assign_role')  # for admin to approve
def assign_role():
    userid = request.cookies.get('authid')

    confid = request.args.get('confid')
    role = request.args.get('role')
    authid = request.args.get('authid')


    conference = Conference.query.filter_by(ConfID=confid).first()

    ConferenceRole(confid,authid, role)

    db.session.add(ConferenceRole)
    db.session.commit()


    return render_template('allusers.html', UserInfo = UserInfo.query.filter_by(UserInfo.AuthenticationID!=userid).all(), Conference=conference)


@app.route('/add_tag')  # for admin to approve
def add_tag():
    userid = request.cookies.get('authid')

    confid = request.args.get('confid')
    role = request.args.get('role')
    authid = request.args.get('authid')

    conference = Conference.query.filter_by(ConfID=confid).first()

    ConferenceRole(confid, authid, role)

    db.session.add(ConferenceRole)
    db.session.commit()

    return render_template('allusers.html',
                           UserInfo=UserInfo.query.filter_by(UserInfo.AuthenticationID != userid).all(),
                           Conference=conference)