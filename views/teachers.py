from database import db
from flask import jsonify, request
from flask_jwt import jwt_required
from views.users import User
from flask_restplus import Namespace, Resource, fields

api = Namespace('teachers', description="Teachers related operations")

class Teacher(db.Model):
    __tablename__ = 'teachers'

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


teacher_api_model = api.model('Teacher', {
    'id': fields.String(required=True, description="The teacher identifier"),
    'user_id': fields.Integer(required=True, description="The id of the user associated")
})

class TeacherService(object):
    @classmethod
    def get(cls, id):
        teacher = Teacher.query.filter_by(id=id).first()
        if teacher:
            return teacher.as_dict()
        api.abort(404)

    @classmethod
    def create(cls, data):
        user = User(data)
        db.session.add(user)
        db.session.commit()
        teacher = Teacher({"user_id": user.id})
        db.session.add(teacher)
        db.session.commit()
        return teacher, 201

    @classmethod
    def get_list(cls):
        teachers = Teacher.query.all()
        teacher_list = [teacher.as_dict() for teacher in teachers]
        user_list = [teacher.user.as_dict() for teacher in teachers]
        for s, u in zip(teacher_list, user_list):
            s['user'] = u
        return teacher_list

@api.route('/')
class TeacherListResorce(Resource):
    @api.doc('list_teachers')
    @api.marshal_list_with(teacher_api_model)
    def get(self):
        '''List all Teachers'''
        return TeacherService.get_list()

    @api.doc('create_new_teacher')
    @api.marshal_with(teacher_api_model)
    def post(self):
        '''Create a teacher'''
        args = request.get_json()
        return TeacherService.create(args)

@api.route('/<id>')
@api.param('id', 'The teacher id')
class TeacherResource(Resource):
    @api.doc('get_teacher')
    @api.marshal_with(teacher_api_model)
    def get(self, id):
        '''Fetch a teacher given its identifier'''
        return TeacherService.get(id)