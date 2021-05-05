from flask import Flask, request, flash, url_for, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import config
from flask_migrate import Migrate
from flask_mongoengine import MongoEngine
import datetime




'''
str ="jdbc:postgresql:User=postgres;Password=1234;Database=postgres;server=localhost;Port=5432;"

DATABASE_URL=str

app = Flask(__name__)

db = SQLAlchemy(app)
'''

admin_usernames={'admin'}

APP_SETTINGS="config.DevelopmentConfig"


app = Flask(__name__)
POSTGRES_URL = config.CONFIG['postgresUrl']
POSTGRES_USER = config.CONFIG['postgresUser']
POSTGRES_PASS = config.CONFIG['postgresPass']
POSTGRES_DB = config.CONFIG['postgresDb']
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PASS, url=POSTGRES_URL, db=POSTGRES_DB)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config.from_object(APP_SETTINGS)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOAD_FOLDER']= 'C:\\Users\\dnz_t\\OneDrive\\Masaüstü\\upld'
app.config['MAX_CONTENT_PATH']=1024*1024*1024


db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.config['MONGODB_SETTINGS'] = {
    'db': 'cnfappmongodb',
    'host': 'localhost',
    'port': 27017
}
me = MongoEngine()
me.init_app(app)

from models import *
from admin_functions import *
from conference_functions import *
from user_functions import *
from submission_functions import *



@app.route('/')
def opening():
    print('opening')
    return render_template('login.html')
    #print(datetime.datetime.now())
    #return 'hello ' + str(datetime.datetime.now())

    '''
    submission = MongoSubmission.objects().all()
    # submission.update(Title='title')

    if submission:
        return jsonify(submission.to_json())
        # submission.delete()
        # return 'deletion succesful'
        #return submission.__getitem__('Title')
    else:
        return 'record not found'

    # return jsonify(submission.to_json())
    '''


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    db.create_all()
    app.run(debug=True)

