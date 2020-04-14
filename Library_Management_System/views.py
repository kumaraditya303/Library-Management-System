"""
Routes and views for the flask application.
"""

from datetime import *
from functools import wraps
from threading import Thread

from flask import *
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message
from werkzeug.security import check_password_hash, generate_password_hash

from Library_Management_System import app, db, login_manager, mail, scheduler
from Library_Management_System.models import *

sess = 'user'
direct = 0


def notify():
    books = Copy.query.filter(Copy.issued_by > 0).all()
    for book in books:
        if book.date_return.hour == datetime.now().hour and book.date_return.date == datetime.now().date:
            send_mail(
                'Book return Notification',
                'admin@librarymgmtsystem.com',
                [book.issue.email],
                f"""<!DOCTYPE html>
<html lang="en">

<head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css'>
     <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'>
     <title>Book return Notification</title>
</head>

<body>
     <div class="container-fluid jumbotron">
          <h1>Dear {book.issue.name},</h1><br>
          <p class="lead">
               This is to notify you that {book.copies.name} book issued with Library Management System with your email {book.issue.email},<br>
               must be returned to the Library before { book.date_return } to avoid fine.<br>
               If you did not issue this book, then you may safely ignore this email.<br><br>

               Regards,<br>
               Library Management System.<br>
          </p>
     </div>
     <script src='https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js'></script>
     <script src='https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js'></script>
</body>

</html>"""
            )


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def send_async_email(app, msg):
    """Sends asynchronous emails with app context"""
    with app.app_context():
        mail.send(msg)


def send_mail(subject, sender, recipients, html_body):
    """Starts a new Thread to send email"""
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = html_body
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()


def requires_roles(roles):
    """Checks if user is authorized"""
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not sess == roles:

                return unauthorized()
            return f(*args, **kwargs)
        return wrapped

    return wrapper


@app.route('/', methods=['GET'])
def index():
    """Home Page"""
    books = Book.query.all()
    if books:
        return render_template(
            'index.html',
            year=datetime.now().year,
            books=books
        )
    else:
        flash('No books are in library!')
        return render_template(
            'index.html',
            year=datetime.now().year

        )


@app.route('/issue_direct/<id>', methods=['GET'])
def issue_direct(id):
    if current_user.is_authenticated:
        global direct
        direct = id
        return redirect(url_for('new_issue'))
    else:
        direct = id
        return redirect(url_for('login'))


@app.route('/login', methods=['GET'])
def login():
    return render_template(
        'login.html',
        year=datetime.now().year
    )


@app.route('/login', methods=['POST'])
def log_in_user():
    email = request.form['email']
    password = request.form['password']
    chkusr = User.query.filter_by(email=email).first()
    if chkusr and check_password_hash(chkusr.password, password):
        login_user(chkusr)
        if int(direct) > 0:
            return redirect(url_for('new_issue'))
        return redirect('/dashboard')
    else:
        flash('Invalid Credentials!')
        return redirect(url_for('login'))


@app.route('/register', methods=['GET'])
def register():
    return render_template(
        'register.html',
        year=datetime.now().year
    )


@app.route('/register', methods=['POST'])
def register_user():
    name = request.form['name']
    email = request.form['email']
    password = generate_password_hash(
        request.form['password'], method='sha256')
    chkusr = User.query.filter_by(email=email).first()
    if chkusr:
        flash('User already exists!')
        return redirect(url_for('register'))
    else:
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        send_mail('Registration Success Notification', 'admin@librarymgmtsystem.com', [
            current_user.email], f"""
<!DOCTYPE html>
<html lang="en">

<head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css'>
     <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'>
     <title>Registration Success</title>
</head>

<body>
     <div class="container-fluid jumbotron">
          <h1>Dear {current_user.name},</h1><br>
          <p class="lead">
               Thank you for registering With Library Management System with your email {current_user.email},<br>
               Your account is active and you can start issuing books.<br>
               If you did not initiate this registration, then you may safely ignore this email.<br><br>

               Regards,<br>
               Library Management System.<br>
          </p>
     </div>
     <script src='https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js'></script>
     <script src='https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js'></script>
</body>

</html>""")
    return redirect('/dashboard')


@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    copies = Copy.query.filter_by(issued_by=current_user.id).all()
    if copies:
        return render_template(
            'dashboard.html',
            year=datetime.now().year,
            books=copies
        )
    else:
        flash("You don't have books issued!")
        return render_template(
            'dashboard.html',
            year=datetime.now().year
        )


@app.route('/admin', methods=['GET'])
def admin_html():
    return render_template(
        'admin.html',
        year=datetime.now().year
    )


@app.route('/admin', methods=['POST'])
def admin_login():
    global sess
    username = request.form['username']
    password = request.form['password']
    if username == app.config['ADMIN_USERNAME'] and password == app.config['ADMIN_PASSWORD']:
        sess = 'admin'
        return redirect(url_for('admin_dashboard'))
    else:
        flash('Invalid Credentials!')
        return redirect(url_for('admin_html'))


@app.route('/admin_dashboard',methods=['GET'])
@requires_roles('admin')
def admin_dashboard():

    books = Book.query.all()
    if books:
        return render_template(
            'admin_dashboard.html',
            books=books,
            year=datetime.now().year
        )
    else:
        flash('No books are there in library!')
        return render_template(
            'admin_dashboard.html',
            year=datetime.now().year
        )


@app.route('/add/book', methods=['GET'])
@requires_roles('admin')
def add_book():
    return render_template(
        'add_book.html',
        year=datetime.now().year
    )


@app.route('/add/book', methods=['POST'])
@requires_roles('admin')
def add_book_data():
    name = request.form['name']
    author = request.form['author']
    description = request.form['description']
    number = request.form['number']
    book = Book.query.filter_by(name=name).first()
    if book:
        flash('Book already exists!')
        return redirect(url_for('add_book'))
    else:
        book = Book(name=name, author=author,
                    description=description, total_copy=number, present_copy=number, issued_copy=0)
        for i in range(int(number)):
            copy = Copy(date_added=datetime.now())
            book.copy.append(copy)
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!')
        return redirect(url_for('admin_dashboard'))


@app.route('/admin/logout')
@requires_roles('admin')
def admin_logout():
    global sess
    sess = 'user'
    return redirect(url_for('index'))


@app.route('/new/issue', methods=['POST'])
@login_required
def issue():
    global direct
    direct = 0
    book_id = request.form['book']
    book = Copy.query.filter_by(book=int(book_id), issued_by=0).first()
    book.issued_by = current_user.id
    book.copies.issued_copy += 1
    book.copies.present_copy -= 1
    book.date_issued = datetime.now()
    book.date_return = datetime.now()+timedelta(days=1)
    db.session.commit()
    send_mail('Book issue Notification', 'admin@librarymgmtsystem.com', [current_user.email],
              f"""<!DOCTYPE html>
<html lang="en">

<head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css'>
     <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'>
     <title>Book Issued Successfully</title>
</head>

<body>
     <div class="container-fluid jumbotron">
          <h1>Dear {current_user.name},</h1><br>
          <p class="lead">
               Thank you for issuing {book.copies.name} book with Library Management System,<br><br>
               The book details are below: <br>
               Book Name : {book.copies.name} <br>
               Book Author : {book.copies.author} <br>
               Issuing Date : {book.date_issued} <br>
               Date Of Return : {book.date_return} <br>
               If you did not initiate this issue, then you may safely ignore this email.<br><br>

               Regards,<br>
               Library Management System.<br>
          </p>
     </div>
     <script src='https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js'></script>
     <script src='https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js'></script>
</body>

</html>""")
    flash('Book issued successfully!')
    return redirect(url_for('dashboard'))


@app.route('/new/issue', methods=['GET'])
@login_required
def new_issue():
    books = Book.query.filter(Book.present_copy > 0).all()
    if books and len(current_user.book) < 2:
        global direct
        if current_user.book:
            t = current_user.book[0].copies.name
            print(t)
        else:
            t = ""

        return render_template(
            'issue.html',
            books=Book.query.all(),
            year=datetime.now().year,
            auto=int(direct),
            t=t
        )
    elif len(current_user.book) == 2:
        flash('You have already issued 2 books!')
        return render_template(
            'issue.html',
            year=datetime.now().year,
            books=Book.query.all(),
            flag=True
        )

    else:
        flash('No books are currently available!')
        return render_template(
            'issue.html',
            year=datetime.now().year,
            books=Book.query.all(),
            flag=True
        )


@app.route('/new/return', methods=['GET'])
@login_required
def return_book_html():
    user = Copy.query.filter_by(issued_by=current_user.id).all()
    if user:
        return render_template(
            'return.html',
            books=user,
            year=datetime.now().year
        )
    else:
        flash("You don't have any books issued!")
        return render_template(
            'return.html',
            year=datetime.now().year,
            books=Book.query.all(),
            flag=True
        )


@app.route('/new/return', methods=['POST'])
@login_required
def return_book():
    book_id = request.form['book']
    book = Copy.query.filter_by(
        book=int(book_id), issued_by=current_user.id).first()
    send_mail('Book returned Notification', 'admin@loginmgmtsystem.com', [current_user.email], f"""
    <!DOCTYPE html>
<html lang="en">

<head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css'>
     <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'>
     <title>Book Issued Successfully</title>
</head>

<body>
     <div class="container-fluid jumbotron">
          <h1>Dear {current_user.name},</h1><br>
          <p class="lead">
               Thank you for returning {book.copies.name} book with Library Management System,<br><br>
               The book details are below: <br>
               Book Name : {book.copies.name} <br>
               Issuing Date : {book.date_issued} <br>
               Return Date :{book.date_return} <br>
               If you did not initiate this issue, then you may safely ignore this email.<br><br>

               Regards,<br>
               Library Management System.<br>
          </p>
     </div>
     <script src='https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js'></script>
     <script src='https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js'></script>
</body>

</html>
    """)
    book.issued_by = 0
    book.date_issued = None
    book.date_return = None
    book.copies.issued_copy -= 1
    book.copies.present_copy += 1
    db.session.commit()
    flash('Book returned successfully!')
    return redirect(url_for('dashboard'))


@app.route('/remove/book', methods=['GET'])
@requires_roles('admin')
def remove_book():
    books = Book.query.filter_by(issued_copy=0).all()
    if books:
        return render_template(
            'remove_book.html',
            year=datetime.now().year,
            books=Book.query.all()
        )
    else:
        flash('No books are available to be removed!')
        return render_template(
            'remove_book.html',
            year=datetime.now().year,
            books=Book.query.all(),
            flag=True
        )


@app.route('/remove/book', methods=['POST'])
@requires_roles('admin')
def remove_book_db():
    book_id = request.form['book']
    book = Book.query.filter_by(id=int(book_id)).first()
    db.session.delete(book)
    db.session.commit()
    flash('Book removed successfully!')
    return redirect(url_for('admin_dashboard'))


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    global direct
    direct = 0
    return redirect(url_for('index'))


@login_manager.unauthorized_handler
def unauthorized():
    flash('You are not authorized to access the content!')
    return redirect(url_for('login'))


scheduler.add_job(func=notify, trigger="interval", hours=1)
scheduler.start()
