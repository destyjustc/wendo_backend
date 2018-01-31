from database import db

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(128))

    def __init__(self, dict):
        for key in dict:
            setattr(self, key, dict[key])

    def __repr__(self):
        return '<id {}><name {}><description {}>'.format(self.id, self.name, self.description)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}