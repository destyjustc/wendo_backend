from database import db
from flask import jsonify, request
from flask_jwt import jwt_required
from flask_restplus import Namespace, Resource, fields
import uuid
from views.model_common import ModelCommon, model_super_model
from views.model_super import ModelSuper

api = Namespace('schools', description="Schools related operations")

class School(ModelCommon, ModelSuper):
    __tablename__ = 'schools'

    name = db.Column(db.String())
    describe = db.Column(db.String())

    def __init__(self, dict):
        ModelSuper.__init__(self, dict)

class SchoolService(object):
    @classmethod
    def get(cls, id):
        school = School.query.filter_by(id=id).first()
        if school is not None:
            return school.as_dict()
        api.abort(404)

    @classmethod
    def get_list(cls):
        schools = School.query.all()
        school_list = [school.as_dict() for school in schools]
        return school_list

    @classmethod
    def create(cls, data):
        school = School.query.filter_by(name=data['name']).first()
        if school:
            api.abort(409, "Name already exists.")
        id = uuid.uuid4()
        data['id'] = str(id)
        school = School(data)
        db.session.add(school)
        db.session.commit()
        return school.as_dict()

    @classmethod
    def update(cls, id, data):
        data.pop('id', None)
        school = School.query.filter_by(id=id).first()
        if not school:
            api.abort(404, "School does not exist.")
        school.update(data)
        db.session.commit()
        return school

school_request_model = api.model('School_Request', {
    'name': fields.String(required=True, description="The school name"),
    'describe': fields.String(required=False, description="The school description"),
})

school_response_model = api.inherit('School_Response', school_request_model, model_super_model, {})

@api.route('/')
class SchoolListResource(Resource):
    @api.doc('list_schools')
    @api.marshal_list_with(school_response_model)
    @jwt_required()
    def get(self):
        '''List all schools'''
        return SchoolService.get_list()

    @api.doc('create_new_school')
    @api.expect(school_request_model)
    @api.marshal_with(school_response_model)
    @jwt_required()
    def post(self):
        '''Create a school'''
        args = request.get_json()
        return SchoolService.create(args)

@api.route('/<id>')
@api.param('id', 'The school id')
class StudentResource(Resource):
    @api.doc('get_school')
    @api.marshal_with(school_response_model)
    @jwt_required()
    def get(self, id):
        '''Fetch a school given its identifier'''
        return SchoolService.get(id)

    @api.doc('update_school')
    @api.expect(school_request_model)
    @api.marshal_with(school_response_model)
    @jwt_required()
    def put(self, id):
        '''Fetch a school given its identifier'''
        args = request.get_json()
        return SchoolService.update(id, args)