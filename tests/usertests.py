import unittest
from website.admin import add_admin
from .base import BaseCase

class TestUnauthorized(BaseCase):
    def test_user_pages(self):
        rv = self.app.get('/users', follow_redirects=True)
        self.assertIn(b'are not authorized to view this page', rv.data)
        rv = self.app.post('/users/addexaminee', follow_redirects=True)
        self.assertIn(b'are not authorized to view this page', rv.data)
        rv = self.app.post('/users/examscore', follow_redirects=True)
        self.assertIn(b'are not authorized to view this page', rv.data)

    def test_exam_pages(self):
        rv = self.app.get('/users/exam', follow_redirects=True)
        self.assertIn(b'are not authorized to view this page', rv.data)

class TestUser(BaseCase):
    def test_login_logout(self):
        """Test login and logout using helper functions"""
        add_admin('admin', 'default', 'Admin')
        rv = self.login('admin', 'default')
        self.assertIn(b'PYU Entrance Exam', rv.data)
        rv = self.logout()
        self.assertIn(b'You have been logged out', rv.data)
        rv = self.login('adxmin', 'default')
        self.assertIn(b'Invalid credentials', rv.data)
        rv = self.login('admin', 'dxefault')
        self.assertIn(b'Invalid credentials', rv.data)

    def test_add_examinee(self):
        add_admin('admin', 'default', 'Admin')
        rv = self.login('admin', 'default')
        rv = self.add_examinee('silly1', 'Henry James')
        self.assertIn(b'Hide student names', rv.data)
        rv = self.add_examinee('silly1', 'Thomas Hardy')
        self.assertIn(b'Thomas Hardy', rv.data)

if __name__ == '__main__':
    unittest.main()
