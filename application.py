from bottle import route, post, run, template, redirect, request

import database

@route("/")
def get_index():
    redirect("/home")

@route("/home")
def get_home():
    # Assuming you have functions to get users and events from the database
    users = database.get_items()
    events = database.get_events()
    #return template("home.tpl", interactive_db=users)
    return template("home.tpl", users=users, events=events)

@route("/list")
def get_list():
    users = database.get_items()
    return template("list.tpl", interactive_db=users)

@route("/add")
def get_add():
    return template("add_item.tpl")

@post("/add")
def post_add():
    user = request.forms.get("username")
    database.add_item(user)
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
    database.delete_item(id)
    redirect("/list")

@route("/update/<id>")
def get_update(id):
    items = database.get_items(id)
    if len(items) != 1:
        redirect("/list")
    description = items[0]['username']
    return template("update_item.tpl", id=id, description=description)

@post("/update")
def post_update():
    description = request.forms.get("username")
    id = request.forms.get("id")
    database.update_item(id, description)
    redirect("/list")

run(host='localhost', port=8080)