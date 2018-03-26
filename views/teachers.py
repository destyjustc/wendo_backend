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


# from database import db
# from flask import jsonify, request
# from flask_jwt import jwt_required
# from views.users import User, UserService, user_response_model
# from flask_restplus import Namespace, Resource, fields
# import uuid
#
# api = Namespace('teachers', description="Teachers related operations")
#
# class Teacher(db.Model):
#     __tablename__ = 'teachers'
#
#     id = db.Column(db.String(36), primary_key=True)
#     user_id = db.Column(db.String(36), db.ForeignKey(User.id))
#     user = db.relationship(User, foreign_keys=user_id, post_update=True, uselist=False)
#
#     def __init__(self, dict):
#         for key in dict:
#             setattr(self, key, dict[key])
#
#     def __repr__(self):
#         return '<id {}>'.format(self.id)
#
#     def as_dict(self):
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns}
#
#     def update(self, dict):
#         for i in dict:
#             setattr(self, i, dict[i])
#
# class TeacherService(object):
#     @classmethod
#     def get(cls, id):
#         teacher = Teacher.query.filter_by(id=id).first()
#         if teacher is not None:
#             return teacher
#         api.abort(404)
#
#     @classmethod
#     def create(cls, data):
#         #TODO: check email or phone number exists
#         tmp_user = User.query.filter(User.username == data['username']).first()
#         if tmp_user:
#             api.abort(409, "Username already exists.")
#         id = uuid.uuid4()
#         data['id'] = str(id)
#         user = User(data)
#         db.session.add(user)
#         db.session.commit()
#         id = uuid.uuid4()
#         teacher = Teacher({"user_id": user.id, "id": str(id)})
#         db.session.add(teacher)
#         db.session.commit()
#         return teacher, 201
#
#     @classmethod
#     def get_list(cls):
#         teachers = Teacher.query.all()
#         return teachers
#
#     @classmethod
#     def update(cls, id, data):
#         data.pop('username', None)
#         data.pop('user_id', None)
#         data.pop('id', None)
#         teacher = Teacher.query.filter_by(id=id).first()
#         if not teacher:
#             api.abort(404, 'Teacher does not exist')
#         UserService.update(teacher.user_id, data)
#         teacher.update(data)
#         db.session.commit()
#         return teacher
#
# teacher_response_model = api.model('Teacher_Response', {
#     'id': fields.String(description="The teacher identifier"),
#     'user_id': fields.String(description="The id of the user associated"),
#     'user': fields.Nested(user_response_model)
# })
#
# teacher_request_model = api.model('Teacher_Request', {
#     'username': fields.String(required=True, description="The username"),
#     'password': fields.String(required=True, description="The password"),
#     'firstname': fields.String(description="The first name"),
#     'lastname': fields.String(description="The last name"),
#     'email': fields.String(description="The email"),
#     'phone': fields.String(description="The phone number"),
# })
#
# @api.route('/')
# class TeacherListResorce(Resource):
#     @api.doc('list_teachers')
#     @api.marshal_list_with(teacher_api_model)
#     def get(self):
#         '''List all Teachers'''
#         return TeacherService.get_list()
#
#     @api.doc('create_new_teacher')
#     @api.marshal_with(teacher_api_model)
#     def post(self):
#         '''Create a teacher'''
#         args = request.get_json()
#         return TeacherService.create(args)
#
# @api.route('/<id>')
# @api.param('id', 'The teacher id')
# class TeacherResource(Resource):
#     @api.doc('get_teacher')
#     @api.marshal_with(teacher_api_model)
#     def get(self, id):
#         '''Fetch a teacher given its identifier'''
#         return TeacherService.get(id)