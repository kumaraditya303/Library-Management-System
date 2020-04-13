from config import TestConfig
from flask_testing import TestCase
from Library_Management_System import app, db
from Library_Management_System.models import User
from Library_Management_System.views import main
from werkzeug.security import generate_password_hash

app.register_blueprint(main)


class Test(TestCase):
    def create_app(self):
        app.config.from_object("config.TestConfig")
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.drop_all()


class TestGet(Test):
    def test_main_page(self):
        response = self.client.get("/")
        self.assertIn(b"Welcome to Library Management System", response.data)

    def test_login_page(self):
        response = self.client.get("/login")
        self.assertIn(b"Login", response.data)

    def test_register_page(self):
        response = self.client.get("/register")
        self.assertIn(b"Register", response.data)

    def test_admin_page(self):
        response = self.client.get("/admin")
        self.assertIn(b"Admin", response.data)


class TestGetAuth(Test):
    def test_dashboard_page(self):
        response = self.client.get("/dashboard")
        self.assertRedirects(response, "/login")

    def test_admin_dashboard_page(self):
        response = self.client.get("/admin/dashboard")
        self.assertRedirects(response, "/login")

    def test_add_book_page(self):
        response = self.client.get("/add/book")
        self.assertRedirects(response, "/login")

    def test_remove_book_page(self):
        response = self.client.get("/remove/book")
        self.assertRedirects(response, "/login")

    def test_return_book_page(self):
        response = self.client.get("/return/book")
        self.assertRedirects(response, "/login")


class TestPost(Test):
    def setUp(self):
        super().setUp()
        admin_user = User(
            email="test@domain.com",
            password=generate_password_hash("Test&Test", method="sha256"),
            admin=True,
        )
        db.session.add(admin_user)
        db.session.commit()

    def test_user_login_post_page(self):
        response = self.client.post(
            "/admin", data=dict(email="test@domain.com", password="Test&Test")
        )
        self.assertRedirects(response, "/dashboard")

    def test_add_book_post_page(self):
        response = self.client.post(
            "/admin", data=dict(email="test@domain.com", password="Test&Test")
        )
        response = self.client.post(
            "/add/book",
            data=dict(
                name="Test Book", author="Tester", number=5, description="Test Book"
            ),
            follow_redirects=True,
        )
        self.assertIn(b"Book added successfully!", response.data)

    def test_remove_book_post_page(self):
        self.client.post(
            "/admin", data=dict(email="test@domain.com", password="Test&Test")
        )
        self.client.post(
            "/add/book",
            data=dict(
                name="Test Book", author="Tester", number=5, description="Test Book"
            ),
            follow_redirects=True,
        )
        response = self.client.post(
            "/remove/book", data=dict(book=1), follow_redirects=True
        )
        self.assertIn(b"Book removed successfully!", response.data)

    def test_register_post_page(self):
        response = self.client.post(
            "/register",
            data=dict(name="Test", email="test1@domain.com", password="Test&Test1"),
        )
        self.assertRedirects(response, "/dashboard")

    def test_admin_register_post_page(self):
        response = self.client.post(
            "/admin", data=dict(email="test@domain.com", password="Test&Test")
        )
        self.assertRedirects(response, "/dashboard")
