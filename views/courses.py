from database import db
from flask import jsonify, request
from flask_jwt import jwt_required
from views.users import User
from views.schools import School
from flask_restplus import Namespace, Resource, fields
import uuid

api = Namespace('courses', description="Courses related operations")

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String(256))
    fee = db.Column(db.Float())
    school_id = db.Column(db.String(36), db.ForeignKey(School.id))
    school = db.relationship(School, foreign_keys=school_id, post_update=True, uselist=False)

    def __init__(self, dict):
        for key in dict:
            setattr(self, key, dict[key])

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def update(self, dict):
        for i in dict:
            setattr(self, i, dict[i])

class CourseService(object):
    @classmethod
    def get(cls, id):
        course = Course.query.filter_by(id=id).first()
        if course:
            return course
        api.abort(404)

    @classmethod
    def create(cls, data):
        id = uuid.uuid4()
        data['id'] = str(id)
        course = Course(data)
        db.session.add(course)
        db.session.commit()
        return course, 201

    @classmethod
    def get_list(cls):
        courses = Course.query.all()
        return courses

    @classmethod
    def update(cls, id, data):
        data.pop('id', None)
        data.pop('school_id', None)
        course = Course.query.filter_by(id=id).first()
        if not course:
            api.abort(404, 'Course does not exist.')
        course.update(data)
        db.session.commit()
        return course

    @classmethod
    def delete(cls, id):
        course = Course.query.filter_by(id=id).first()
        if course:
            db.session.delete(course)
            db.session.commit()
            return course
        api.abort(404)

course_request_model = api.model('Course_Request', {
    'name': fields.String(request=False, description="The course name"),
    'description': fields.String(request=False, description="The course description"),
    'fee': fields.Float(request=False, description="The course fee"),
    'school_id': fields.String(description="The school id")
})

course_response_model = api.inherit('Course_Response', course_request_model, {
    'id': fields.String(description="The course identifier")
})

@api.route('/')
class CourseListResource(Resource):
    @api.doc('list_courses')
    @api.marshal_list_with(course_response_model)
    def get(self):
        '''List all courses'''
        return CourseService.get_list()

    api.doc('create_new_course')
    @api.expect(course_request_model)
    @api.marshal_with(course_response_model)
    def post(self):
        '''Create a course'''
        args = request.get_json()
        return CourseService.create(args)

@api.route('/<id>')
@api.param('id', 'The course id')
class CourseResource(Resource):
    @api.doc('get_course')
    @api.marshal_with(course_response_model)
    def get(self, id):
        '''Fetch a course given its identifier'''
        return CourseService.get(id)

    @api.doc('update_course')
    @api.expect(course_request_model)
    @api.marshal_with(course_response_model)
    def put(self, id):
        '''Update a course given its identifier'''
        args = request.get_json()
        return CourseService.update(id, args)

    @api.doc('delete_course')
    @api.marshal_with(course_response_model)
    def delete(self, id):
        '''Remove a course given its identifier'''
        return CourseService.delete(id)