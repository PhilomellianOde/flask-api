import sqlite3
import click
from flask import current_app, g

# g is special object unique to each request
#   used to store data that might be accessed by multiple funcs during request

# current_app points tp the Flask app handling the request

def get_db():
    if 'db' not in g:

        # establishes db connection based on DATABASE config
        #   file is okay to not exist until db intialized

        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        #tells connection to return rows that behave like dicts
        # formats such that columns can be accessed by name
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# initializing tables
def init_db():
    db = get_db()

    # open_resource opens file relative to flaskr, allowing file to be out anywhere
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

#defines CL command called init-db
@click.command('init-db')
def init_db_command():
    """Clear existing able and create new tables"""
    init_db()
    click.echo('Initialized the database')

# registering with app

def init_app(app):
    #calls function when cleaning up folowing response
    app.teardown_appcontext(close_db)
    
    #adds new command that can be called with 'flask' command
    app.cli.add_command(init_db_command)

