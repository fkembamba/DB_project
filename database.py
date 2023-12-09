from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from bson.objectid import ObjectId

uri= "mongodb+srv://Kembamba:kem2023@cluster0.ebkomh4.mongodb.net/?retryWrites=true&w=majority"

#uri = "mongodb://localhost:27017"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

interactive_db = client.interactive_calendar

def setup_database():
    interactive_db.drop_collection(interactive_db.User)
    items_collection = interactive_db.User
    for item in ['Tina', 'Fred', 'Abby', 'Alvin', 'Davey']:
        items_collection.insert_one({"username":item})

def get_items(id=None):
    items_collection = interactive_db.User
    if id == None:
        items = items_collection.find({})
    else:
        items = items_collection.find({"_id":ObjectId(id)})
    items = list(items)
    for item in items:
        item["id"] = str(item["_id"])
    return items


def add_item(description):
    items_collection = interactive_db.User
    items_collection.insert_one({"username":description})

def delete_item(id):
    user_collection = interactive_db.User
    user_collection.delete_one({"_id":ObjectId(id)})

def update_item(id, username):
    user_collection = interactive_db.User
    where = {"_id": ObjectId(id)}
    updates = { "$set": { "username": username } }
    user_collection.update_one(where, updates)

def test_setup_database():
    print("testing setup_database()")
    setup_database()
    items = get_items()
    assert len(items) == 5
    descriptions = [item['username'] for item in items]
    for description in ['Tina', 'Fred', 'Abby', 'Alvin', 'Davey']:
        assert description in descriptions

def test_get_items():
    print("testing get_items()")
    setup_database()
    items = get_items()
    assert type(items) is list
    assert len(items) > 0
    for item in items:
        assert 'id' in item
        assert type(item['id']) is str
        assert 'username' in item
        assert type(item['username']) is str
    example_id = items[0]['id']
    example_description = items[0]['username']
    items = get_items(example_id)
    assert len(items) == 1
    assert example_id == items[0]['id']
    assert example_description == items[0]['username']

def test_add_item():
    print("testing add_item()")
    setup_database()
    items = get_items()
    original_length = len(items)
    add_item("Kembamba")
    items = get_items()
    assert len(items) == original_length + 1
    descriptions = [item['username'] for item in items]
    assert "Kembamba" in descriptions


def test_delete_item():
    print("testing delete_item()")
    setup_database()
    items = get_items()
    original_length = len(items)
    deleted_description = items[1]['username']
    deleted_id = items[1]['id']
    delete_item(deleted_id)
    items = get_items()
    assert len(items) == original_length - 1
    for item in items:
        assert item['id'] != deleted_id
        assert item['username'] != deleted_description

def test_update_item():
    print("testing update_item()")
    setup_database()
    items = get_items()
    original_description = items[1]['username']
    original_id = items[1]['id']
    update_item(original_id,"new-description")
    items = get_items()
    found = False
    for item in items:
        if item['id'] == original_id:
            assert item['username'] == "new-description"
            found = True
    assert found


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