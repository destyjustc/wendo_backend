from database import db
from views.users import User, user_response_model, UserService
from views.courses import Course, course_response_model, CourseService
from views.roles import Role
from views.schools import School
from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields
import uuid
from views.model_common import ModelCommon, model_super_model
from views.model_super import ModelSuper

api = Namespace('course_users', description="Course and student relationship operations")

class CourseUser(ModelCommon, ModelSuper):
    __tablename__ = 'course_users'

    user_id = db.Column(db.String(36), db.ForeignKey(User.id))
    course_id = db.Column(db.String(36), db.ForeignKey(Course.id))
    user = db.relationship(User, foreign_keys=user_id, post_update=True, uselist=False)
    course = db.relationship(Course, foreign_keys=course_id, post_update=True, uselist=False)

    def __init__(self, dict):
        ModelSuper.__init__(self, dict)

class CourseUserService(object):
    @classmethod
    def get_by_course_id(cls, id):
        course_users = CourseUser.query.filter_by(course_id=id).all()
        for cu in course_users:
            cu = cu.as_dict()
            user_id = cu['user_id']
            user = UserService.get(user_id)
            cu['user'] = user
            course_id = cu['course_id']
            course = CourseService.get_by_course_id(course_id)
            cu['course'] = course
        return course_users

    @classmethod
    def get_by_user_id_and_schoold_id(cls, user_id, school_id):
        course_users = CourseUser.query.join(Course, Course.id == CourseUser.course_id)\
            .filter(CourseUser.user_id==user_id)\
            .filter(Course.school_id==school_id)\
            .all()
        for cu in course_users:
            cu = cu.as_dict()
            user_id = cu['user_id']
            user = UserService.get(user_id)
            cu['user'] = user
            course_id = cu['course_id']
            course = CourseService.get_by_course_id(course_id)
            cu['course'] = course
        return course_users

    @classmethod
    def create(cls, data):
        id = uuid.uuid4()
        data['id'] = str(id)
        course_user = CourseUser(data)
        db.session.add(course_user)
        db.session.commit()
        return course_user, 201


course_user_request_model = api.model('Course_User_Request', {
    'user_id': fields.String(required=True, description="The id of the user associated"),
    'course_id': fields.String(required=True, description="The id of the course associated")
})

course_user_response_model = api.inherit('Course_User_Response', course_user_request_model, model_super_model, {
    'user': fields.Nested(user_response_model),
    'course': fields.Nested(course_response_model)
})

@api.route('/')
class CourseUserListResource(Resource):
    @api.doc('create_course_users')
    @api.expect(course_user_request_model)
    @api.marshal_with(course_user_response_model)
    def post(self):
        '''Create a new course user record'''
        args = request.get_json()
        return CourseUserService.create(args)

@api.route('/course/<id>')
@api.param('id', 'The course id')
class CourseUserCourseResource(Resource):
    @api.doc('get_by_course_id')
    @api.marshal_list_with(course_user_response_model)
    def get(self, id):
        '''Fetch course user records given course id'''
        return CourseUserService.get_by_course_id(id)

@api.route('/school/<school_id>/user/<user_id>')
@api.param('school_id', 'The school id')
@api.param('user_id', 'The user id')
class CourseUserUserResource(Resource):
    @api.doc('get_by_user_id')
    @api.marshal_list_with(course_user_response_model)
    def get(self, school_id, user_id):
        '''Fetch course user records given user id'''
        print(school_id, user_id)
        return CourseUserService.get_by_user_id_and_schoold_id(user_id, school_id)

