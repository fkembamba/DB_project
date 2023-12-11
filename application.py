from bottle import route, post, run, template, redirect, request, response

import database

def check_credentials(username, password):
    users = database.get_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            print("This checked")
            return True
    return False

@route("/")
def get_index():
    redirect("/login")

@post("/login")
def post_login():
    global current_user
    username = request.forms.get("username")
    password = request.forms.get("password")

    if check_credentials(username, password):
        current_user = username
        # Set cookies or session variables to store user information
        response.set_cookie("username", username)
        response.set_cookie("password", password)
        return redirect("/home")
    return redirect("/login")


# Route for rendering the login page
@route("/login")
def get_login():
    return template("login.tpl")

@route("/logout")
def logout():
    global current_user
    current_user = None
    return redirect("/login")

@route("/home")
def get_home():
    # Check if the username and password are correct (you need to implement this logic)
    username = request.get_cookie("username")
    password = request.get_cookie("password")

    if database.get_user_by_credentials(username, password):
        # Assuming you have functions to get users and events from the database
        users = database.get_users()
        events = database.get_events()
        return template("home.tpl", users=users, events=events, username = username, id = id)
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

@route('/create_event', method='POST')
def create_event():
    # Assuming you have a user ID stored in cookies
    user_id = request.get_cookie("id")
    print("Let's check here")
    # Check if the user is logged in
    if user_id:
        print(user_id)
        # Get event details from the form or request data
        title = request.forms.get('title')
        description = request.forms.get('description')
        start_datetime = request.forms.get('start_datetime')
        end_datetime = request.forms.get('end_datetime')
        location = request.forms.get('location')

        # Create an event document with the created_by field
        event_document = {
            "title": title,
            "description": description,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
            "location": location,
            "created_by": ObjectId(id),
        }

        # Insert the event document into the MongoDB collection
        result = add_event.insert_one(event_document)

        if result.inserted_id:
            # Event creation successful
            return "Event created successfully!"
        else:
            # Event creation failed
            return "Failed to create the event."

    else:
        # User not logged in
        return "You need to be logged in to create an event."
    
@route('/delete_event/<event_id>', method='GET')
def delete_event(event_id):
    # Assuming you have a user ID stored in cookies
    user_id = request.get_cookie("user_id")

    # Check if the user is logged in
    if user_id:
        # Convert the event_id to ObjectId
        event_id_obj = ObjectId(event_id)

        # Check if the event exists and was created by the logged-in user
        event = event_collection.find_one({"_id": event_id_obj, "created_by": ObjectId(user_id)})

        if event:
            # Delete the event
            result = event_collection.delete_one({"_id": event_id_obj})

            if result.deleted_count > 0:
                # Event deletion successful
                return "Event deleted successfully!"
            else:
                # Event deletion failed
                return "Failed to delete the event."

        else:
            # Event not found or not created by the logged-in user
            return "Event not found or you don't have permission to delete it."

    else:
        # User not logged in
        return "You need to be logged in to delete an event."

@route('/update_event/<event_id>', method='POST')
def update_event(event_id):
    # Assuming you have a user ID stored in cookies
    user_id = request.get_cookie("user_id")

    # Check if the user is logged in
    if user_id:
        # Convert the event_id to ObjectId
        event_id_obj = ObjectId(event_id)

        # Check if the event exists and was created by the logged-in user
        event = event_collection.find_one({"_id": event_id_obj, "created_by": ObjectId(user_id)})

        if event:
            # Get updated event details from the form or request data
            title = request.forms.get('title')
            description = request.forms.get('description')
            start_datetime = request.forms.get('start_datetime')
            end_datetime = request.forms.get('end_datetime')
            location = request.forms.get('location')

            # Update the event document
            result = event_collection.update_one(
                {"_id": event_id_obj},
                {"$set": {
                    "title": title,
                    "description": description,
                    "start_datetime": start_datetime,
                    "end_datetime": end_datetime,
                    "location": location,
                }}
            )

            if result.modified_count > 0:
                # Event update successful
                return "Event updated successfully!"
            else:
                # Event update failed
                return "Failed to update the event."

        else:
            # Event not found or not created by the logged-in user
            return "Event not found or you don't have permission to update it."

    else:
        # User not logged in
        return "You need to be logged in to update an event."


run(host='localhost', port=8080)