import os
import unittest

from Library_Management_System import app, db, mail


class Tests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        mail.init_app(app)
        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_page(self):
        response = self.app.get('/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_admin_page(self):
        response = self.app.get('/admin', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_new_issue_page(self):
        response = self.app.get('/new/issue', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_admin_dash_page(self):
        response = self.app.get('/admin_dashboard')
        self.assertEqual(response.status_code, 302)
    def test_register_post_page(self):
        response = self.app.post(
            '/register',
            data=dict(name='Test',
                      email='testdomain.com',
                      password='Test&Test'),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

    def test_login_post_page(self):
        response = self.app.post(
            '/login',
            data=dict(email='test1@domain.com',
                      password='Test&Test'),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
