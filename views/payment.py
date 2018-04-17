from database import db
from views.users import User
from views.courses import Course
from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields
import uuid
from views.model_common import ModelCommon, model_super_model
from views.model_super import ModelSuper
from flask_jwt import jwt_required

api = Namespace('payment', description="Payment related operations")

class Payment(ModelCommon, ModelSuper):
    __tablename__ = 'payments'

    user_id = db.Column(db.String(36), db.ForeignKey(User.id))
    course_id = db.Column(db.String(36), db.ForeignKey(Course.id))
    user = db.relationship(User, foreign_keys=user_id, post_update=True, uselist=False)
    course = db.relationship(Course, foreign_keys=course_id, post_update=True, uselist=False)
    payment = db.Column(db.Float(), default=0)

    def __init__(self, dict):
        ModelSuper.__init__(self, dict)

class PaymentService(object):
    @classmethod
    def get_by_user_id_and_course_id(cls, user_id, course_id):
        payments = Payment.query.filter_by(user_id=user_id).filter_by(course_id=course_id).all()
        return payments

    @classmethod
    def create(cls, data):
        id = uuid.uuid4()
        data['id'] = str(id)
        payment = Payment(data)
        db.session.add(payment)
        db.session.commit()
        return payment, 201


payment_request_model = api.model('Payment_Request', {
    'user_id': fields.String(required=True, description="The id of the user associated"),
    'course_id': fields.String(required=True, description="The id of the course associated"),
    'payment': fields.Float(required=True, description="The amount paid")
})

payment_response_model = api.inherit('Payment_Response', payment_request_model, model_super_model, {})

@api.route('/')
class PaymentListResource(Resource):
    @api.doc('create_payment')
    @api.expect(payment_request_model)
    @api.marshal_with(payment_response_model)
    @jwt_required()
    def post(self):
        '''Create a new payment record'''
        args = request.get_json()
        return PaymentService.create(args)

@api.route('/user/<user_id>/course/<course_id>')
@api.param('user_id', 'The user id')
@api.param('course_id', 'The course id')
class PaymentResource(Resource):
    @api.doc('get_by_user_id_and_course_id')
    @api.marshal_with(payment_response_model)
    @jwt_required()
    def get(self, user_id, course_id):
        '''Fetch payment records by user_id and course_id'''
        return PaymentService.get_by_user_id_and_course_id(user_id, course_id)