from database import db
from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required

school = Blueprint('school', __name__)

class School(db.Model):
    __tablename__ = 'schools'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    describe = db.Column(db.String())

    def __init__(self, dict):
        for key in dict:
            setattr(self, key, dict[key])

    def __repr__(self):
        return '<id {}><name {}><description {}>'.format(self.id, self.name, self.description)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@school.route('/all', methods=['GET'])
def get_all_schools():
    schools = School.query.all()
    return jsonify([school.as_dict() for school in schools])

@school.route('/new', methods=['POST'])
def create_one_schools():
    args = request.get_json()
    school = School(args)
    ret = db.session.add(school)
    db.session.commit()
    print(ret)
    return jsonify(ret)