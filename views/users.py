from database import db
from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required
from flask_restplus import Namespace, Resource, fields

api = Namespace('users', description="Users related operations")

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(36), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    firstname = db.Column(db.String(36))
    lastname = db.Column(db.String(36))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(64))
    enabled = db.Column(db.Boolean, default=False)

    def __init__(self, dict):
        for key in dict:
            setattr(self, key, dict[key])

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class UserService(object):
    @classmethod
    def signin(cls, data):
        user = User.query.filter(User.username == data['username']). \
            filter(User.password == data['password']).first()
        if user is not None:
            return user.as_dict()
        api.abort(401)

    @classmethod
    def get(cls, id):
        user = User.query.filter(User.id == id).first()
        if user is not None:
            return user.as_dict()
        api.abort(404)

    @classmethod
    def get_list(cls):
        users = User.query.filter(User.enabled == Ture).all()
        user_list = [user.as_dict() for user in users]
        return user_list

    @classmethod
    def create(cls, data):
        user = User(data)
        db.session.add(user)
        db.session.commit()
        return user.as_dict()

    @classmethod
    def delete(cls, id):
        user = User.query.filter(User.id == id).first()
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return user.as_dict()
        api.abort(404)

    @classmethod
    def update(cls, id, data):
        user = User.query.filter(User.id == id).first()
        try:
            user.update(data)
            db.session.commit()
            return user.as_dict()
        except Exception:
            api.abort(400)

user_signin_api_model = api.model('User', {
    'username': fields.String(required=True, description="The username"),
    'password': fields.String(required=True, description="The password"),
})

user_api_model = api.model('User', {
    'id': fields.String(required=True, description="The user identifier"),
    'username': fields.String(required=True, description="The username"),
    'password': fields.String(required=True, description="The password"),
    'firstname': fields.String(required=False, description="The first name"),
    'lastname': fields.String(required=False, description="The last name"),
    'email': fields.String(required=False, description="The email"),
    'phone': fields.String(required=False, description="The phone number"),
})

@api.route('/signin')
class UserSigninResource(Resource):
    @api.doc('user_sign_in')
    @api.marshal_with(user_signin_api_model)
    def post(self):
        '''User Sign in'''
        args = request.get_json()
        return UserService.signin(args)

@api.route('/')
class UserListResource(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_api_model)
    def get(self):
        '''List all users'''
        return UserService.get_list()

    @api.doc('create_new_user')
    @api.marshal_with(user_api_model)
    def post(self):
        '''Create an user'''
        args = request.get_json()
        return UserService.create(args)

@api.route('/<id>')
@api.param('id', 'The user id')
class UserResource(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_api_model)
    def get(self, id):
        '''Fetch an user given its identifier'''
        return UserService.get(id)

    @api.doc('delete_user')
    @api.marshal_with(user_api_model)
    def delete(self, id):
        '''Remove an user given its identifier'''
        return UserService.delete(id)

    @api.doc('update_user')
    @api.marshal_with(user_api_model)
    def put(self, id):
        '''Update an user given its identifier'''
        args = request.get_json()
        return UserService.update(id, args)




