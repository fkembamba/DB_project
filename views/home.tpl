<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Calendar</title>
    <link rel="stylesheet" type="text/css" href="styles.css">
</head>
<body>
    <h1>Interactive Calendar</h1>

    <!-- Users Section -->
    <section>
        <h2>Users</h2>
        <ul>
            % for user in users:
                <tr>
                    <li>
                        <td>{{user['username']}}</td>
                    </li>
                </tr>
            % end
        </ul>
    </section>

    <!-- Events Section -->
    <section>
        <h2>Events</h2>
        <table>
            <tr>
                <th>Title</th>
                <th>Description</th>
                <th>Start Datetime</th>
                <th>End Datetime</th>
                <th>Location</th>
            </tr>
            % for event in events:
                <tr>
                    <td>{{event['title']}}</td>
                    <td>{{event['description']}}</td>
                    <td>{{event['start_datetime']}}</td>
                    <td>{{event['end_datetime']}}</td>
                    <td>{{event['location']}}</td>
                </tr>
            % end
        </table>
    </section>

    <!-- Add User Form -->
    <section>
        <h2>Add User</h2>
        <form action="/add" method="post">
            <label for="username">Username:</label>
            <input type="text" name="username" required>
            <button type="submit">Add User</button>
        </form>
    </section>

    <!-- Add Event Form -->
    <section>
        <h2>Add Event</h2>
        <form action="/add_event" method="post">
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
    </section>
</body>
</html>
