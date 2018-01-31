from database import db
from flask import jsonify, request
from flask_jwt import jwt_required
from views.users import User
from flask_restplus import Namespace, Resource, fields
from sqlalchemy.dialects.postgresql import UUID

api = Namespace('students', description="Students related operations")

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.String(32), primary_key=True)
    user_id = db.Column(db.String(32), db.ForeignKey(User.id))
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
    'user_id': fields.Integer(required=True, description="The id of the user associated")
})

class StudentService(object):
    @classmethod
    def get(cls, id):
        student = Student.query.filter_by(id=id).first()
        if student is not None:
            return student.as_dict()
        api.abort(404)

    @classmethod
    def create(cls, data):
        user = User(data)
        db.session.add(user)
        db.session.commit()
        student = Student({"user_id": user.id})
        db.session.add(student)
        db.session.commit()
        return student, 201

    @classmethod
    def get_list(cls):
        students = Student.query.all()
        for s in students:
            print(s.user)
        student_list = [student.as_dict() for student in students]
        user_list = [student.user.as_dict() for student in students]
        for s, u in zip(student_list, user_list):
            s['user'] = u
        return student_list


@api.route('/')
class StudentListResource(Resource):
    @api.doc('list_students')
    @api.marshal_list_with(student_api_model)
    def get(self):
        '''List all students'''
        return StudentService.get_list()

    @api.doc('create_new_student')
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

    # def put(self, id):
    #     args = request.get_json()
    #     student = Student.query.filter(Student.id == id).first()
    #     student.update(args)
    #     print(student)