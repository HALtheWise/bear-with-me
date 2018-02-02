from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(128))
    active = db.Column(db.Boolean())
    last_call = db.Column(db.DateTime())

    def __repr__(self):
        return '<User {} ({})>'.format(self.phone, 'active' if self.active else 'inactive')
