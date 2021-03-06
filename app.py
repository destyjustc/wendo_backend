from database import db
from flask import Flask, jsonify
import os
from flask_jwt import JWT, current_identity, JWTError
from views.users import User
from views.roles import Role
from views.schools import api as school_api
from views.students import api as student_api
from views.teachers import api as teacher_api
from views.courses import api as course_api
from views.users import api as user_api
from views.user_roles import api as user_role_api
from views.course_users import api as course_user_api
from views.roles import api as role_api
from views.payment import api as payment_api
from views.model_common import api as common_api
from views.clue_groups import api as clue_group_api
from views.clues import api as clue_api
from views.whoami import api as whoami_api
from flask_cors import CORS
from flask_restplus import Api

def init_api():
    api = Api(
        title="wendo",
        version='1.0',
        description="Wendo application apis",
        doc='/doc/'
    )
    api.add_namespace(common_api, path="/common")
    api.add_namespace(student_api, path="/student")
    api.add_namespace(school_api, path="/school")
    api.add_namespace(user_api, path="/user")
    api.add_namespace(teacher_api, path="/teacher")
    api.add_namespace(course_api, path="/course")
    api.add_namespace(user_role_api, path='/user_role')
    api.add_namespace(course_user_api, path='/course_user')
    api.add_namespace(role_api, path='/role')
    api.add_namespace(payment_api, path='/payment')
    api.add_namespace(clue_group_api, path='/clue_group')
    api.add_namespace(clue_api, path='/clue')
    api.add_namespace(whoami_api, path='/whoami')
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

def handle_user_exception_again(e):
    if isinstance(e, JWTError):
        return jsonify({
            'message': e.description,
            'code': e.status_code
        }), e.status_code
    return e

app.handle_user_exception = handle_user_exception_again

if __name__ == '__main__':
    app.run()
