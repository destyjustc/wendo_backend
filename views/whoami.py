from database import db
from flask import Blueprint, jsonify, request
from flask_jwt import JWT, current_identity, jwt_required
from flask_restplus import Namespace, Resource, fields
import uuid
from views.model_common import ModelCommon, model_super_model
from views.model_super import ModelSuper
from views.users import User, user_response_model
from views.user_roles import UserRoleService
from views.roles import RoleService, role_response_model

api = Namespace('whoami', description="who am i api")

class WhoAmIService(object):
    @classmethod
    def whoami(cls, id):
        user = User.query.filter_by(id=id).first()
        user = user.as_dict()
        user_role = UserRoleService.get_user(id)
        school_id = user_role.school_id
        role = RoleService.get(user_role.role_id)
        user['school_id'] = school_id
        user['role'] = role
        return user

whoami_response_model = api.inherit('User_Whoami', user_response_model, {
    'school_id': fields.String(description="The school id"),
    'role': fields.Nested(role_response_model),
})

@api.route('/')
class UserWhoAmIResource(Resource):
    @api.doc('get user info')
    @api.marshal_with(whoami_response_model)
    @jwt_required()
    def get(self):
        '''Get user info by access token'''
        return WhoAmIService.whoami(current_identity['user_id'])