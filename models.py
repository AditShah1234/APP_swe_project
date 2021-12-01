from app import db
from sqlalchemy.dialects.postgresql import JSON


class User(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    # url = db.Column(db.String())
    # result_all = db.Column(JSON)
    # result_no_stop_words = db.Column(JSON)

    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<id {}>'.format(self.id)