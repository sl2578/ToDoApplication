import sqlite3, datetime, os.path
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, DateTimeField
from wtforms.validators import DataRequired


# CONFIG DATABASE
DATABASE = 'tmp/todo.db'
DEBUG = True
SECRET_KEY = 'pst_key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


# SETTING UP THE DB
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('todo.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# FORM VALIDATION
# class AddTodo(Form):
#     title = TextField('Title')
#     descr = TextAreaField('Description')
#     dline = DateTimeField('Deadline')
#     submit = SubmitField('Add')

# ROUTES
@app.route("/")
def index():
    # form = AddTodo(request.form)
    cur = g.db.execute('select id, title, descr, done, dline, finish from entries order by id desc')
    tasks = [dict(id=row[0], title=row[1], descr=row[2], done=row[3], dline=row[4], finish=row[5]) 
        for row in cur.fetchall()]
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET','POST'])
def add_entry():
    # form = AddTodo(request.form)
    # print form.title.data
    # if form.validate():
    g.db.execute('insert into entries (title, descr, done, dline, finish) values (?, ?, ?, ?, ?)', 
    [request.form['title'], request.form['descr'], 0, request.form['dline'], datetime.datetime.now().strftime('%Y-%m-%d %H:%M')])
    g.db.commit()
    return redirect(url_for('index'))
    # else:
        # flash('Sorry, invalid format. Correct format includes non-empty task name and deadline of format of YYYY-MM-DD HH:MM')
        # return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
def delete_task():
    g.db.execute('delete from entries where id = ?', [request.form['task_to_delete']])
    g.db.commit()
    return redirect(url_for('index'))

@app.route('/move', methods=['POST'])
def move_task():
    time = datetime.datetime.now()
    g.db.execute('update entries set done=1 where id=?', [request.form['task_to_move']])
    g.db.commit()
    return redirect(url_for('index'))

# INITIALIZATION
if __name__ == "__main__":
    app.run(debug=True)












