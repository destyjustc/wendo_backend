from database import db
from flask import Blueprint, jsonify, request
from flask_jwt import JWT, current_identity, jwt_required
from flask_restplus import Namespace, Resource, fields
import uuid
from views.model_common import ModelCommon, model_super_model
from views.model_super import ModelSuper

api = Namespace('users', description="Users related operations")

class User(ModelCommon, ModelSuper):
    __tablename__ = 'users'

    username = db.Column(db.String(36), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    firstname = db.Column(db.String(36))
    lastname = db.Column(db.String(36))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(64))
    enabled = db.Column(db.Boolean, default=True)

    def __init__(self, dict):
        ModelSuper.__init__(self, dict)

class UserService(object):
    @classmethod
    def signin(cls, data):
        user = User.query.filter(User.username == data['username']). \
            filter(User.password == data['password']).first()
        if user is not None:
            return user
        api.abort(401)

    @classmethod
    def get(cls, id):
        user = User.query.filter(User.id == id).first()
        if user is not None:
            return user
        api.abort(404)

    @classmethod
    # @jwt_required()
    def get_list(cls):
        users = User.query.filter(User.enabled == True).all()
        return users

    @classmethod
    def create(cls, data):
        # TODO: check email or phone number exists
        tmp_user = User.query.filter(User.username == data['username']).first()
        if tmp_user:
            api.abort(409, "Username already exists.")
        id = uuid.uuid4()
        data['id'] = str(id)
        user = User(data)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def delete(cls, id):
        user = User.query.filter(User.id == id).first()
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return user
        api.abort(404)

    @classmethod
    def update(cls, id, data):
        data.pop('username', None)
        user = User.query.filter_by(id=id).first()
        user.update(data)
        db.session.commit()
        return user

user_request_model = api.model('User_request', {
    'username': fields.String(required=True, description="The username"),
    'password': fields.String(required=True, description="The password"),
    'firstname': fields.String(required=False, description="The first name"),
    'lastname': fields.String(required=False, description="The last name"),
    'email': fields.String(required=False, description="The email"),
    'phone': fields.String(required=False, description="The phone number"),
})

user_response_model = api.inherit('User_response', user_request_model, model_super_model, {})

@api.route('/')
class UserListResource(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_response_model)
    @jwt_required()
    def get(self):
        '''List all users'''
        return UserService.get_list()

    @api.doc('create_new_user')
    @api.marshal_with(user_response_model)
    @api.expect(user_request_model)
    @jwt_required()
    def post(self):
        '''Create an user'''
        args = request.get_json()
        return UserService.create(args)

@api.route('/<id>')
@api.param('id', 'The user id')
class UserResource(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_response_model)
    @jwt_required()
    def get(self, id):
        '''Fetch an user given its identifier'''
        return UserService.get(id)

    # @api.doc('delete_user')
    # @api.marshal_with(user_api_model)
    # def delete(self, id):
    #     '''Remove an user given its identifier'''
    #     return UserService.delete(id)

    @api.doc('update_user')
    @api.expect(user_request_model)
    @api.marshal_with(user_response_model)
    @jwt_required()
    def put(self, id):
        '''Update an user given its identifier'''
        args = request.get_json()
        return UserService.update(id, args)




