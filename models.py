from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Feedback(db.Model):

    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    username = db.Column(db.Text, db.ForeignKey('users.username',ondelete='CASCADE'))

    user = db.relationship('User', backref="feedbacks")


class User(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.Text, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text)
    firstname = db.Column(db.Text)
    lastname = db.Column(db.Text)

    @classmethod
    def register(cls,username,pwd,email,firstname,lastname):
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")
        return cls(username=username,password=hashed_utf8,email=email,firstname=firstname,lastname=lastname)

    @classmethod
    def login(cls,username,pwd):
        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password,pwd):
            return u
        else:
            return False




