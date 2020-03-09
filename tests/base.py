import unittest
import json
from website import app, db

class BaseCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, username, password):
        """Login helper function"""
        return self.app.post('/users/login', data=dict(
            username=username,
            password=password
            ), follow_redirects=True)

    def logout(self):
        """Logout helper function"""
        return self.app.get('/users/logout', follow_redirects=True)

    def add_examinee(self, exam_id, fullname):
        """Add examinee helper function."""
        return self.app.post('/users/addexaminee', data=json.dumps(dict(
            exam_id=exam_id,
            fullname=fullname
            )), content_type='application/json', follow_redirects=True)

