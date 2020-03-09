import json
from datetime import datetime
from flask import render_template, request, redirect, flash, url_for
from flask.ext.login import login_user, logout_user, current_user
from website import app, db, login_man
from website.models import User, Exams, Examscores
from website.forms import LoginForm
from website.admin import login_required
from website.exam_admin import record_scores, add_examinees

@login_man.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.after_request
def add_no_cache(response):
    """Make sure that pages are not cached if the current user is authenticated."""
    if current_user.is_authenticated():
        response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.route('/users/exam')
@login_required(role='examinee')
def exam_page():
    """Display exam page for the user."""
    exam_id = current_user.exam_id
    answers = json.loads(current_user.answer_page)
    data = Exams.query.filter_by(exam_id=exam_id).first().pages
    return render_template('users/exam.html',
            welcome=get_time_limit(data.get('pages')[0]),
            pages=data.get('pages')[1:],
            answers=answers)

def get_time_limit(data):
    """Format the time limit for the exam."""
    (hrs, mins) = divmod(data.get('time_limit', 180), 60)
    data['time_string'] = 'Time remaining: {}:{:02d}'.format(hrs, mins)
    return data

@app.route('/users/exam/update_results', methods=['POST'])
@login_required(role='examinee')
def update_results():
    """Get the user's answers. This function can be called periodically
    during the exam so that data loss can be kept to a minimum.
    """
    results_to_db(request.get_json())
    return json.dumps({'status': 'ok'})

@app.route('/users/exam/finish', methods=['POST'])
@login_required(role='examinee')
def finish():
    """Get the user's answers and logout user."""
    results_to_db(request.form.items())
    return redirect(url_for('logout'))

def results_to_db(items):
    """Add the user's answers to the database."""
    if isinstance(items, dict):
        results = items
    else:
        results = {item[0]: item[1] for item in items if item[0] != 'csrf_token'}
    answers = json.loads(current_user.answer_page)
    answers.update(results)
    current_user.answer_page = json.dumps(answers)
    db.session.commit()

@app.route('/users/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user or not user.check_password(form.password.data):
            flash('Invalid credentials.')
            return redirect(url_for('login'))
        login_user(user)
        if user.role == 'admin':
            return redirect(url_for('user_page'))
        else:
            return redirect(url_for('exam_page'))
    return render_template('users/login.html', form=form)

@app.route('/users/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/users')
@login_required(role='admin')
def user_page():
    """The main admin user page."""
    exams = [(q.exam_id, q.exam_name) for q in Exams.query.all()
            if q.exam_id.startswith('pyueng')]
    old = list(set([exam.taken_date for exam in Examscores.query.all()]))
    old.sort(reverse=True)
    return render_template('users/index.html', exams=exams, old=old)

@app.route('/users/addexaminee', methods=['POST'])
@login_required(role='admin')
def addexaminee():
    """Add an examinee to the User table in the database."""
    items = dict(request.get_json())
    users = add_examinees([(None, items.get('fullname'), items.get('exam_id'))])
    if users:
        (username, password, fullname, exam_id) = users.pop(0)
    button = items.get('button', False)
    return render_template('partials/shownamepass.html',
            fullname=fullname, username=username, password=password, button=button)

@app.route('/users/examscore', methods=['POST'])
@login_required(role='admin')
def examscore():
    """Display exam scores filtered by date."""
    items = dict(request.get_json())
    date = items.get('getscore')
    exams = Examscores.query.filter_by(taken_date=date).all()
    scores = [(exam.username, exam.code, exam.exam_score) for exam in exams]
    return render_template('partials/showscore.html', scores=scores)

@app.route('/users/examreport/<int:code>')
@login_required(role='admin')
def examreport(code):
    """Produce a printable report providing details about the exam score.
    The title of the report uses the value of the exam.exam_id without the number.
    """
    exam = Examscores.query.filter_by(code=str(code)).first()
    taken_date = datetime.strftime(exam.taken_date, '%d %B %Y')
    return render_template('users/examreport.html',
            name=exam.username, exam=exam.exam_score, taken_date=taken_date)

@app.route('/users/examwriting', methods=['POST'])
@login_required(role='admin')
def examwriting():
    """Send the user's writing score, calculate the total score and update
    the database. Once the total score is calculated, the user is transferred
    from the User table to the Examscores table in the database.
    """
    items = dict(request.get_json())
    for data in items:
        user = User.query.filter_by(username=data).first()
        if user:
            writing = float(items.get(data) or 0)
            writing = writing if writing <= 6 else 0
            record_scores(user, writing)
    return str(datetime.now().date())

@app.route('/users/checkwriting', methods=['POST'])
@login_required(role='admin')
def checkwriting():
    """Show the examinees' writing so that they can be assessed."""
    users = User.query.all()
    check = [assess_writing(username) for username in users
            if username.role == 'examinee' and json.loads(username.answer_page)]
    return render_template('partials/checkwriting.html', check=check)

def assess_writing(user):
    """Get the user's writing section from his/her answer_page."""
    answers = json.loads(user.answer_page)
    writing = answers.get('writing')
    return (user.username, user.fullname, writing)
