from flask import Flask, request, flash, url_for, redirect, render_template, request
from app import app, admin_usernames, db, me
from models import *
from conference_functions import *
from user_functions import *
import os
from flask_pymongo import PyMongo
import datetime


@app.route('/new_submission_request')  # unaffiliated users
def new_submission_request():

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



    return render_template('new_submission.html', Conference=conference )


@app.route('/new_submission_submit', methods=['POST', 'GET'])  # unaffiliated users
def new_submission_submit():

    userid = request.cookies.get('authid')
    admin = request.cookies.get('admin')

    if request.method == 'POST':

        userinfo=UserInfo.query.filter_by(AuthenticationID=userid).first()

        title = request.form.get('title')
        abstract = request.form.get('abstract')
        keywords = request.form.get('keywords')
        authors = request.form.get('authors')
        submitted_by = userid
        corresponding_author = userinfo.Name + ' ' + userinfo.LastName
        pdf_path = request.files['pdf']

        submission_type = request.form.get('type')
        submissiondatetime = datetime.datetime.now()
        status = 0
        active = request.form.get('active')

        '''
        if pdf_path.filename != '':
            pdf_path.save(pdf_path.filename)

        pdf_path.save(os.path(app.config['UPLOAD_FOLDER'], pdf_path.filename))

        print('path', pdf_path.filename)
        '''

        confid = request.args.get('confid')
        prevsubmission = request.args.get('prevsubmission')

        submission = Submission(userid,confid, prevsubmission)
        db.session.add(submission)
        db.session.commit()

        submission = Submission.query.filter_by(AuthenticationID=userid, ConfID=confid, PrevSubmission=prevsubmission).first()

        #submission = Submission(PrevSubmissionID=prevsubmission, SubmissionID=submission.SubmissionID, Title=title, Abstract=abstract, Keywords=keywords, \
        #                        Authors=authors, SubmittedBy=userid, CorrespondingAuthor=corresponding_author, PdfPath='pdf_path', Type=type, SubmissionDateTime=submissiondatetime, Status=status, Active=active)


        mongosubmission = MongoSubmission(PrevSubmissionID=prevsubmission, SubmissionID=submission.SubmissionID, Title=title,
                                          Abstract=abstract, Keywords=keywords,
                                          Authors=None, SubmittedBy=submitted_by, CorrespondingAuthor=corresponding_author,
                                          PdfPath=pdf_path,
                                          Type=submission_type, SubmissionDateTime=submissiondatetime, Status=status, Active=active)

        # with open(pdf_path, 'rb') as fd:
        #    mongosubmission.PdfPath.put(fd)


        mongosubmission.save()

        return render_template('crud_conference.html', Conference=Conference.query.filter(
            Conference.CreatorUser == userid and Conference.ConfID.in_(NewUser.query.all())).all())




    #print(request.args.get('confid'),request.args.get('name'),request.args.get('year'),)
    #return 'hello world'



    return render_template('new_submission_page.html', Conference = Conference.query.all())


@app.route('/show_submissions')
def show_submissions():

    userid = request.cookies.get('authid')

    submission = MongoSubmission.objects(SubmittedBy=userid).first()

    return render_template('personal_submissions.html', Submission = MongoSubmission.objects().all())




@app.route('/update_submission_request')  # unaffiliated users
def update_submission_request():


    submissionid = request.args.get('submissionid')

    print('submissionid', submissionid)

    mongosubmission=MongoSubmission.objects(SubmissionID=submissionid).first()



    return render_template('new_submission.html', Submission=mongosubmission)


@app.route('/update_submission_submit', methods=['POST', 'GET'])  # unaffiliated users
def update_submission_submit():

    userid = request.cookies.get('authid')
    admin = request.cookies.get('admin')

    if request.method == 'POST':

        userinfo=UserInfo.query.filter_by(AuthenticationID=userid).first()

        title = request.form.get('title')
        abstract = request.form.get('abstract')
        keywords = request.form.get('keywords')
        authors = None
        submitted_by = userid
        corresponding_author = userinfo.Name + ' ' + userinfo.LastName
        pdf_path = request.files['pdf']

        submission_type = request.form.get('type')
        submissiondatetime = datetime.datetime.now()
        status = 1
        active = request.form.get('active')

        confid = request.args.get('confid')
        submissionid = request.args.get('submissionid')


        submission = Submission(userid, confid,  submissionid)
        db.session.add(submission)
        db.session.commit()

        submission = Submission.query.filter(ConfID=confid, AuthenticationID=userid, PreSubmission=submissionid)


        mongosubmission = MongoSubmission.objects(SubmissionID=submissionid).first()
        mongosubmission.update(PrevSubmissionID=submissionid, SubmissionID=submission.SubmissionID, Title=title,
                                          Abstract=abstract, Keywords=keywords,
                                          Authors=None, SubmittedBy=submitted_by, CorrespondingAuthor=corresponding_author,
                                          PdfPath=pdf_path,
                                          Type=submission_type, SubmissionDateTime=submissiondatetime, Status=status, Active=active)

        mongosubmission.save()

        return render_template('crud_conference.html', Conference=Conference.query.filter(
            Conference.CreatorUser == userid and Conference.ConfID.in_(NewUser.query.all())).all())




    #print(request.args.get('confid'),request.args.get('name'),request.args.get('year'),)
    #return 'hello world'



    return render_template('crud_conference.html', Conference = Conference.query.all())



@app.route('/delete_submission', methods=['POST', 'GET'])
def delete_submission():
    #return render_template('crud_conference.html', Conference = Conference.query.all() )



    userid = request.cookies.get('authid')
    admin = request.cookies.get('admin')

    submissionid=request.args.get('submissionid')
    mongosubmission = MongoSubmission.objects(SubmissionID=submissionid).first()
    submission=Submission.query.filter_by(SubmissionID=submissionid).first()

    while submission:
        submissionid=submission.PrevSubmission

        db.session.delete(submission)
        db.session.commit()

        mongosubmission.delete()

        mongosubmission = MongoSubmission.objects(SubmissionID=submissionid).first()
        submission = Submission.query.filter_by(SubmissionID=submissionid).first()



    return render_template('personal_submissions.html', Conference=Conference.query.filter(
        Conference.CreatorUser == userid and Conference.ConfID.in_(NewUser.query.all())).all())

    #print(request.args.get('confid'),request.args.get('name'),request.args.get('year'),)
    #return 'hello world'