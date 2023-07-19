import os
from flask import Flask, request, render_template, redirect
from lib.database_connection import get_flask_database_connection
from lib.space_repository import *
from lib.user import *
from lib.user_repository import UserRepository
from lib.request_repository import *

# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==

@app.route('/index', methods=['POST'])
def post_user_on_index():
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)
    user = User(None, request.form['username'], request.form['user_password'], request.form['email'])
    repository.create(user)
    return render_template('spaces/book.html')

@app.route('/login', methods=['GET'])
def get_login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def existing_user_log_in():
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)
    user_email = request.form['email']
    user_password = request.form['user_password']
    repository.find_user(user_email)
    if repository.username_and_password_match_user(user_email, user_password) == True:
        return render_template('spaces/book.html')
    return "Incorrect username or password. Try Again"

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5000/index
@app.route('/index', methods=['GET'])
def get_index():
    return render_template('index.html')

@app.route('/book_space', methods = ["GET"])
def get_all_listings():
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    spaces = repository.all()
    return render_template('/spaces/book.html', spaces=spaces)

@app.route("/spaces/new_space", methods=["GET"])
def get_new_space():
    return render_template("/spaces/new_space.html")

@app.route('/spaces/new_space', methods=["POST"])
def post_new_space():
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    availability = request.form['availability']
    user_id = request.form['user_id']
    new_space = Space(None, name, description, price, availability, user_id)
    repository.create(new_space)
    return redirect(f"/spaces/{new_space.id}")

@app.route('/spaces/<int:id>')
def get_single_space_page(id):
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    spaces = repository.find(id)
    space = spaces[0]
    dates = space.availability.split(",")
    return render_template("spaces/show_space.html", space=space, dates=dates)

# @app.route('/spaces/<int:id>/confirm_booking_request')
# def confirm_booking_request(date):
#     connection = get_flask_database_connection(app)
#     space_repository = SpaceRepository(connection)
#     request_repository = RequestRepository(connection)
#     request_repository.create()


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))

