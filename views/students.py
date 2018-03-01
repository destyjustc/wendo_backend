from database import db
from flask import jsonify, request
from flask_jwt import jwt_required
from views.users import User, user_api_model, UserService
from flask_restplus import Namespace, Resource, fields
import uuid

api = Namespace('students', description="Students related operations")

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey(User.id))
    user = db.relationship(User, foreign_keys=user_id, post_update=True, uselist=False)

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

class StudentService(object):
    @classmethod
    def get(cls, id):
        student = Student.query.filter_by(id=id).first()
        if student is not None:
            return student
        api.abort(404)

    @classmethod
    def create(cls, data):
        #TODO: check email or phone number exists
        tmp_user = User.query.filter(User.username == data['username']).first()
        if tmp_user:
            api.abort(409, "Username already exists.")
        id = uuid.uuid4()
        data['id'] = str(id)
        user = User(data)
        db.session.add(user)
        db.session.commit()
        id = uuid.uuid4()
        student = Student({"user_id": user.id, "id": str(id)})
        db.session.add(student)
        db.session.commit()
        return student, 201

    @classmethod
    def get_list(cls):
        students = Student.query.all()
        return students

    @classmethod
    def update(cls, id, data):
        data.pop('username', None)
        data.pop('user_id', None)
        data.pop('id', None)
        student = Student.query.filter_by(id=id).first()
        if not student:
            api.abort(404, 'Student does not exist')
        UserService.update(student.user_id, data)
        student.update(data)
        db.session.commit()
        return student

student_api_model = api.model('Student_Response', {
    'id': fields.String(description="The student identifier"),
    'user_id': fields.String(description="The id of the user associated"),
    'user': fields.Nested(user_api_model)
})

student_request_model = api.model('Student_Request', {
    'username': fields.String(required=True, description="The username"),
    'password': fields.String(required=True, description="The password"),
    'firstname': fields.String(description="The first name"),
    'lastname': fields.String(description="The last name"),
    'email': fields.String(description="The email"),
    'phone': fields.String(description="The phone number"),
})

@api.route('/')
class StudentListResource(Resource):
    @api.doc('list_students')
    @api.marshal_list_with(student_api_model)
    def get(self):
        '''List all students'''
        return StudentService.get_list()

    @api.doc('create_new_student')
    @api.expect(student_request_model)
    @api.marshal_with(student_api_model)
    def post(self):
        '''Create a student'''
        args = request.get_json()
        return StudentService.create(args)

@api.route('/<id>')
@api.param('id', 'The student id')
class StudentResource(Resource):
    @api.doc('get_student')
    @api.marshal_with(student_api_model)
    def get(self, id):
        '''Fetch a student given its identifier'''
        return StudentService.get(id)

    @api.doc('update_student')
    @api.marshal_with(student_api_model)
    @api.expect(student_request_model)
    def put(self, id):
        '''Update a student given its identifier and data'''
        args = request.get_json()
        return StudentService.update(id, args)
