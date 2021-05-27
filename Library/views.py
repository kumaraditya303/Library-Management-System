"""
Routes and views for the flask application.
"""

from datetime import datetime, timedelta
from functools import wraps

from flask import flash, redirect, render_template, request, url_for
from flask.blueprints import Blueprint
from flask.views import MethodView
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db, login_manager
from .models import Book, Copy, User

main = Blueprint("main", __name__)


def requires_admin(f):
    """Checks if user has admin access"""

    @wraps(f)
    def wrapped(*args, **kwargs):
        if current_user.admin:
            return f(*args, **kwargs)
        return unauthorized()

    return wrapped


@login_manager.user_loader
def load_user(user_id: int):
    return User.query.get(user_id)


@main.route("/", methods=["GET"])
def index():
    """Home Page"""
    books = Book.query.all()
    if books:
        return render_template("index.html", year=datetime.now().year, books=books)
    flash("No books are in library!")
    return render_template("index.html", year=datetime.now().year)


class LoginView(MethodView):
    def get(self):
        return render_template("login.html", year=datetime.now().year)

    def post(self):
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            if request.args.get("next"):
                return redirect(request.args.get("next"))
            return redirect(url_for("main.dashboard"))
        flash("Invalid Credentials!")
        return redirect(url_for("main.login"))


class RegisterView(MethodView):
    def get(self):
        return render_template("register.html", year=datetime.now().year)

    def post(self):
        name = request.form.get("name")
        email = request.form.get("email")
        isadmin = request.form.get("isAdmin")
        
        password = generate_password_hash(request.form.get("password"), method="sha256")
        if User.query.filter_by(email=email).first():
            flash("User already exists!")
            return redirect(url_for("main.register"))

        if(isadmin == "on"):
            user = User(name=name, email=email, password=password, admin=True)
        else:
            user = User(name=name, email=email, password=password)
        
        db.session.add(user)
        db.session.commit()
        login_user(user)
        if request.args.get("next"):
            return redirect(request.args.get("next"))
        return redirect(url_for("main.dashboard"))


class AdminView(MethodView):
    def get(self):
        return render_template("admin.html", year=datetime.now().year)

    def post(self):
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email, admin=True).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            if request.args.get("next"):
                return redirect(request.args.get("next"))
            return redirect(url_for("main.admin_dashboard"))
        flash("Invalid Credentials!")
        return redirect(url_for("main.admin"))


@main.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    copies = db.session.query(Book.id, Book.name, Book.author, Copy.date_issued, Copy.date_return) \
    .join(Book).filter(Copy.book == Book.id).filter(Copy.issued_by == current_user.id).all()

    if copies:
        return render_template("dashboard.html", year=datetime.now().year, books=copies)

    flash("You don't have books issued!")
    return render_template("dashboard.html", year=datetime.now().year)


@main.route("/admin/dashboard", methods=["GET"])
@login_required
@requires_admin
def admin_dashboard():
    books = Book.query.all()
    if books:
        return render_template(
            "admin_dashboard.html", books=books, year=datetime.now().year
        )
    flash("No books are there in library! Add Some")
    return render_template("admin_dashboard.html", year=datetime.now().year)


class ShowStudentView(MethodView):
    def get(self):
        students = User.query.filter_by(admin = False).all()
        print(students)
        if students:
            return render_template("show_students.html", student=students, year=datetime.now().year)

        flash("No Student registered till now")
        return render_template("admin_dashboard.html", year=datetime.now().year)


class AddBookView(MethodView):
    def get(self):
        return render_template("add_book.html", year=datetime.now().year)

    def post(self):
        name = request.form.get("name")
        author = request.form.get("author")
        description = request.form.get("description")
        number = int(request.form.get("number"))
        book = Book.query.filter_by(name=name).first()
        if book:
            flash("Book already exists!")
            return redirect(url_for("main.add_book"))
        book = Book(
            name=name,
            author=author,
            description=description,
            total_copy=number,
            present_copy=number,
            issued_copy=0,
        )

        for _ in range(number):
            copy = Copy(date_added=datetime.now())
            book.copy.append(copy)
            db.session.add(book)
        db.session.commit()
        flash("Book added successfully!")
        return redirect(url_for("main.admin_dashboard"))


@main.route("/admin/logout")
@login_required
@requires_admin
def admin_logout():
    return redirect(url_for("main.index"))


class IssueBookView(MethodView):
    def get(self):
        books = Book.query.filter(Book.present_copy > 0).all()
        if books:
            return render_template(
                "issue.html", books=Book.query.all(), year=datetime.now().year
            )
        flash("No books are currently available!")
        return render_template(
            "issue.html", year=datetime.now().year, books=Book.query.all()
        )

    def post(self):
        book_id = int(request.form.get("book"))
        copy = Copy.query.filter_by(
            book=book_id, issued_by=None
        ).first()
        print(copy)
        copy.book = book_id
        copy.issued_by = current_user.id
        copy.date_issued = datetime.now()
        copy.date_return = datetime.now() + timedelta(days=1)
        db.session.commit()

        book = Book.query.filter_by(
            id=book_id
        ).first()
        print(book)
        book.issued_copy += 1
        book.present_copy -= 1
        db.session.commit()

        flash("Book issued successfully!")
        return redirect(url_for("main.dashboard"))


class ReturnBookView(MethodView):
    def get(self):
        copies = db.session.query(Book.id, Book.name, Book.author, Copy.issued_by) \
        .join(Book).filter(Copy.book == Book.id).filter(Copy.issued_by == current_user.id).all()

        if copies:
            return render_template(
                "return.html", books=copies, year=datetime.now().year
            )

        flash("You don't have any books issued!")
        return render_template(url_for("main.dashboard"))

    def post(self):
        book_id = int(request.form.get("book"))
        copy = Copy.query.filter_by(
            book=book_id, issued_by=current_user.id
        ).first()
        copy.issued_by = None
        copy.date_issued = None
        copy.date_return = None
        db.session.commit()

        book = Book.query.filter_by(
            id=book_id
        ).first()
        book.issued_copy -= 1
        book.present_copy += 1
        db.session.commit()
        flash("Book returned successfully!")
        return redirect(url_for("main.dashboard"))


class RemoveBookView(MethodView):
    def get(self):
        books = Book.query.filter_by(issued_copy=0).all()
        if books:
            return render_template(
                "remove_book.html", year=datetime.now().year, books=Book.query.all()
            )

        flash("No books are available to be removed!")
        return render_template(
            "remove_book.html", year=datetime.now().year, books=Book.query.all()
        )

    def post(self):
        book_id = int(request.form.get("book"))
        book = Book.query.filter_by(id=book_id).first()
        db.session.delete(book)
        db.session.commit()
        flash("Book removed successfully!")
        return redirect(url_for("main.admin_dashboard"))


main.add_url_rule("/register", view_func=RegisterView.as_view("register"))
main.add_url_rule("/login", view_func=LoginView.as_view("login"))
main.add_url_rule("/admin", view_func=AdminView.as_view("admin"))

main.add_url_rule(
    "/show/students",
    view_func=login_required(requires_admin(ShowStudentView.as_view("show_students"))),
)
main.add_url_rule(
    "/add/book",
    view_func=login_required(requires_admin(AddBookView.as_view("add_book"))),
)
main.add_url_rule(
    "/return/book", view_func=login_required(ReturnBookView.as_view("return_book"))
)
main.add_url_rule(
    "/remove/book", view_func=login_required(RemoveBookView.as_view("remove_book"))
)
main.add_url_rule(
    "/issue/book", view_func=login_required(IssueBookView.as_view("issue_book"))
)


@main.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@login_manager.unauthorized_handler
def unauthorized():
    flash("You are not authorized to access the content!")
    return redirect(url_for("main.login"))
