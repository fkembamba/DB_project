from bottle import route, post, run, template, redirect, request, response
from bson import ObjectId  # Import ObjectId from bson module

import database
# Set your secret key
secret_key = "alpha@2023"

def check_credentials(username, password):
    users = database.get_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
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
    color_code = request.forms.get("color_code")

    user = check_credentials(username, password)
    if user:
        current_user = username
        user = database.get_user_by_credentials(username, password)
        # Set cookies or session variables to store user information
        response.set_cookie("username", username)
        response.set_cookie("password", password)
        response.set_cookie("color_code", color_code, secret=secret_key)
        # Get the user_id from the user object
        user_id = str(user['_id'])

        # Set the user ID in cookies
        response.set_cookie("user_id", user_id)
        return redirect("/home")
    return redirect("/login")


@route("/create_user")
def create_user():
    return template("create_user.tpl")
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
    # Check if the username and password are correct 
    username = request.get_cookie("username")
    password = request.get_cookie("password")
    color_code = request.get_cookie("color_code")

    if database.get_user_by_credentials(username, password):
        # get users and events from the database
        users = database.get_users()
        events = database.get_events()
        return template("home.tpl", users=users, events=events, username = username, message="", id = id, color_code = color_code)
    else:
        # Redirect to the login page if credentials are incorrect
        redirect("/login")

@route("/user_list")
def get_list():
    users = database.get_users()
    return template("user_list.tpl", interactive_db=users)

@route("/add_user")
def get_add():
    return template("create_user.tpl")

@post("/add_user")
def post_add():
    username = request.forms.get("username")
    password = request.forms.get("password")
    confirm_password = request.forms.get("confirm_password")
    color_code = request.forms.get("color_code")

    if password == confirm_password:
        check = database.add_users(username, password, color_code)
        if check:
            umessage = "User created successfully"
            redirect("/home?message=" + umessage)  # Pass the message as a query parameter
        else:
            umessage = "User creation failed"
            redirect("/home?message=" + umessage)  # Pass the message as a query parameter
    else:
        umessage = "Unmatched passwords"
        redirect("/create_user?message=" + umessage)  # Pass the message as a query parameter
        

@route("/add_event")
def get_addevent():
    return template("home.tpl")

@post("/add_event")
def post_addevent(user_id):
    title = request.forms.get("title")
    description = request.forms.get("description")
    start_datetime= request.forms.get("start_datetime")
    end_datetime = request.forms.get("end_datetime")
    location = request.forms.get("location")
    created_by = ObjectId(user_id)
    database.add_event(title, description, start_datetime, end_datetime, location, created_by)
    redirect("/home")

@route("/delete_user/<id>")
def get_delete(id):
    database.delete_users(id)
    redirect("/user_list")

@route("/update_user/<id>")
def get_update(id):
    items = database.get_users(id)
    if len(items) != 1:
        redirect("/user_list")
    description = items[0]['username']
    return template("user_update.tpl", id=id, description=description)

@post("/update")
def post_update():
    description = request.forms.get("username")
    id = request.forms.get("id")
    database.update_users(id, description)
    redirect("/user_list")

@route('/create_event', method='POST')
def create_event():
    # Retrieve user ID stored in cookies
    user_id = request.get_cookie("user_id")
    print("Let's check here", user_id)

    # Check if the user is logged in
    if user_id:
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
            "created_by": ObjectId(user_id)  # Convert user_id to ObjectId
        }

        # Insert the event document into the MongoDB collection
        result = database.add_event(event_document)

        if result:
            # Event creation successful
            message = "Event created successfully!"
        else:
            # Event creation failed
            message = "Failed to create the event."

    else:
        # User not logged in
        message = "You need to be logged in to create an event."
    # Retrieve the events and users (you may have different logic here)
    events = database.get_events()
    users = database.get_users()

    # Pass the events, users, and message to the template
    return template('home', events=events, users=users, message=message, username=user_id)
    
@route('/delete_event/<event_id>', method='GET')
def delete_event(event_id):
    # Assuming you have a user ID stored in cookies
    user_id = request.get_cookie("user_id")

    # Check if the user is logged in
    if user_id:
        # Convert the event_id to ObjectId
        event_id_obj = ObjectId(event_id)

        # Check if the event exists and was created by the logged-in user
        event = database.event_collection.find_one({"_id": event_id_obj, "created_by": ObjectId(user_id)})

        if event:
            # Delete the event
            result = database.event_collection.delete_one({"_id": event_id_obj})

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

@route('/update_event/<event_id>', method=['GET', 'POST'])
def update_event(event_id):
    #global event_collection  # Add this line to access the global variable

    # Assuming you have a user ID stored in cookies
    user_id = request.get_cookie("user_id")

    # Check if the user is logged in
    if user_id:
        # Convert the event_id to ObjectId
        event_id_obj = ObjectId(event_id)

        # Check if the event exists and was created by the logged-in user
        event = database.event_collection.find_one({"_id": event_id_obj, "created_by": ObjectId(user_id)})

        if event:
            # Get updated event details from the form or request data
            title = request.forms.get('title')
            description = request.forms.get('description')
            start_datetime = request.forms.get('start_datetime')
            end_datetime = request.forms.get('end_datetime')
            location = request.forms.get('location')

            # Update the event document
            result = database.event_collection.update_one(
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
    
@route('/load_update_page/<event_id>')
def load_update_page(event_id):
    # Retrieve event details based on event_id
    # You may need to adapt this to your database retrieval logic
    #print("From load_update_page",event_id)
    event = database.get_event_details(event_id)

    # Render the update page with the event details
    return template('event_update', events=event)

@route('/update_event/<event_id>', method='post')
def update_event(event_id):
    
    updated_event = database.update_event_details(event_id, request.forms)
    
    if updated_event:
        message = "Event updated successfully"
    else:
        message = "Update failed"

    # Redirect to the events page with a message
    return redirect('/home?message=' + message)



@route('/search_events', method='GET')
def event_search():
    search_query = request.query.get('search_query', '')
    user_id = request.get_cookie("user_id")  # Assuming user authentication is implemented

    if user_id:
        # Assuming search_events returns a list of events based on the search query and user ID
        search_results = database.search_events(search_query, user_id)
        
        # Pass the search query and results to the template
        return template('search', search_query=search_query, search_results=search_results, username=user_id)
    else:
        # Redirect to login if the user is not logged in
        return template('login')  # Update with your actual login template route   

run(host='localhost', port=8080)