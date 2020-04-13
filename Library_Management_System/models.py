from Library_Management_System import db, UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    book = db.relationship('Copy', backref='issue', lazy=True)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    author = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    copy = db.relationship('Copy', backref='copies',
                           cascade='all,delete', lazy=True)
    total_copy = db.Column(db.Integer, nullable=False)
    issued_copy = db.Column(db.Integer, nullable=False)
    present_copy = db.Column(db.Integer, nullable=False)


class Copy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime(), nullable=False)
    issued_by = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False, default=0)
    date_issued = db.Column(db.DateTime(), default=None)
    date_return = db.Column(db.DateTime(), default=None)
    book = db.Column(db.Integer, db.ForeignKey('book.id'))
