from bottle import route, post, run, template, redirect, request

import database

@route("/")
def get_index():
    redirect("/list")

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
    redirect("/list")

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