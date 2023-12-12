<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Calendar</title>
    <link rel="stylesheet" type="text/css" href="styles.css">
    <style>
        body {
            display: flex;
            justify-content: space-between;
        }

        section {
            width: 45%;
            padding: 10px;
            border: 1px solid #ccc;
            margin: 10px;
        }

        form {
            display: flex;
            flex-direction: column;
        }

        label {
            margin-bottom: 5px;
        }

        input, textarea {
            margin-bottom: 10px;
        }

        button {
            cursor: pointer;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            color:#606060
        }

        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }

        th {
            background-color: #f2f2f2;
        }
        body {
        display: flex;
        justify-content: space-between;
        align-items: center; /* Center items vertically */
        }

        div {
        text-align: right; /* Align text to the right */
        margin: 10px; /* Add margin for spacing */
        }

        p {
        margin: 0; /* Remove default margin for the paragraph */
        }

        a {
        margin-left: 10px; /* Add margin between login link and welcome message */
        }
    </style>
</head>
<body>
    <h1>Interactive Calendar</h1>

    <!-- Users and Events Section -->
    <section>
    </head>
        % if username:
            <h1>Welcome, {{ username }}!</h1>
        % else:
            <h1>Welcome!</h1>
        % end

        <h2>Events</h2>
        <div class="event-theme">
        <table>
            <tr>
                <th>Title</th>
                <th>Description</th>
                <th>Start Datetime</th>
                <th>End Datetime</th>
                <th>Location</th>
                <th>Update Event</th>
                <th>Delete Event</th>
            </tr>
            % for event in events:
                <tr>
                    <td>{{event['title']}}</td>
                    <td>{{event['description']}}</td>
                    <td>{{event['start_datetime']}}</td>
                    <td>{{event['end_datetime']}}</td>
                    <td>{{event['location']}}</td>
                    <td><a href="/update_event/{{str(event['id'])}}">update</a></td>
                    <td><a href="/delete_event/{{str(event['id'])}}">delete</a></td>
                </tr>
            % end
        </table>
        </div>
        <!-- Update Event Form -->
    <h2>Update Event</h2>
    <form action="/update_event/{{str(event['id'])}}" method="post">
        <label for="title">Title:</label>
        <input type="text" name="title" value="{{ event['title'] }}" required>
        <label for="description">Description:</label>
        <textarea name="description" required>{{ event['description'] }}</textarea>
        <label for="start_datetime">Start Date and Time:</label>
        <input type="text" name="start_datetime" value="{{ event['start_datetime'] }}" required>
        <label for="end_datetime">End Date and Time:</label>
        <input type="text" name="end_datetime" value="{{ event['end_datetime'] }}" required>
        <label for="location">Location:</label>
        <input type="text" name="location" value="{{ event['location'] }}" required>
        <button type="submit">Update Event</button>
    </form>
    </section>

    <!-- CRUD Section with Table -->
    <!-- Link to Create User Page -->
   
    <section>
        <h2>Create User Page</h2>
        <div>
            % if username:
                <p>Welcome, {{ username }}! <a href="/logout">Logout</a></p>
            % else:
                <p><a href="/login">Login</a></p>
            % end
        </div>
        <a href="/add">Create User</a>
            <!-- Add Event Form -->
            
            <tr>
                <td>
                    <h2>Add Event</h2>
                    <form action="/create_event" method="post">
                        <label for="title">Title:</label>
                        <input type="text" name="title" required>
                        <label for="description">Description:</label>
                        <textarea name="description" required></textarea>
                        <label for="start_datetime">Start Date and Time:</label>
                        <input type="text" name="start_datetime" required>
                        <label for="end_datetime">End Date and Time:</label>
                        <input type="text" name="end_datetime" required>
                        <label for="location">Location:</label>
                        <input type="text" name="location" required>
                        <button type="submit">Add Event</button>
                    </form>
                </td>
            </tr>
        </table>
    </section>
</body>
</html>
