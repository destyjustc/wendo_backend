from database import db
from flask_restplus import Namespace, Resource, fields

api = Namespace('role', description="Role related operations")

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(128))

    def __init__(self, dict):
        for key in dict:
            setattr(self, key, dict[key])

    def __repr__(self):
        return '<id {}><name {}><description {}>'.format(self.id, self.name, self.description)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

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
    def get(self):
        '''List all roles'''
        return RoleService.get_list()