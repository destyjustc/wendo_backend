from database import db
from views.users import User
from views.roles import Role
from views.schools import School
from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields
import uuid

api = Namespace('user_roles', description="User and role relationship operations")

class UserRole(db.Model):
    __tablename__ = 'user_roles'

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey(User.id))
    role_id = db.Column(db.String(36), db.ForeignKey(Role.id))
    school_id = db.Column(db.String(36), db.ForeignKey(School.id))
    user = db.relationship(User, foreign_keys=user_id, post_update=True, uselist=False)
    role = db.relationship(Role, foreign_keys=role_id, post_update=True, uselist=False)
    school = db.relationship(School, foreign_keys=school_id, post_update=True, uselist=False)

    def __init__(self, dict):
        for key in dict:
            setattr(self, key, dict[key])

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def update(self, dict):
        for i in dict:
            setattr(self, i, dict[i])

user_role_api_model = api.model('UserRole', {
    'id': fields.String(required=True, description="The user_role identifier"),
    'user_id': fields.String(required=True, description="The user identifier"),
    'role_id': fields.String(required=True, description="The role identifier"),
    'school_id': fields.String(required=True, description="The school identifier"),
})

user_role_post_model = api.model('UserRole', {
    'user_id': fields.String(required=True, description="The user identifier"),
    'role_id': fields.String(required=True, description="The role identifier"),
    'school_id': fields.String(required=True, description="The school identifier"),
})

class UserRoleService(object):
    @classmethod
    def create(cls, data):
        id = uuid.uuid4()
        data['id'] = str(id)
        user_role = UserRole(data)
        db.session.add(user_role)
        db.commit()
        return user_role, 201

    @classmethod
    def get_user(cls, user_id):
        user = UserRole.query.filter(UserRole.user_id==user_id).first()
        return user.as_dict()

@api.route('/')
class UserRoleListResource(Resource):
    @api.doc('create_new_user_role')
    @api.marshal_with(user_role_post_model)
    def post(self):
        '''Create a new user role record'''
        args = request.get_json()
        return UserRoleService.create(args)

@api.route('/<id>')
@api.param('id', 'The user id')
class UserRoleResource(Resource):
    @api.doc('get_user_role')
    @api.marshal_with(user_role_api_model)
    def get(self, id):
        '''Fetch a user role record given user id'''
        return UserRoleService.get_user(id)

