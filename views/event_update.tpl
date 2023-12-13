<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }

        form {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 300px;
            text-align: center; /* Center the form contents */
        }

        h2 {
            color: #333;
        }

        label {
            display: block;
            margin-bottom: 8px;
            text-align: left; /* Align labels to the left */
        }

        input,
        textarea {
            width: 100%;
            padding: 8px;
            margin-bottom: 12px;
            box-sizing: border-box;
        }

        button {
            background-color: #4caf50;
            color: #fff;
            padding: 10px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }

        button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <form action="/update_event/{{str(events['_id'])}}" method="post">
        <h2>Update Event</h2>
        <label for="title">Title:</label>
        <input type="text" name="title" value="{{str(events['title'])}}" required>
        <label for="description">Description:</label>
        <textarea name="description" required>{{str(events['description'])}}</textarea>
        <label for="start_datetime">Start Date and Time:</label>
        <input type="text" name="start_datetime" value="{{str(events['start_datetime'])}}" required>
        <label for="end_datetime">End Date and Time:</label>
        <input type="text" name="end_datetime" value="{{str(events['end_datetime'])}}" required>
        <label for="location">Location:</label>
        <input type="text" name="location" value="{{str(events['location'])}}" required>
        <button type="submit">Update Event</button>
    </form>
</body>
</html>
