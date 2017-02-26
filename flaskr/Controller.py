from flask import request, session, g, redirect, url_for, abort, \
     render_template, flash

class Controller():

    def __init__(self, app, database):
        self.app = app
        self.database = database
        self.app.route('/')(self.show_entries)
        self.app.route('/add', methods=['POST'])(self.add_entry)
        self.app.route('/login', methods=['GET', 'POST'])(self.login)
        self.app.route('/logout')(self.logout)

    def show_entries(self):
        db = self.database.get_db()
        cur = db.execute('select title, text from entries order by id desc')
        entries = cur.fetchall()
        return render_template('show_entries.html', entries=entries)

    def add_entry(self):
        db = self.database.get_db()
        if not session.get('logged_in'):
            abort(401)
        db.execute('insert into entries (title, text) values (?, ?)',
                [request.form['title'], request.form['text']])
        db.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('show_entries'))


    def login(self):
        error = None
        if request.method == 'POST':
            if request.form['username'] != self.app.config['USERNAME']:
                error = 'Invalid username'
            elif request.form['password'] != self.app.config['PASSWORD']:
                error = 'Invalid password'
            else:
                session['logged_in'] = True
                flash('You were logged in')
                return redirect(url_for('show_entries'))
        return render_template('login.html', error=error)

    def logout(self):
        session.pop('logged_in', None)
        flash('You were logged out')
        return redirect(url_for('show_entries'))

