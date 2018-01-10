from database import db
from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required
from views.users import User

student = Blueprint('student', __name__)

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User, foreign_keys=user_id, post_update=True, uselist=False)

    def __init__(self, dict):
        for key in dict:
            setattr(self, key, dict[key])

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@student.route('/all', methods=['GET'])
def get_all_students():
    students = Student.query.all()
    for s in students:
        print(s.user)
    student_list = [student.as_dict() for student in students]
    user_list = [student.user.as_dict() for student in students]
    for s, u in zip(student_list, user_list):
        s['user'] = u
    return jsonify(student_list)

@student.route('/new', methods=['POST'])
def create_one_schools():
    args = request.get_json()
    user = User(args)
    db.session.add(user)
    db.session.commit()
    student = Student({"user_id":user.id})
    db.session.add(student)
    db.session.commit()
    return jsonify(user.as_dict())