from database import db
from flask import Blueprint, jsonify, request
from flask_jwt import JWT, current_identity, jwt_required
from flask_restplus import Namespace, Resource, fields
import uuid
from views.model_common import ModelCommon, model_super_model
from views.model_super import ModelSuper
from views.users import User, user_response_model
from views.user_roles import UserRoleService

api = Namespace('whoami', description="who am i api")

class WhoAmIService(object):
    @classmethod
    def whoami(cls, id):
        user = User.query.filter_by(id=id).first()
        user = user.as_dict()
        school_id = UserRoleService.get_user(id).school_id
        user['school_id'] = school_id
        return user

whoami_response_model = api.inherit('User_Whoami', user_response_model, {
    'school_id': fields.String(description="The school id")
})

@api.route('/')
class UserWhoAmIResource(Resource):
    @api.doc('get user info')
    @api.marshal_with(whoami_response_model)
    @jwt_required()
    def get(self):
        '''Get user info by access token'''
        return WhoAmIService.whoami(current_identity['user_id'])