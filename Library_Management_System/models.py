from Library_Management_System import db, UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    book = db.relationship('Copy', backref='issue', lazy=True)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    author = db.Column(db.String(255), )
    description = db.Column(db.String(2000), )
    copy = db.relationship('Copy', backref='copies',
                           cascade='all,delete', lazy=True)
    total_copy = db.Column(db.Integer, )
    issued_copy = db.Column(db.Integer, )
    present_copy = db.Column(db.Integer, )


class Copy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime(), )
    issued_by = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=True, default=None)
    date_issued = db.Column(db.DateTime(), default=None)
    date_return = db.Column(db.DateTime(), default=None)
    book = db.Column(db.Integer, db.ForeignKey('book.id'))
