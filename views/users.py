from database import db
from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required

user = Blueprint('user', __name__)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@user.route('/')
@jwt_required()
def test():
    users = User.query.all()
    return jsonify([user.as_dict() for user in users])

@user.route('/signin', methods=['POST'])
def signin():
    args = request.form
    # user = User.query.filter()
    user = User.query.filter(User.username == args['username']).\
    filter(User.password == args['password']).first()
    if user is not None:
        return jsonify(user.as_dict())
    return jsonify(args)