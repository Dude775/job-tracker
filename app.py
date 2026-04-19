from flask import Flask
from db import init_db
from routes.applications import applications_bp
from errors import errors_bp

app = Flask(__name__)

init_db(app)

app.register_blueprint(applications_bp)
app.register_blueprint(errors_bp)

if __name__ == "__main__":
    app.run(debug=True)
