import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

     
# CONFIG DATABASE
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'pst_key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)


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

# ROUTES
@app.route("/")
def index():
    cur = g.db.execute('select id, title, descr, done from entries order by id desc')
    tasks = [dict(id=row[0], title=row[1], descr=row[2], done=row[3]) for row in cur.fetchall()]
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_entry():
    g.db.execute('insert into entries (title, descr, done) values (?, ?, ?)', [request.form['title'], request.form['descr'], 0])
    g.db.commit()
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete_task():
    g.db.execute('delete from entries where id = ?', [request.form['task_to_delete']])
    g.db.commit()
    return redirect(url_for('index'))

@app.route('/move', methods=['POST'])
def move_task():
    g.db.execute('update entries set done=1 where id=?', [request.form['task_to_move']])
    g.db.commit()
    return redirect(url_for('index'))

# INITIALIZATION
if __name__ == "__main__":
    app.run(debug=True)