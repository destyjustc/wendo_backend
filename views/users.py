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

@api.route('/signin')
class UserSignin(Resource):
    @api.doc('list_school')
    def post(self):
        '''User Sign in'''
        args = request.get_json()
        user = User.query.filter(User.username == args['username']). \
            filter(User.password == args['password']).first()
        if user is not None:
            return jsonify(user.as_dict())
        return jsonify(args)
