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
from views.model_common import model_super_model

api = Namespace('teacher', description="Teachers related operations")

class Teacher(ModelSuper):
    def __init__(self, dict):
        ModelSuper.__init__(self, dict)

class TeacherService(object):
    @classmethod
    def get(cls, school_id, id):
        teacher = User.query.join(UserRole, User.id == UserRole.user_id) \
            .join(Role, UserRole.role_id == Role.id) \
            .filter(User.id == id) \
            .filter(Role.name == 'staff') \
            .filter(UserRole.school_id == school_id) \
            .first()
        if teacher:
            return teacher
        api.abort(404)

    @classmethod
    def create(cls, data, school_id):
        user = UserService.create(data)
        role_id = Role.query.filter_by(name='staff').first().id
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
        teachers = User.query.join(UserRole, User.id == UserRole.user_id) \
            .join(Role, UserRole.role_id == Role.id) \
            .filter(UserRole.school_id == school_id) \
            .filter(Role.name == 'staff') \
            .all()
        return teachers

    @classmethod
    def update(cls, school_id, id, data):
        data.pop('username', None)
        data.pop('user_id', None)
        data.pop('id', None)
        teacher = User.query.join(UserRole, User.id == UserRole.user_id) \
            .filter(UserRole.school_id == school_id) \
            .filter(User.id == id) \
            .first()
        if not teacher:
            api.abort(404, 'Teacher does not exist')
        UserService.update(teacher.id, data)
        return teacher

teacher_request_model = api.model('Teacher_Request', {
    'username': fields.String(required=True, description="The username"),
    'password': fields.String(required=True, description="The password"),
    'firstname': fields.String(description="The first name"),
    'lastname': fields.String(description="The last name"),
    'email': fields.String(description="The email"),
    'phone': fields.String(description="The phone number"),
})

teacher_api_model = api.inherit('Teacher_Response', teacher_request_model, model_super_model, {})

@api.route('/school/<school_id>')
@api.param('school_id', 'The school id')
class TeacherListResource(Resource):
    @api.doc('list_teachers')
    @api.marshal_list_with(teacher_api_model)
    def get(self, school_id):
        '''List all teachers'''
        return TeacherService.get_list(school_id)

    @api.doc('create_new_teacher')
    @api.expect(teacher_request_model)
    @api.marshal_with(teacher_api_model)
    def post(self, school_id):
        '''Create a teacher'''
        args = request.get_json()
        return TeacherService.create(args, school_id)

@api.route('/school/<school_id>/<id>')
@api.param('school_id', 'The school id')
@api.param('id', 'The teacher id')
class TeacherResource(Resource):
    @api.doc('get_teacher')
    @api.marshal_with(teacher_api_model)
    def get(self, school_id, id):
        '''Fetch a teacher given its identifier'''
        return TeacherService.get(school_id, id)

    @api.doc('update_teacher')
    @api.marshal_with(teacher_api_model)
    @api.expect(teacher_request_model)
    def put(self, school_id, id):
        '''Update a teacher given its identifier and data'''
        args = request.get_json()
        return TeacherService.update(school_id, id, args)