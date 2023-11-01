#import packages
import os
from flask import Flask, render_template

# __init__.py contains App factory and lets Python know to treat flaskr
# directory as a package.

def create_app(test_config=None):
    #creating and configuring app
    app = Flask(__name__, instance_relative_config=True)
        #__name__ is name of current Python module; tells app where to set paths
        #instance_relative_config tells app config files are in instance folder
    
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'),
        #
    )

    if test_config is None:
        #load instance config file, when not testing
        app.config.from_pyfile('config.py', silent = True)
    else:
        #load config if passed
        app.config.from_mapping(test_config)

    #check instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    
    #import db module
    from . import db
    db.init_app(app)
    
    #import auth blueprint and register (module)
    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint = 'index')


    #################################
    # end of func is return app
    return app


     