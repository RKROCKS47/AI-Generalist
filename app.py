# app.py
from flask import Flask
from web.routes import init_routes


def create_app():
    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"] = "uploads"
    app.config["TEMPLATES_DIR"] = "templates"
    init_routes(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
