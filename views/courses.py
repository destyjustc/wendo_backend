from database import db
from flask import jsonify, request
from flask_jwt import jwt_required
from views.users import User
from flask_restplus import Namespace, Resource, fields

api = Namespace('courses', description="Courses related operations")

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String(256))
    fee = db.Column(db.Float())

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

course_api_model = api.model('Course', {
    'id': fields.String(required=True, description="The course identifier"),
    'name': fields.String(request=False, description="The course name"),
    'description': fields.String(request=False, description="The course description"),
    'fee': fields.Float(request=False, description="The course fee")
})

class CourseService(object):
    @classmethod
    def get(cls, id):
        course = Course.query.filter_by(id=id).first()
        if course:
            return course.as_dict()
        api.abort(404)

    @classmethod
    def create(cls, data):
        course = Course(data)
        db.session.add(course)
        db.session.commit()
        return course, 201

    @classmethod
    def get_list(cls):
        courses = Course.query.all()
        course_list = [course.as_dict() for course in courses]
        return course_list

    @classmethod
    def update(cls, id, data):
        course = Course.query.filter(id=id).first()
        try:
            course.update(data)
            db.session.commit()
            return course.as_dict()
        except Exception:
            api.abort(400)

    @classmethod
    def delete(cls, id):
        course = Course.query.filter(id=id).first()
        if course:
            db.session.delete(course)
            db.session.commit()
            return course.as_dict()
        api.abort(404)

@api.route('/')
class CourseListResource(Resource):
    @api.doc('list_courses')
    @api.marshal_list_with(course_api_model)
    def get(self):
        '''List all courses'''
        return CourseService.get_list()

    api.doc('create_new_course')
    @api.marshal_with(course_api_model)
    def post(self):
        '''Create a course'''
        args = request.get_json()
        return CourseService.create(args)

@api.route('/<id>')
@api.param('id', 'The course id')
class CourseResource(Resource):
    @api.doc('get_course')
    @api.marshal_with(course_api_model)
    def get(self, id):
        '''Fetch a course given its identifier'''
        return CourseService.get(id)

    @api.doc('update_course')
    @api.marshal_with(course_api_model)
    def put(self, id):
        '''Update a course given its identifier'''
        args = request.get_json()
        return CourseService.update(id, args)

    @api.doc('delete_course')
    @api.marshal_with(course_api_model)
    def put(self, id):
        '''Remove a course given its identifier'''
        return CourseService.delete(id)