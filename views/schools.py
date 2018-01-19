from database import db
from flask import jsonify, request
from flask_jwt import jwt_required
from flask_restplus import Namespace, Resource, fields

api = Namespace('schools', description="Schools related operations")

class School(db.Model):
    __tablename__ = 'schools'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    describe = db.Column(db.String())

    def __init__(self, dict):
        for key in dict:
            setattr(self, key, dict[key])

    def __repr__(self):
        return '<id {}><name {}><description {}>'.format(self.id, self.name, self.description)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

school_api_model = api.model('School', {
    'id': fields.Integer(required=True, description="The school identifier"),
    'name': fields.Integer(required=True, description="The school name"),
    'describe': fields.Integer(required=False, description="The school description"),
})

@api.route('/')
class SchoolListResource(Resource):
    @api.doc('list_schools')
    @api.marshal_list_with(school_api_model)
    def get(self):
        '''List all schools'''
        schools = School.query.all()
        school_list = [school.as_dict() for school in schools]
        return jsonify(school_list)

    @api.doc('create_new_school')
    @api.marshal_with(school_api_model)
    def post(self):
        '''Create a school'''
        args = request.get_json()
        school = School(args)
        db.session.add(school)
        db.session.commit()
        return jsonify(school.as_dict())

@api.route('/<id>')
@api.param('id', 'The school id')
class StudentResource(Resource):
    @api.doc('get_school')
    @api.marshal_with(school_api_model)
    def get(self, id):
        '''Fetch a school given its identifier'''
        school = School.query.filter(School.id == id).first()
        if school is not None:
            return school.as_dict()
        api.abort(404)