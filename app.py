# from flask import Flask
# from flask_restful import Resource, Api
#
# app = Flask(__name__)
# api = Api(app)
#
# class HelloWorld(Resource):
#     def get(self):
#         return {'hello': 'world'}
#
# api.add_resource(HelloWorld, '/')
#
# if __name__ == '__main__':
#     app.run(debug=True)
from database import db
from flask import Flask, Blueprint
import os
from flask_jwt import JWT
from views.users import User
from views.schools import api as school_api
from views.students import api as student_api
from views.users import api as user_api
from flask_cors import CORS
from flask_restplus import Api

def init_api():
    api = Api(
        title="wendo",
        version='1.0',
        description="Wendo application apis",
        doc='/doc/'
    )
    api.add_namespace(student_api, path="/student")
    api.add_namespace(school_api, path="/school")
    api.add_namespace(user_api, path="/user")
    return api

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'WHATEVER'
    db.init_app(app)
    api = init_api()
    api.init_app(app)

    return app

app = create_app()

def verify(username, password):
    if not (username and password):
        return False
    user = User.query.filter(User.username == username).\
    filter(User.password == password).first()
    if user is not None:
        return user

def identity(payload):
    user_id = payload['identity']
    return {"user_id": user_id}

jwt = JWT(app, verify, identity)

if __name__ == '__main__':
    app.run()
