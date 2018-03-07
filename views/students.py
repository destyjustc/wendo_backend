from database import db
from flask import jsonify, request
from flask_jwt import jwt_required
from views.users import User, user_response_model, UserService
from views.user_roles import UserRole
from views.roles import Role
from views.schools import School
from flask_restplus import Namespace, Resource, fields
import uuid
from views.model_super import ModelSuper

api = Namespace('students', description="Students related operations")

class Student(ModelSuper):
    def __init__(self, dict):
        ModelSuper.__init__(self, dict)

class StudentService(object):
    @classmethod
    def get(cls, school_id, id):
        student = User.query.join(UserRole, User.id == UserRole.user_id)\
            .join(Role, UserRole.role_id==Role.id)\
            .filter(User.id==id)\
            .filter(Role.name=='student')\
            .filter(UserRole.school_id==school_id)\
            .first()
        if student:
            return student
        api.abort(404)

    @classmethod
    def create(cls, data, school_id):
        user = UserService.create(data)
        role_id = Role.query.filter_by(name='student').first().id
        id = uuid.uuid4()
        obj = {
            'id': id,
            'user_id': user.id,
            'role_id': role_id,
            'school_id': school_id
        }
        user_role = UserRole(obj)
        db.session.add(user_role)
        db.session.commit()
        return user, 201

    @classmethod
    def get_list(cls, school_id):
        students = User.query.join(UserRole, User.id==UserRole.user_id)\
            .join(Role, UserRole.role_id==Role.id)\
            .filter(UserRole.school_id==school_id)\
            .all()
        return students

    @classmethod
    def update(cls, school_id, id, data):
        data.pop('username', None)
        data.pop('user_id', None)
        data.pop('id', None)
        student = User.query.join(UserRole, User.id==UserRole.user_id)\
            .filter(UserRole.school_id==school_id)\
            .filter(User.id==id)\
            .first()
        if not student:
            api.abort(404, 'Student does not exist')
        UserService.update(student.id, data)
        return student

student_request_model = api.model('Student_Request', {
    'username': fields.String(required=True, description="The username"),
    'password': fields.String(required=True, description="The password"),
    'firstname': fields.String(description="The first name"),
    'lastname': fields.String(description="The last name"),
    'email': fields.String(description="The email"),
    'phone': fields.String(description="The phone number"),
})

student_api_model = api.inherit('Student_Response', student_request_model, {
    'id': fields.String(description="The student identifier")
})

@api.route('/school/<school_id>')
@api.param('school_id', 'The school id')
class StudentListResource(Resource):
    @api.doc('list_students')
    @api.marshal_list_with(student_api_model)
    def get(self, school_id):
        '''List all students'''
        return StudentService.get_list(school_id)

    @api.doc('create_new_student')
    @api.expect(student_request_model)
    @api.marshal_with(student_api_model)
    def post(self, school_id):
        '''Create a student'''
        args = request.get_json()
        return StudentService.create(args, school_id)

@api.route('/school/<school_id>/<id>')
@api.param('id', 'The student id')
class StudentResource(Resource):
    @api.doc('get_student')
    @api.marshal_with(student_api_model)
    def get(self, school_id, id):
        '''Fetch a student given its identifier'''
        return StudentService.get(school_id, id)

    @api.doc('update_student')
    @api.marshal_with(student_api_model)
    @api.expect(student_request_model)
    def put(self, school_id, id):
        '''Update a student given its identifier and data'''
        args = request.get_json()
        return StudentService.update(school_id, id, args)
