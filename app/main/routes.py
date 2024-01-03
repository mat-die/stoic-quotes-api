from app.main import bp
from .. import db


@bp.route("/")
def get_quotes():
    quotes = []
    conn = db.get_db()
    rows = conn.execute("SELECT * FROM quotes;").fetchall()
    conn.close()

    for row in rows:
        quote = {}
        quote["author"] = row["author"]
        quote["quote"] = row["quote"]
        quotes.append(quote)

    return quotes


@bp.route("/random")
def get_random_quote():
    conn = db.get_db()
    random_quote = conn.execute(
        "SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1;"
    ).fetchone()
    conn.close()

    return dict(random_quote)
