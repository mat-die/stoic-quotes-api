import os

import sqlite3
from flask import Flask

from . import db


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'quotes.db'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    def connect_db():
        rv = sqlite3.connect(app.config['DATABASE'])
        rv.row_factory = sqlite3.Row
        return rv

    @app.route("/")
    def get_quotes():
        quotes = []
        conn = connect_db()
        rows = conn.execute("SELECT * FROM quotes;").fetchall()
        conn.close()

        for row in rows:
            quote = {}
            quote["author"] = row["author"]
            quote["quote"] = row["quote"]
            quotes.append(quote)

        return quotes


    @app.route('/random-quote')
    def get_random_quote():
        conn = connect_db()
        random_quote = conn.execute("SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1;").fetchone()
        conn.close()

        return dict(random_quote)


    db.init_app(app)

    return app