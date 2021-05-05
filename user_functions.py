from flask import Flask, request, flash, url_for, redirect, render_template
from flask import make_response
from app import app, admin_usernames, db
from models import *
from admin_functions import *
from conference_functions import *
from submission_functions import *
import datetime


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not request.form['username'] or not request.form['password']:
            flash('Please enter all the fields', 'error')
        else:
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter_by(
                Username=username, Password=password).first()  # if this returns a user, then the email already exists in database

            if user:  # if a user is found, we want to redirect back to signup page so user can try again

                newuser = NewUser.query.filter_by(NewUserID=user.AuthenticationID).first()

                if not newuser:

                    userinfo = UserInfo.query.filter_by(AuthenticationID=user.AuthenticationID).first()

                    response = make_response(render_template('crud_conference.html', Conference=Conference.query
                                                             .filter(Conference.CreatorUser==user.AuthenticationID ).all()))
                    if (user.Username in admin_usernames):
                        response.set_cookie("authid", str(user.AuthenticationID), max_age=None)
                        response.set_cookie("admin", "True", max_age=None)
                    else:
                        response.set_cookie("authid", str(user.AuthenticationID))
                        response.set_cookie("admin", "False")

                    return response

                else:
                    flash('Your account is not confirmed yet!')
                    return render_template('login.html')


            else:
                flash('Incorrect Email or Password')
                print('hereee 66666')
                return render_template('login.html')




    else:
        print('here 444444444')


@app.route('/crud_conference_page', methods=['GET', 'POST'])
def crud_conference_page():
    userid = request.cookies.get('authid')
    admin = request.cookies.get('admin')

    return render_template('crud_conference.html', Conference=Conference.query
                                             .filter(Conference.CreatorUser == userid).all())


@app.route('/signup_page', methods=['GET', 'POST'])
def signup_page():
    return render_template('register.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if False:
            print('signup1')
            return render_template('register.html')


        else:
            email = request.form.get('primaryEmail')

            user_info = UserInfo.query.filter_by(
                PrimaryEmail=email).first()  # if this returns a user, then the email already exists in database

            if user_info:  # if a user is found, we want to redirect back to signup page so user can try again
                flash('This email belongs to another account')
                return render_template('login.html')

            else:
                salutation = request.form.get('salutation')
                name = request.form.get('name')
                lastname = request.form.get('lastname')
                affiliation = request.form.get('affiliation')
                primary_email = request.form.get('primaryEmail')
                secondary_email = request.form.get('secondaryEmail')
                password = request.form.get('password')
                phone = request.form.get('phone')
                fax = request.form.get('fax')
                url = request.form.get('url')
                address = request.form.get('address')
                city = request.form.get('city')
                country = request.form.get('country')

                username = request.form.get('username')


                user_info = UserInfo(salutation,
                                     name,
                                     lastname,
                                     affiliation,
                                     primary_email,
                                     secondary_email,
                                     password,
                                     phone,
                                     fax,
                                     url,
                                     address,
                                     city,
                                     country,
                                     datetime.datetime.now())


                db.session.add(user_info)
                db.session.commit()

                user_id = UserInfo.query.filter_by(
                    PrimaryEmail=email).first().AuthenticationID

                user = User(user_id, username, password)
                newuser = NewUser(user_id)

                db.session.add(user)
                db.session.add(newuser)
                db.session.commit()

                print('signup2')
                #return redirect(url_for('/'))
                return render_template('login.html')

    print('signup3')


@app.route('/update_userinfo_page', methods=['POST', 'GET'])
def update_userinfo_page():
    # return render_template('crud_conference.html', Conference = Conference.query.all() )

    userid = request.cookies.get('authid')
    admin = request.cookies.get('admin')

    #userinfo=db.Session.query(UserInfo).join(User, User.AuthenticationID==UserInfo.AuthenticationID).filter(User.AuthenticationID==userid).first()
    userinfo=UserInfo.query.filter_by(AuthenticationID=userid).first()
    user=User.query.filter_by(AuthenticationID=userid).first()
    #userinfo =UserInfo.followed.append(user)

    #print('join', userinfo.Username)



    return render_template('update_userinfo.html', UserInfo=userinfo, User=user)
    # print(request.args.get('confid'),request.args.get('name'),request.args.get('year'),)
    # return 'hello world'


@app.route('/update_userinfo_submit', methods=['GET', 'POST'])
def update_userinfo_submit():
    userid=request.cookies.get('authid')
    admin=request.cookies.get('admin')

    print('userid', userid)

    if request.method == 'POST':
        if False:
            flash('Please enter all the fields', 'error')
            userinfo = UserInfo.query.filter_by(AuthenticationID=userid).first()
            return render_template('update_userinfo.html', UserInfo=userinfo)


        else:
            primaryemail = request.form.get('PrimaryEmail')
            secondaryemail = request.form.get('SecondaryEmail')
            username = request.form.get('Username')

            user_info = UserInfo.query.filter(UserInfo.AuthenticationID != userid) \
                                                 .filter((UserInfo.PrimaryEmail==primaryemail) or (UserInfo.SecondaryEmail==secondaryemail)).first()

            user= User.query.filter(User.AuthenticationID!=userid).filter(User.Username==username).first()

            #print('user', user.AuthenticationID)

            if user_info:
                userinfo = UserInfo.query.filter_by(AuthenticationID=userid).first()
                user = User.query.filter_by(AuthenticationID=userid).first()
                flash('This email belongs to another user')
                return render_template('update_userinfo.html', UserInfo=userinfo, User=user)

            elif user is not None:
                print(user)
                userinfo = UserInfo.query.filter_by(AuthenticationID=userid).first()
                user = User.query.filter_by(AuthenticationID=userid).first()
                flash('This username belongs to another user')
                return render_template('update_userinfo.html', UserInfo=userinfo, User=user)
            else:

                user_info = UserInfo.query.filter(UserInfo.AuthenticationID==userid).first()
                user = User.query.filter(User.AuthenticationID == userid).first()

                salutation = request.form.get('Salutation')
                name = request.form.get('Name')
                lastname = request.form.get('LastName')
                affiliation = request.form.get('Affiliation')
                password = request.form.get('Password')
                phone = request.form.get('Phone')

                fax = request.form.get('Fax')
                if fax =='':
                    fax = None

                url = request.form.get('Url')
                address = request.form.get('Address')
                city = request.form.get('City')
                country = request.form.get('Country')

                print('password', password)

                user_info.Salutation = salutation
                user_info.Name = name
                user_info.LastName = lastname
                user_info.Affiliation = affiliation
                user_info.PrimaryEmail = primaryemail
                user_info.SecondaryEmail = secondaryemail
                user_info.Password = password
                user_info.Phone = phone
                user_info.Fax = fax
                user_info.Url = url
                user_info.Address = address
                user_info.City = city
                user_info.Country = country


                user.Username=username
                user.Password=password

                db.session.commit()

                return render_template('crud_conference.html',
                                       Conference=Conference.query.filter_by(CreatorUser=userid).all())

    #else:


