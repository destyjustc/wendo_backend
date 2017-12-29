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
from views.users import user, User
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'WHATEVER'
    db.init_app(app)
    app.register_blueprint(user, url_prefix='')
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
