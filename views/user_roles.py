from database import db
from views.users import User, user_response_model
from views.roles import Role, role_response_model
from views.schools import School, school_response_model
from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields
import uuid
from views.model_common import ModelCommon, model_super_model
from views.model_super import ModelSuper
from flask_jwt import jwt_required

api = Namespace('user_roles', description="User and role relationship operations")

class UserRole(ModelCommon, ModelSuper):
    __tablename__ = 'user_roles'

    user_id = db.Column(db.String(36), db.ForeignKey(User.id))
    role_id = db.Column(db.String(36), db.ForeignKey(Role.id))
    school_id = db.Column(db.String(36), db.ForeignKey(School.id))
    user = db.relationship(User, foreign_keys=user_id, post_update=True, uselist=False)
    role = db.relationship(Role, foreign_keys=role_id, post_update=True, uselist=False)
    school = db.relationship(School, foreign_keys=school_id, post_update=True, uselist=False)

    def __init__(self, dict):
        ModelSuper.__init__(self, dict)

user_role_request_model = api.model('User_Role_Request', {
    'user_id': fields.String(required=True, description="The user identifier"),
    'role_id': fields.String(required=True, description="The role identifier"),
    'school_id': fields.String(required=True, description="The school identifier"),
})

user_role_response_model = api.inherit('User_Role_Response', model_super_model, {
    'user': fields.Nested(user_response_model),
    'role': fields.Nested(role_response_model),
    'school': fields.Nested(school_response_model),
})

class UserRoleService(object):
    @classmethod
    def create(cls, data):
        user_role = UserRole.query.filter_by(user_id=data['user_id'])\
            .filter_by(role_id=data['role_id'])\
            .filter_by(school_id=data['school_id']).first()
        if user_role:
            api.abort(409, "User role already exists.")
        id = uuid.uuid4()
        data['id'] = str(id)
        user_role = UserRole(data)
        db.session.add(user_role)
        db.session.commit()
        return user_role, 201

    @classmethod
    def get_user(cls, user_id):
        user = UserRole.query.filter(UserRole.user_id==user_id).first()
        return user

@api.route('/')
class UserRoleListResource(Resource):
    @api.doc('create_new_user_role')
    @api.expect(user_role_request_model)
    @api.marshal_with(user_role_response_model)
    @jwt_required()
    def post(self):
        '''Create a new user role record'''
        args = request.get_json()
        return UserRoleService.create(args)

@api.route('/<id>')
@api.param('id', 'The user id')
class UserRoleResource(Resource):
    @api.doc('get_user_role')
    @api.marshal_with(user_role_response_model)
    @jwt_required()
    def get(self, id):
        '''Fetch a user role record given user id'''
        return UserRoleService.get_user(id)

