from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import InsertOne

from bson.objectid import ObjectId

uri= "mongodb+srv://Kembamba:kem2023@cluster0.ebkomh4.mongodb.net/?retryWrites=true&w=majority"

#uri = "mongodb://localhost:27017"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

interactive_db = client.interactive_calendar
event_collection = interactive_db.Event


def setup_database():
    interactive_db.drop_collection(interactive_db.User)
    items_collection = interactive_db.User
    for item in ['Tina', 'Fred', 'Abby', 'Alvin', 'Davey']:
        items_collection.insert_one({"username":item})

def get_user_by_credentials(username, password):
    user_collection = interactive_db.User
    if username is None:
        user = user_collection.find({})
    else:
        user = user_collection.find_one({"username": username, "password": password})

    return user  # Return the user document if found, otherwise None

def get_users(id=None):
    users_collection = interactive_db.User
    if id == None:
        users = users_collection.find({})
    else:
        users = users_collection.find({"_id":ObjectId(id)})
    users = list(users)
    for user in users:
        user["id"] = str(user["_id"])
    return users

def get_events(id=None):
    event_collection = interactive_db.Event
    if id is None:
        events = event_collection.find({})
    else:
        events = event_collection.find({"_id": ObjectId(id)}) 
    events = list(events)
    for event in events:
        event["id"] = str(event["_id"])  
    return events

def add_users(description):
    items_collection = interactive_db.User
    if items_collection.insert_one({"username":description}):
        return True
    return False

def add_event(document):
    try:
        event_collection = interactive_db.Event
        result = event_collection.bulk_write([InsertOne(document)])
        
        # Check the result to determine if the insertion was successful
        if result.inserted_count > 0:
            return True  # Event creation successful
        else:
            return False  # Event creation failed

    except Exception as e:
        # Handle exceptions if any
        print(f"Error adding event: {e}")
        return False  # Event creation failed due to an exception

    

def delete_users(id):
    user_collection = interactive_db.User
    user_collection.delete_one({"_id":ObjectId(id)})

def update_users(id, username):
    user_collection = interactive_db.User
    where = {"_id": ObjectId(id)}
    updates = { "$set": { "username": username } }
    user_collection.update_one(where, updates)

def test_setup_database():
    print("testing setup_database()")
    setup_database()
    items = get_users()
    assert len(items) == 5
    descriptions = [item['username'] for item in items]
    for description in ['Tina', 'Fred', 'Abby', 'Alvin', 'Davey']:
        assert description in descriptions

def test_get_users():
    print("testing get_items()")
    setup_database()
    items = get_users()
    assert type(items) is list
    assert len(items) > 0
    for item in items:
        assert 'id' in item
        assert type(item['id']) is str
        assert 'username' in item
        assert type(item['username']) is str
    example_id = items[0]['id']
    example_description = items[0]['username']
    items = get_users(example_id)
    assert len(items) == 1
    assert example_id == items[0]['id']
    assert example_description == items[0]['username']

def test_add_item():
    print("testing add_item()")
    setup_database()
    items = get_users()
    original_length = len(items)
    add_users("Kembamba")
    items = get_users()
    assert len(items) == original_length + 1
    descriptions = [item['username'] for item in items]
    assert "Kembamba" in descriptions


def test_delete_item():
    print("testing delete_item()")
    setup_database()
    items = get_users()
    original_length = len(items)
    deleted_description = items[1]['username']
    deleted_id = items[1]['id']
    delete_users(deleted_id)
    items = get_users()
    assert len(items) == original_length - 1
    for item in items:
        assert item['id'] != deleted_id
        assert item['username'] != deleted_description

def test_update_item():
    print("testing update_item()")
    setup_database()
    items = get_users()
    original_description = items[1]['username']
    original_id = items[1]['id']
    update_users(original_id,"new-description")
    items = get_users()
    found = False
    for item in items:
        if item['id'] == original_id:
            assert item['username'] == "new-description"
            found = True
    assert found

def search_events(query, user_id):
    # Perform a simple search in the 'title' and 'description' fields
    result_cursor = event_collection.find(
        {"$and": [
            {"$or": [{"title": {"$regex": query, "$options": "i"}},
                     {"description": {"$regex": query, "$options": "i"}}]},
            {"created_by": ObjectId(user_id)}  # Filter by the user ID
        ]}
    )

    # Convert MongoDB cursor to a list of dictionaries
    search_results = list(result_cursor)
    
    return search_results


if __name__ == "__main__":
    test_setup_database()
    test_get_items()
    test_add_item()
    test_delete_item()
    test_update_item()

# def delete_item(id):
#     item = Item.select().where(Item.id == id).get()
#     item.delete_instance()

# def update_item(id, description):
#     # item = Item.select().where(Item.id == id).get()
#     # item.description = description
#     # item.save()
#     Item.update({Item.description: description}).where(Item.id == id).execute()

# # def test_update_item():
# #     print("testing update_item()")
# #     setup_database()
# #     items = get_items()
# #     original_description = items[1]['description']
# #     original_id = items[1]['id']
# #     update_item(original_id,"new-description")
# #     items = get_items()
# #     found = False
# #     for item in items:
# #         if item['id'] == original_id:
# #             assert item['description'] == "new-description"
# #             found = True
# #     assert found

# if __name__ == "__main__":
#     test_setup_database()
#     test_get_items()
#     # test_add_item()
#     # test_delete_item()
#     # test_update_item()
#     print("done.")