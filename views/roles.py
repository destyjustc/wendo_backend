from database import db
from flask_restplus import Namespace, Resource, fields
from views.model_super import ModelSuper
from flask_jwt import jwt_required

api = Namespace('role', description="Role related operations")

class Role(db.Model, ModelSuper):
    __tablename__ = 'roles'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(128))

    def __init__(self, dict):
        ModelSuper.__init__(self, dict)

class RoleService(object):
    @classmethod
    def get_list(cls):
        roles = Role.query.all()
        return roles;

role_response_model = api.model('Role_Response_Model', {
    'id': fields.String(description="The id of the role."),
    'name': fields.String(description="The name of the role."),
    'description': fields.String(description="The description of the role.")
})

@api.route('/')
class RoleListResource(Resource):
    @api.doc('list_roles')
    @api.marshal_with(role_response_model)
    @jwt_required()
    def get(self):
        '''List all roles'''
        return RoleService.get_list()