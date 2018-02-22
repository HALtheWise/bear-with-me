from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(128))
    active = db.Column(db.Boolean())
    last_call = db.Column(db.DateTime())

    def __repr__(self):
        # <User …> is Python's convention for unreadable representations (reprs
        # that can't be entered into the source or the interpreter.)
        return '<User {} ({})>'.format(self.phone, 'active' if self.active else 'inactive')

        # Or use this to get the module name:
        #   '<{} {} ({})>'.format(self.__class__.__name__, sself.phone, 'active' if self.active else 'inactive')

        # Python 3.6 also (finally) lets you say:
        #   f'[User {self.phone} ({'active' if self.active else 'inactive'})]'
        # Available in ECMAScript with suitable babel as:
        #   `[User #{self.phone} (#{self.active ? 'active' : 'inactive'})]`
