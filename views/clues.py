from database import db
from views.users import User, user_response_model, UserService
from views.schools import School
from views.user_roles import UserRole
from views.clue_groups import ClueGroup, clue_gourp_response_model, ClueGroupService
from flask import jsonify, request
from flask_jwt import jwt_required
from flask_restplus import Namespace, Resource, fields
import uuid
from views.model_common import ModelCommon, model_super_model
from views.model_super import ModelSuper

api = Namespace('clue', description='Clues related operations')

class Clue(ModelCommon, ModelSuper):
    __tablename__ = 'clues'

    clue_group_id = db.Column(db.String(36), db.ForeignKey(ClueGroup.id))
    student_id = db.Column(db.String(36), db.ForeignKey(User.id))
    content = db.Column(db.String(256))
    deadline = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    clue_group = db.relationship(ClueGroup, foreign_keys=clue_group_id, post_update=True, uselist=False)
    student = db.relationship(User, foreign_keys=student_id, post_update=True, uselist=False)

    def __init__(self, dict):
        ModelSuper.__init__(self, dict)

class ClueService(object):
    @classmethod
    def create(cls, data):
        id = uuid.uuid4()
        data['id'] = str(id)
        clue = Clue(data)
        db.session.add(clue)
        db.session.commit()
        clue = clue.as_dict()
        clue['clue_group'] = ClueService.get_by_id(data['clue_group_id'])
        clue['student'] = UserService.get(data['student_id'])
        return clue, 201

    @classmethod
    def get(cls, id):
        clue = Clue.query.filter_by(id=id).first()
        if clue:
            clue = clue.as_dict()
            clue['clue_group'] = ClueService.get_by_id(clue['clue_group_id'])
            clue['student'] = UserService.get(clue['student_id'])
            return clue

    @classmethod
    def get_by_clue_group_id(cls, clue_group_id):
        clues = Clue.query.filter_by(clue_group_id=clue_group_id).all()
        for clue in clues:
            clue = clue.as_dict()
            clue['clue_group'] = ClueService.get_by_id(clue['clue_group_id'])
            clue['student'] = UserService.get(clue['student_id'])
        return clues

    pass

clue_request_model = api.model('Clue_Request', {
    'clue_group_id': fields.String(required=True, description="The id of the clue group"),
    'student_id': fields.String(required=False, description="The id of the target student"),
    'content': fields.String(required=True, description="The content"),
    'deadline': fields.DateTime(description="The deadline"),
    'completed_at': fields.DateTime(description="The complete time"),
})

clue_response_model = api.inherit('Clue_response', clue_request_model, model_super_model, {
    'clue_group': fields.Nested(clue_gourp_response_model),
    'student': fields.Nested(user_response_model),
})

@api.route('/')
class ClueListResource(Resource):
    @api.doc('create_clue')
    @api.expect(clue_request_model)
    @api.marshal_with(clue_response_model)
    def post(self):
        '''Create a new clue'''
        args = request.get_json()
        return ClueService.create(args)

@api.route('/<id>')
@api.param('id', 'The clue id')
class ClueResource(Resource):
    @api.doc('get_by_clue_id')
    @api.marshal_with(clue_response_model)
    def get(self, id):
        '''Fetch clue given id'''
        return ClueService.get(id)

@api.route('/clue_group/<clue_group_id>')
@api.param('clue_group_id', 'The clue group id')
class ClueClueGroupResource(Resource):
    @api.doc('get_by_clue_group_id')
    @api.marshal_list_with(clue_response_model)
    def get(self, clue_group_id):
        '''Fetch clues given clue group id'''
        return ClueService.get_by_clue_group_id(clue_group_id)