from database import db
from flask import jsonify, request
from flask_jwt import jwt_required
from flask_restplus import Namespace, Resource, fields
# from uuid import UUID

api = Namespace('schools', description="Schools related operations")

class School(db.Model):
    __tablename__ = 'schools'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String())
    describe = db.Column(db.String())

    def __init__(self, dict):
        for key in dict:
            setattr(self, key, dict[key])

    def __repr__(self):
        return '<id {}><name {}><description {}>'.format(self.id, self.name, self.description)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class SchoolService(object):
    @classmethod
    def get(cls, id):
        school = School.query.filter(id=id).first()
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
        school = School(data)
        db.session.add(school)
        db.session.commit()
        return school.as_dict()

school_api_model = api.model('School', {
    'id': fields.String(required=True, description="The school identifier"),
    'name': fields.Integer(required=True, description="The school name"),
    'describe': fields.Integer(required=False, description="The school description"),
})

@api.route('/')
class SchoolListResource(Resource):
    @api.doc('list_schools')
    @api.marshal_list_with(school_api_model)
    def get(self):
        '''List all schools'''
        return SchoolService.get_list()

    @api.doc('create_new_school')
    @api.marshal_with(school_api_model)
    def post(self):
        '''Create a school'''
        args = request.get_json()
        return SchoolService.create(args)

@api.route('/<id>')
@api.param('id', 'The school id')
class StudentResource(Resource):
    @api.doc('get_school')
    @api.marshal_with(school_api_model)
    def get(self, id):
        '''Fetch a school given its identifier'''
        return SchoolService.get(id)