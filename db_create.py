import os
from website import db
from website.models import User
from website.admin import add_admin
from website.exam_admin import add_exam

db.reflect()
db.drop_all()
db.create_all()

os.chdir(os.path.join('tests', 'testdata'))
add_exam('silly1', 'Silly 1', os.path.join('exams', 'silly1.json'),
        os.path.join('exams', 'silly1_answers.json'))
add_admin('admin', 'pass', 'Admin')

user1 = User(username='1', role='examinee', fullname='Thomas Hardy', exam_id='silly1', answer_page='{}')
user1.hash_password('pass')
db.session.add(user1)
user2 = User(username='2', role='examinee', fullname='Franz Kafka', exam_id='silly1', answer_page='{}')
user2.hash_password('pass')
db.session.add(user2)
db.session.commit()
