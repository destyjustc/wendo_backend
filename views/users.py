from database import db
from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required
from flask_restplus import Namespace, Resource, fields

api = Namespace('users', description="Users related operations")

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(32), primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, dict):
        for key in dict:
            setattr(self, key, dict[key])

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

user_signin_api_model = api.model('User', {
    'username': fields.String(required=True, description="The username"),
    'password': fields.String(required=True, description="The password"),
})

user_api_model = api.model('User', {
    'id': fields.String(required=True, description="The user identifier"),
    'username': fields.String(required=True, description="The username"),
    'password': fields.String(required=True, description="The password"),
})

@api.route('/signin')
class UserSigninResource(Resource):
    @api.doc('user_sign_in')
    @api.marshal_with(user_signin_api_model)
    def post(self):
        '''User Sign in'''
        args = request.get_json()
        user = User.query.filter(User.username == args['username']). \
            filter(User.password == args['password']).first()
        if user is not None:
            return jsonify(user.as_dict())
        return jsonify(args)

@api.route('/')
class UserListResource(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_api_model)
    def get(self):
        '''List all users'''
        users = User.query.all()
        user_list = [user.as_dict() for user in users]
        return jsonify(user_list)

    @api.doc('create_new_user')
    @api.marshal_with(user_api_model)
    def post(self):
        '''Create an user'''
        args = request.get_json()
        user = User(args)
        db.session.add(user)
        db.session.commit()
        return jsonify(user.as_dict())

@api.route('/<id>')
@api.param('id', 'The user id')
class UserResource(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_api_model)
    def get(self, id):
        '''Fetch an user given its identifier'''
        user = User.query.filter(User.id == id).first()
        if user is not None:
            return jsonify(user.as_dict())
        api.abort(404)

    @api.doc('delete_user')
    @api.marshal_with(user_api_model)
    def delete(self, id):
        '''Remove an user given its identifier'''
        user = User.query.filter(User.id == id).first()
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return jsonify(user.as_dict())
        api.abort(404)

    @api.doc('update_user')
    @api.marshal_with(user_api_model)
    def put(self, id):
        '''Update an user given its identifier'''
        user = User.query.filter(User.id == id).first()
        args = request.get_json()
        args.pop('id', None)
        try:
            user.update(args)
            db.session.commit()
            return jsonify(user.as_dict())
        except Exception:
            api.abort(400)




