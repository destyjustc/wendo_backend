from database import db
from flask import jsonify, request
from flask_jwt import jwt_required
from views.users import User, user_api_model
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

student_api_model = api.model('Student', {
    'id': fields.String(required=True, description="The student identifier"),
    'user_id': fields.String(required=True, description="The id of the user associated"),
    'user': fields.Nested(user_api_model)
})

student_request_model = api.inherit('Resource', {
    'username': fields.String,
    'password': fields.String,
    'firstname': fields.String,
    'lastname': fields.String,
    'email': fields.String,
    'phone': fields.String,
})

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
            api.abort(400, "Username already exists.")
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


@api.route('/')
class StudentListResource(Resource):
    @api.doc('list_students')
    @api.marshal_list_with(student_api_model)
    def get(self):
        '''List all students'''
        return StudentService.get_list()

    @api.doc('create_new_student')
    @api.marshal_with(student_api_model)
    @api.expect(student_request_model)
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