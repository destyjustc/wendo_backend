from database import db
from views.users import User, user_response_model, UserService
from views.schools import School
from views.user_roles import UserRole
from flask import jsonify, request
from flask_jwt import jwt_required
from flask_restplus import Namespace, Resource, fields
import uuid
from views.model_common import ModelCommon, model_super_model
from views.model_super import ModelSuper

api = Namespace('clue_groups', description="Clue Groups related operations")

class ClueGroup(ModelCommon, ModelSuper):
    __tablename__ = 'clue_groups'

    created_by = db.Column(db.String(36), db.ForeignKey(User.id))
    assigned_to = db.Column(db.String(36), db.ForeignKey(User.id))
    created = db.relationship(User, foreign_keys=created_by, post_update=True, uselist=False)
    assigned = db.relationship(User, foreign_keys=assigned_to, post_update=True, uselist=False)

    def __init__(self, dict):
        ModelSuper.__init__(self, dict)

class ClueGroupService(object):
    @classmethod
    def create(cls, data):
        id = uuid.uuid4()
        data['id'] = str(id)
        clue_group = ClueGroup(data)
        db.session.add(clue_group)
        db.session.commit()
        clue_group = clue_group.as_dict()
        assigned = UserService.get(clue_group['assigned_to'])
        clue_group['assigned'] = assigned
        created = UserService.get(clue_group['created_by'])
        clue_group['created'] = created
        return clue_group, 201

    @classmethod
    def get_by_id(cls, id):
        clue_group = ClueGroup.query.filter_by(id=id).first()
        if clue_group:
            clue_group = clue_group.as_dict()
            assigned = UserService.get(clue_group['assigned_to'])
            clue_group['assigned'] = assigned
            created = UserService.get(clue_group['created_by'])
            clue_group['created'] = created
            return clue_group
        api.abort(404)

    @classmethod
    def get_by_school_id(cls, school_id):
        clue_groups = ClueGroup.query.join(UserRole, UserRole.user_id == ClueGroup.created_by)\
            .filter(UserRole.school_id==school_id)\
            .all()
        for clue_group in clue_groups:
            clue_group = clue_group.as_dict()
            assigned = UserService.get(clue_group['assigned_to'])
            clue_group['assigned'] = assigned
            created = UserService.get(clue_group['created_by'])
            clue_group['created'] = created
        return clue_groups
    pass


clue_gourp_request_model = api.model('Clue_Group_Request', {
    'created_by': fields.String(required=True, description="The id of the user created this clue group"),
    'assigned_to': fields.String(required=True, description="The id of the user this clue group was assigned to"),
})

clue_gourp_response_model = api.inherit('Clue_Group_Response', clue_gourp_request_model, model_super_model, {
    'created': fields.Nested(user_response_model),
    'assigned': fields.Nested(user_response_model),
})

@api.route('/')
class ClueGroupListResource(Resource):
    @api.doc('create_clue_group')
    @api.expect(clue_gourp_request_model)
    @api.marshal_with(clue_gourp_response_model)
    def post(self):
        '''Create a new clue group'''
        args = request.get_json()
        return ClueGroupService.create(args)

@api.route('/<id>')
@api.param('id', 'The clue group id')
class ClueGroupResource(Resource):
    @api.doc('get_by_clue_group_id')
    @api.marshal_with(clue_gourp_response_model)
    def get(self, id):
        '''Fetch clue group given id'''
        return ClueGroupService.get_by_id(id)

@api.route('/school/<school_id>')
@api.param('school_id', 'The school id')
class ClueGroupSchoolListResource(Resource):
    @api.doc('get_by_school_id')
    @api.marshal_list_with(clue_gourp_response_model)
    def get(self, school_id):
        '''Fetch clue groups given school id'''
        return ClueGroupService.get_by_school_id(school_id)
