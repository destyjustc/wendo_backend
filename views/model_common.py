from database import db
from flask_restplus import Namespace, Resource, fields

class ModelCommon(db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

api = Namespace('model_super', description="Model super")

model_super_model = api.model('Model_Super_Model', {
    'id': fields.String(description="The identifier"),
    'created_on': fields.DateTime(description="The time that the record was created"),
    'updated_on': fields.DateTime(description="The time that the record was updated"),
})