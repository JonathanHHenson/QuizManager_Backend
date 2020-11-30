import config as cfg
from urllib.parse import quote_plus
from flask import Flask, send_from_directory
from quiz_routes import quiz_routes
from login_routes import login_routes
from datetime import timedelta
import user_session_manager
import models
import os


def get_database_url():
    config = cfg.Config('database.cfg')

    username = quote_plus(config["username"])
    password = quote_plus(config["password"])
    host = config["host"]
    port = config["port"]
    database = quote_plus(config["database"])

    return f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'


app = Flask(__name__, static_folder='static', static_url_path='/')
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
models.db.init_app(app)
with app.app_context():
    models.db.create_all()

user_session_manager.start_cleaning(timedelta(minutes=30))

app.register_blueprint(quiz_routes)
app.register_blueprint(login_routes)


@app.route("/")
@app.route("/<string:path>")
@app.route("/<path:path>")
@app.route("/quiz/<quiz_id>")
@app.route("/quiz/<quiz_id>/_edit")
def index(path=None, quiz_id=None):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run(debug=True)