from database import db
from views.users import User
from views.courses import Course
from views.roles import Role
from views.schools import School
from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields
import uuid

api = Namespace('course_users', description="Course and student relationship operations")

class CourseUser(db.Model):
    __tablename__ = 'course_users'

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey(User.id))
    course_id = db.Column(db.String(36), db.ForeignKey(Course.id))
    user = db.relationship(User, foreign_keys=user_id, post_update=True, uselist=False)
    course = db.relationship(Course, foreign_keys=course_id, post_update=True, uselist=False)

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

course_user_api_model = api.model('CourseUser', {
    'id': fields.String(required=True, description="The course_user record identifier"),
    'user_id': fields.String(required=True, description="The id of the user associated"),
    'course_id': fields.String(required=True, description="The id of the course associated")
})

course_user_post_model = api.model('CourseUser', {
    'user_id': fields.String(required=True, description="The id of the user associated"),
    'course_id': fields.String(required=True, description="The id of the course associated")
})

class CourseUserService(object):
    @classmethod
    def get_by_course_id(cls, id):
        course_users = CourseUser.query.filter_by(CourseUser.course_id == id).all()
        return [course_user.as_dict() for course_user in course_users]

    @classmethod
    def get_by_user_id_and_schoold_id(cls, user_id, school_id):
        course_users = CourseUser.query.join(Course, Course.id == CourseUser.course_id).filter(CourseUser.user_id==user_id).filter(Course.school_id==school_id).all()
        return [course_user.as_dict() for course_user in course_users]

    @classmethod
    def create(cls, data):
        id = uuid.uuid4()
        data['id'] = str(id)
        course_user = CourseUser(data)
        db.session.add(course_user)
        db.session.commit()
        return course_user, 201

@api.route('/')
class CourseUserListResource(Resource):
    @api.doc('list_course_users')
    @api.marshal_with(course_user_post_model)
    def post(self):
        '''Create a new course user record'''
        args = request.get_json()
        return CourseUserService.create(args)

@api.route('/course/<id>')
@api.param('id', 'The course id')
class CourseUserCourseResource(Resource):
    @api.doc('get_by_course_id')
    @api.marshal_with(course_user_api_model)
    def get(self, id):
        '''Fetch course user records given course id'''
        return CourseUserService.get_by_course_id(id)

@api.route('/user/<user_id>/school/<school_id>')
@api.param('id', 'The user id')
class CourseUserUserResource(Resource):
    @api.doc('get_by_user_id')
    @api.marshal_with(course_user_api_model)
    def get(self, user_id, school_id):
        '''Fetch course user records given user id'''
        return CourseUserService.get_by_user_id_and_schoold_id(user_id, school_id)
