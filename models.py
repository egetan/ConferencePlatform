from app import db, me
import enum
from flask_mongoengine import MongoEngine
from mongoengine import *
from flask_serialize import FlaskSerializeMixin

FlaskSerializeMixin.db=db

class User(db.Model, FlaskSerializeMixin):
    __tablename__ = 'Users'

    AuthenticationID = db.Column(db.Integer, db.ForeignKey('UsersInfo.AuthenticationID'), primary_key=True)
    Username = db.Column(db.VARCHAR(20))
    Password = db.Column(db.VARCHAR(50))

    def __init__(self, authenticationid, username, password):
        self.AuthenticationID= authenticationid
        self.Username = username
        self.Password = password

    def __repr__(self):
        return '<User {} {} {}>'.format(self.AuthenticationID, self.Username, self.Password)


    def serialize(self):
        return {
            'AuthenticationID': self.AuthenticationID,
            'Username': self.Username,
            'Password': self.Password
        }




class Conference(db.Model):
    __tablename__ = 'Conferences'

    ConfID = db.Column(db.VARCHAR(20), primary_key=True)
    CreationDateTime = db.Column(db.TIMESTAMP)
    Name = db.Column(db.VARCHAR(100))
    ShortName = db.Column(db.VARCHAR(19))
    Year = db.Column(db.Integer)
    StartDate = db.Column(db.TIMESTAMP)
    EndDate = db.Column(db.TIMESTAMP)
    SubmissionDeadLine = db.Column(db.TIMESTAMP)
    CreatorUser = db.Column(db.Integer, db.ForeignKey('UsersInfo.AuthenticationID'))
    Website = db.Column(db.VARCHAR(100))

    def __init__(self, confid, creation_datetime, name, shortname, year, startdate, enddate, submission_deadline, creator_user,
                 website):
        self.ConfID = confid
        self.CreationDateTime = creation_datetime
        self.Name = name
        self.ShortName = shortname
        self.Year = year
        self.StartDate = startdate
        self.EndDate = enddate
        self.SubmissionDeadLine = submission_deadline
        self.CreatorUser = creator_user
        self.Website = website

    def __repr__(self):
        return '<ConfID {}>'.format(self.ConfID)

    def serialize(self):
        return {
            'ConfID': self.ConfID,
            'CreationDateTime': self.CreationDateTime,
            'Name': self.Name,
            'ShortName': self.ShortName,
            'Year': self.Year,
            'StartDate': self.StartDate,
            'EndDate': self.EndDate,
            'SubmissionDeadLine': self.SubmissionDeadLine,
            'CreatorUser': self.CreatorUser,
            'Website': self.Website
        }


class cnf_role(enum.IntEnum):
    chair: 0
    reviewer: 1
    author: 2


class ConferenceRole(db.Model):
    __tablename__ = 'ConferenceRoles'

    ConfID = db.Column(db.VARCHAR(20), db.ForeignKey('Conferences.ConfID'), primary_key=True)
    AuthenticationID = db.Column(db.Integer, db.ForeignKey('Users.AuthenticationID'), primary_key=True)
    Role = db.Column(db.INT, nullable=False)

    def __init__(self, confid, authenticationid, role):
        self.ConfID = confid
        self.AuthenticationID = authenticationid
        self.Role = role

    def __repr__(self):
        return '<ConfID {}, AuthenticationID {}>'.format(self.ConfID, self.AuthenticationID)

    def serialize(self):
        return {
            'ConfID': self.ConfID,
            'AuthenticationID': self.AuthenticationID,
            'Role': self.Role
        }

class ConferenceTag(db.Model):
    __tablename__ = 'ConferenceTags'

    ConfID = db.Column(db.VARCHAR(20), db.ForeignKey('Conferences.ConfID'), primary_key=True)
    Tag = db.Column(db.VARCHAR(30), primary_key=True)

    def __init__(self, confid, tag):
        self.ConfID = confid
        self.Tag = tag

    def __repr__(self):
        return '<ConfID {}, Tag {}>'.format(self.ConfID, self.Tag)

    def serialize(self):
        return {
            'ConfID': self.ConfID,
            'Tag': self.Tag,
        }


class UserInfo(db.Model):
    __tablename__ = 'UsersInfo'

    AuthenticationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Salutation = db.Column(db.VARCHAR(50))
    Name = db.Column(db.VARCHAR(30))
    LastName = db.Column(db.VARCHAR(30))
    Affiliation = db.Column(db.VARCHAR(50))
    PrimaryEmail = db.Column(db.VARCHAR(50))
    SecondaryEmail = db.Column(db.VARCHAR(50))
    Password = db.Column(db.VARCHAR(50))
    Phone = db.Column(db.INT)
    Fax = db.Column(db.INT)
    Url = db.Column(db.VARCHAR(50))
    Address = db.Column(db.VARCHAR(100))
    City = db.Column(db.VARCHAR(100))
    Country = db.Column(db.VARCHAR(50))
    RecordCreationDate = db.Column(db.TIMESTAMP)

    def __init__(self, salutation, name, lastname, affiliation, primary_email, secondary_email, password, phone, fax,
                 url, address, city, country, record_creation_date):
        self.Salutation = salutation
        self.Name = name
        self.LastName = lastname
        self.Affiliation = affiliation
        self.PrimaryEmail = primary_email
        self.SecondaryEmail = secondary_email
        self.Password = password
        self.Phone = phone
        self.Fax = fax
        self.Url = url
        self.Address = address
        self.City = city
        self.Country = country
        self.RecordCreationDate = record_creation_date

    def __repr__(self):
        return '<AuthenticationID {}>'.format(self.AuthenticationID)

    def serialize(self):
        return {
            'AuthenticationID': self.AuthenticationID,
            'Saluation': self.Salutation,
            'Name': self.Name,
            'LastName': self.LastName,
            'Affiliation': self.Affiliation,
            'PrimaryEmail': self.PrimaryEmail,
            'SecondaryEmail': self.SecondaryEmail,
            'Password': self.Password,
            'Phone': self.Phone,
            'Fax': self.Fax,
            'Url': self.Url,
            'Address': self.Address,
            'City': self.City,
            'Country': self.Country,
            'RecordCreationDate': self.RecordCreationDate
        }

class UserLog(db.Model):
    __tablename__ = 'UserLog'

    AuthenticationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Salutation = db.Column(db.VARCHAR(50))
    Name = db.Column(db.VARCHAR(30))
    LastName = db.Column(db.VARCHAR(30))
    Affiliation = db.Column(db.BOOLEAN)
    PrimaryEmail = db.Column(db.VARCHAR(50))
    SecondaryEmail = db.Column(db.VARCHAR(50))
    Password = db.Column(db.VARCHAR(50))
    Phone = db.Column(db.INT)
    Fax = db.Column(db.INT)
    Url = db.Column(db.VARCHAR(50))
    Address = db.Column(db.VARCHAR(100))
    City = db.Column(db.VARCHAR(100))
    Country = db.Column(db.VARCHAR(50))
    RecordCreationDate = db.Column(db.TIMESTAMP)

    def __init__(self, salutation, name, lastname, affiliation, primary_email, secondary_email, password, phone, fax,
                 url, address, city, country, record_creation_date):
        self.Salutation = salutation
        self.Name = name
        self.LastName = lastname
        self.Affiliation = affiliation
        self.PrimaryEmail = primary_email
        self.SecondaryEmail = secondary_email
        self.Password = password
        self.Phone = phone
        self.Fax = fax
        self.Url = url
        self.Address = address
        self.City = city
        self.Country = country
        self.RecordCreationDate = record_creation_date

    def __repr__(self):
        return '<AuthenticationID {}>'.format(self.AuthenticationID)

    def serialize(self):
        return {
            'AuthenticationID': self.AuthenticationID,
            'Saluation': self.Salutation,
            'Name': self.Name,
            'LastName': self.LastName,
            'Affiliation': self.Affiliation,
            'PrimaryEmail': self.PrimaryEmail,
            'SecondaryEmail': self.SecondaryEmail,
            'Password': self.Password,
            'Phone': self.Phone,
            'Fax': self.Fax,
            'Url': self.Url,
            'Address': self.Address,
            'City': self.City,
            'Country': self.Country,
            'RecordCreationDate': self.RecordCreationDate
        }


class City(db.Model):
    __tablename__ = 'City'

    CityID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CountryCode = db.Column(db.CHAR(3), db.ForeignKey('Country.CountryCode'), primary_key=True)
    CityName = db.Column(db.VARCHAR(100))

    def __init__(self, country_code, city_name):
        self.CountryCode = country_code
        self.CityName = city_name

    def __repr__(self):
        return '<CityName {}, CountryCode {}>'.format(self.CityName, self.CountryCode)

    def serialize(self):
        return {
            'CityID': self.CityID,
            'CountryCode': self.CountryCode,
            'CityName': self.CityName
        }


class Country(db.Model):
    __tablename__ = 'Country'

    CountryCode = db.Column(db.CHAR(3), primary_key=True)
    CountryName = db.Column(db.VARCHAR(50))

    def __init__(self, country_code, country_name):
        self.CountryCode = country_code
        self.CountryName = country_name

    def __repr__(self):
        return '<CountryCode {}>'.format(self.CountryCode)

    def serialize(self):
        return {
            'CountryCode': self.CountryCode,
            'CountryName': self.CountryName,
        }

class NewUser(db.Model):
    __tablename__ = 'NewUsers'

    NewUserID=db.Column(db.INT, db.ForeignKey('UsersInfo.AuthenticationID'), primary_key=True)

    def __init__(self, id):
        self.NewUserID=id


class NewConference(db.Model):
    __tablename__ = 'NewConferences'

    NewCnfID = db.Column(db.VARCHAR(20), db.ForeignKey('Conferences.ConfID'), primary_key=True)

    def __init__(self, id):
        self.NewCnfID = id


class Submission(db.Model):
    __tablename__ = 'Submissions'


    AuthenticationID = db.Column(db.INT, db.ForeignKey('UsersInfo.AuthenticationID'), primary_key=True)
    ConfID = db.Column(db.VARCHAR(20), db.ForeignKey('Conferences.ConfID'), primary_key=True)
    SubmissionID = db.Column(db.INT, autoincrement=True, primary_key=True)
    PrevSubmission = db.Column(db.INT)

    def __init__(self, authenticationid, confid, prevsubmission):
        self.AuthenticationID = authenticationid
        self.ConfID = confid
        self.PrevSubmission = prevsubmission

class MongoSubmission(me.Document):
    PrevSubmissionID = IntField()
    SubmissionID = IntField()
    Title = StringField()
    Abstract = StringField()
    Keywords = StringField()
    Authors = ListField()
    SubmittedBy = IntField()
    CorrespondingAuthor = StringField()
    PdfPath = FileField()
    Type = StringField()
    SubmissionDateTime = DateTimeField()
    Status = IntField()
    Active = BooleanField()