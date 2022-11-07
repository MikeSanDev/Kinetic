from flask_app import app

from flask_app.controllers import users, surveys

if __name__ == "__main__":
    app.run(debug=True)
