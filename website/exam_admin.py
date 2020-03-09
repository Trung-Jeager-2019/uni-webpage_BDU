import json
import random
from datetime import datetime
from website import db
from website.models import User, Exams, Examscores

def get_score(user):
    """Return a list of answers that are correct."""
    answers = json.loads(user.answer_page)
    exam_id = user.exam_id
    data = Exams.query.filter_by(exam_id=exam_id).first().correct
    score = [key for key, val in data.items() if val == answers.get(key)]
    return score

def calc_score(ans_list):
    """Calculate the score for each section of the exam."""
    listening = structure = reading = 0
    for ans in ans_list:
        if ans.split('_')[1] == 'list':
            listening += 1
        elif ans.split('_')[1] == 'struct':
            structure += 1
        else:
            reading += 1
    return listening, structure, reading

def update_db(user, exam_score):
    """Remove the user (examinee) from the User table and add him/her to the
    Examscores table.
    """
    answer_page = json.loads(user.answer_page)
    taken_date = datetime.now().date()
    db.session.add(Examscores(username=user.fullname, code=user.username,
        taken_date=taken_date, answer_page=answer_page, exam_score=exam_score))
    db.session.delete(user)
    db.session.commit()

def record_scores(user, writing):
    """Get the user's scores, apply the calculation formula, if necessary,
    and assign a grade to the user.
    """
    exams = {'pyueng5': 'PYU Entrance Exam 5',
            'pyueng8': 'PYU Entrance Exam 8',
            'geneng1': 'General English 1'}
    exam_id = exams.get(user.exam_id, 'English Exam 0')
    listening, structure, reading = calc_score(get_score(user))
    if user.exam_id.startswith('pyueng'):
        total = round(((listening + structure + reading + 55) * 11.6/3) - 23.5 + (writing * 7.83))
        grade = get_grade(total)
    else:
        total = listening + structure + reading + writing
        grade = ''
    exam_score = {'exam_id': exam_id, 'listening': listening, 'structure': structure,
            'reading': reading, 'writing': writing, 'total': total, 'grade': grade}
    update_db(user, exam_score)

def get_grade(total):
    """Calculate the grade for the PYU exam."""
    if total > 629:
        grade = 'Grade: Upper advanced'
    elif total > 569:
        grade = 'Grade: Lower advanced'
    elif total > 446:
        grade = 'Grade: Upper intermediate'
    elif total > 342:
        grade = 'Grade: Lower intermediate'
    elif total > 326:
        grade = 'Grade: Elementary'
    else:
        grade = 'Grade: Beginner'
    return grade

def add_examinees(namelist):
    """Add examinees to the User table in the database.
    The namelist is a list of tuples. Each tuple contains the username,
    or user id, fullname, or real name, and exam id. If the username is
    None, a random username is generated.
    This function returns a list of tuples. Each tuple contains the username,
    password (randomly generated), fullname and exam id.
    """
    examinees = []
    for (username, fullname, exam_id) in namelist:
        username, password = get_user_id(username)
        user = User(username=username, role='examinee', fullname=fullname,
                exam_id=exam_id, answer_page='{}')
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        examinees.append((username, password, fullname, exam_id))
    return examinees

def add_exam(exam_id, exam_name, question_path, answer_path):
    """Add a new exam's questions and answers to the database."""
    with open(question_path) as questions:
        pages = json.load(questions)
    with open(answer_path) as answers:
        correct = json.load(answers)
    db.session.add(Exams(exam_id=exam_id, exam_name=exam_name, pages=pages, correct=correct))
    db.session.commit()

def get_current_exam(username):
    """View the answer page of a current examinee."""
    user = User.query.filter_by(username=username).first()
    return json.loads(user.answer_page)

def get_old_exams(realname):
    """View the score of someone who has taken the exam."""
    user = Examscores.query.filter_by(fullname=realname).first()
    return user.exam_score

def rand_password():
    """Generate a random password for the examinee."""
    alphabet = '2345789;!@#$%*abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
    myrg = random.SystemRandom()
    length = 8
    return ''.join(myrg.choice(alphabet) for i in range(length))

def get_user_id(user_id):
    """Assign an id or generate a random number to be used as the username."""
    if user_id and not User.query.filter_by(username=str(user_id)).count():
        password = rand_password()
        return user_id, password
    return get_user_id(random.randrange(100000, 199999))
