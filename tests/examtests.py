import os
import unittest
from website import app, db
from website.models import User
from website.exam_admin import add_exam, get_score, calc_score, get_current_exam
from .base import BaseCase

class TestExaminee(BaseCase):
    @classmethod
    def setUpClass(cls):
        db.create_all()
        cls.examinee = User(username='12345678', role='examinee',
                fullname='Charles Dickens', exam_id='silly1', answer_page='{}')
        cls.examinee.hash_password('hard2guess')
        db.session.add(cls.examinee)
        db.session.commit()
        add_exam('silly1', 'Silly 1', (os.path.join('tests', 'testdata', 'exams', 'silly1.json')),
                (os.path.join('tests', 'testdata', 'exams', 'silly1_answers.json')))

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()

    def setUp(self):
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.login('12345678', 'hard2guess')

    def tearDown(self):
        self.logout()

    def mock_test(self, ans1, ans2, ans3, ans4, ans5):
        """Take test helper function."""
        return self.app.post('/users/exam/finish', data={
            'silly1_list_01': ans1,
            'silly1_list_02': ans2,
            'silly1_struct_03': ans3,
            'silly1_struct_04': ans4,
            'silly1_read_05': ans5 
            }, follow_redirects=True)

    def test_initial(self):
        rv = self.app.get('/users/exam', follow_redirects=True)
        self.assertIn(b'read the instructions for each section carefully', rv.data)
        self.assertIn(b'Ontologically the goal exists only in the imagination', rv.data)
        self.assertIn(b'fart in your general direction', rv.data)
        self.assertIn(b'a swallow bring a coconut to such a temperate zone', rv.data)

    def test_full(self):
        """Mini exam with all correct answers."""
        self.mock_test("B", "D", "D", "A", "C")
        user = User.query.filter_by(username='12345678').first()
        score = get_score(user)
        listening, structure, reading = calc_score(score)
        self.assertEqual(len(score), 5)
        self.assertEqual(listening, 2)
        self.assertEqual(structure, 2)
        self.assertEqual(reading, 1)

    def test_not_full(self):
        """Mini exam with some incorrect answers."""
        self.mock_test("B", "B", "D", "C", "C")
        user = User.query.filter_by(username='12345678').first()
        score = get_score(user)
        listening, structure, reading = calc_score(score)
        self.assertEqual(len(score), 3)
        self.assertEqual(listening, 1)
        self.assertEqual(structure, 1)
        self.assertEqual(reading, 1)

    def test_view_current_examinee(self):
        """Check admin.py call to current examinee."""
        self.mock_test("A", "B", "C", "D", "A")
        answers = get_current_exam('12345678')
        self.assertEqual(answers['silly1_list_01'], "A")
        self.assertEqual(answers['silly1_list_02'], "B")
        self.assertEqual(answers['silly1_struct_03'], "C")
        self.assertEqual(answers['silly1_struct_04'], "D")
        self.assertEqual(answers['silly1_read_05'], "A")

    def test_finish(self):
        rv = self.app.post('/users/exam/finish', follow_redirects=True)
        self.assertIn(b'have been logged out', rv.data)

if __name__ == '__main__':
    unittest.main()
