from bottle import route, post, run, template, redirect, request, response

import database

@route("/")
def get_index():
    redirect("/login")

@post("/login")
def post_login():
    username = request.forms.get("username")
    password = request.forms.get("password")

    if username:
        # Set cookies or session variables to store user information
        response.set_cookie("username", username)
        response.set_cookie("password", password)

        # Redirect to the home page
        redirect("/home")
    else:
        # Redirect back to the login page if credentials are incorrect
        redirect("/login")

# Route for rendering the login page
@route("/login")
def get_login():
    return template("login.tpl")

@route("/home")
def get_home():
    # Check if the username and password are correct (you need to implement this logic)
    username = request.get_cookie("username")
    password = request.get_cookie("password")

    if database.get_user_by_credentials(username, password):
        # Assuming you have functions to get users and events from the database
        users = database.get_users()
        events = database.get_events()
        return template("home.tpl", users=users, events=events)
    else:
        # Redirect to the login page if credentials are incorrect
        redirect("/login")

@route("/list")
def get_list():
    users = database.get_users()
    return template("list.tpl", interactive_db=users)

@route("/add")
def get_add():
    return template("create_user.tpl")

@post("/add")
def post_add():
    user = request.forms.get("username")
    database.add_users(user)
    redirect("/home")

@route("/add_event")
def get_addevent():
    return template("home.tpl")

@post("/add_event")
def post_addevent():
    title = request.forms.get("title")
    description = request.forms.get("description")
    start_datetime= request.forms.get("start_datetime")
    end_datetime = request.forms.get("end_datetime")
    location = request.forms.get("location")
    database.add_event(title, description, start_datetime, end_datetime, location)
    redirect("/home")

@route("/delete/<id>")
def get_delete(id):
    database.delete_users(id)
    redirect("/list")

@route("/update/<id>")
def get_update(id):
    items = database.get_users(id)
    if len(items) != 1:
        redirect("/list")
    description = items[0]['username']
    return template("update_item.tpl", id=id, description=description)

@post("/update")
def post_update():
    description = request.forms.get("username")
    id = request.forms.get("id")
    database.update_users(id, description)
    redirect("/list")

run(host='localhost', port=8080)