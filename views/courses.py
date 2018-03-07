from database import db
from flask import jsonify, request
from flask_jwt import jwt_required
from views.users import User
from views.schools import School
from flask_restplus import Namespace, Resource, fields
import uuid
from views.model_super import ModelSuper
from views.model_common import ModelCommon, model_super_model
from views.model_super import ModelSuper

api = Namespace('courses', description="Courses related operations")

class Course(ModelCommon, ModelSuper):
    __tablename__ = 'courses'

    name = db.Column(db.String(128))
    description = db.Column(db.String(256))
    fee = db.Column(db.Float())
    school_id = db.Column(db.String(36), db.ForeignKey(School.id))
    school = db.relationship(School, foreign_keys=school_id, post_update=True, uselist=False)

    def __init__(self, dict):
        ModelSuper.__init__(self, dict)

class CourseService(object):
    @classmethod
    def get(cls, school_id, id):
        course = Course.query.filter_by(id=id).filter_by(school_id=school_id).first()
        if course:
            return course
        api.abort(404)

    @classmethod
    def create(cls, school_id, data):
        id = uuid.uuid4()
        data['id'] = str(id)
        data['school_id'] = school_id
        course = Course(data)
        db.session.add(course)
        db.session.commit()
        return course, 201

    @classmethod
    def get_list(cls, school_id):
        courses = Course.query.filter_by(school_id=school_id).all()
        return courses

    @classmethod
    def update(cls, school_id, id, data):
        data.pop('id', None)
        data.pop('school_id', None)
        course = Course.query.filter_by(id=id).filter_by(school_id=school_id).first()
        if not course:
            api.abort(404, 'Course does not exist.')
        course.update(data)
        db.session.commit()
        return course

    @classmethod
    def delete(cls, school_id, id):
        course = Course.query.filter_by(id=id).filter_by(school_id=school_id).first()
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

course_response_model = api.inherit('Course_Response', course_request_model, model_super_model, {})

@api.route('/school/<school_id>')
@api.param('school_id', 'The school id')
class CourseListResource(Resource):
    @api.doc('list_courses')
    @api.marshal_list_with(course_response_model)
    def get(self, school_id):
        '''List all courses'''
        return CourseService.get_list(school_id)

    api.doc('create_new_course')
    @api.expect(course_request_model)
    @api.marshal_with(course_response_model)
    def post(self, school_id):
        '''Create a course'''
        args = request.get_json()
        return CourseService.create(school_id, args)

@api.route('/school/<school_id>/<id>')
@api.param('id', 'The course id')
class CourseResource(Resource):
    @api.doc('get_course')
    @api.marshal_with(course_response_model)
    def get(self, school_id, id):
        '''Fetch a course given its identifier'''
        return CourseService.get(school_id, id)

    @api.doc('update_course')
    @api.expect(course_request_model)
    @api.marshal_with(course_response_model)
    def put(self, school_id, id):
        '''Update a course given its identifier'''
        args = request.get_json()
        return CourseService.update(school_id, id, args)

    @api.doc('delete_course')
    @api.marshal_with(course_response_model)
    def delete(self, school_id, id):
        '''Remove a course given its identifier'''
        return CourseService.delete(school_id, id)