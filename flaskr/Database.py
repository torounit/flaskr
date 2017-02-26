from sqlite3 import dbapi2 as sqlite3
from flask import g

class Database():
    """DB class"""

    def __init__(self, app):
        self.app = app

    def connect_db(self):
        """Connects to the specific database."""
        rv = sqlite3.connect(self.app.config['DATABASE'])
        rv.row_factory = sqlite3.Row
        return rv


    def init_db(self):
        """Initializes the database."""
        db = self.get_db()
        with self.app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

    def initdb_command(self):
        """Creates the database tables."""
        self.init_db()
        print('Initialized the database.')


    def get_db(self):
        """Opens a new database connection if there is none yet for the
        current application context.
        """
        if not hasattr(g, 'sqlite_db'):
            g.sqlite_db = self.connect_db()
        return g.sqlite_db

    #@app.teardown_appcontext
    def close_db(self, error):
        """Closes the database again at the end of the request."""
        if hasattr(g, 'sqlite_db'):
            g.sqlite_db.close()


            