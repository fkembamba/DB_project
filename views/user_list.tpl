<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User List</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 20px;
        }

        h2 {
            color: #333;
        }

        table {
            width: 80%;
            margin: 20px auto;
            border-collapse: collapse;
        }

        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }

        th {
            background-color: #f2f2f2;
        }

        a {
            text-decoration: none;
            color: #007BFF;
            margin-right: 10px;
        }

        a:hover {
            color: #0056b3;
        }
    </style>
</head>
<body>
    <h2>User List</h2>
    <hr/>
    <table>
        <tr>
            <th>Username</th>
            <th>Update</th>
            <th>Delete</th>
        </tr>
        % for item in interactive_db:
            <tr>
                <td>{{item['username']}}</td>
                <td><a href="/update_user/{{str(item['id'])}}">Update</a></td>
                <td><a href="/delete_user/{{str(item['id'])}}">Delete</a></td>
            </tr>
        % end
    </table>
    <hr/>
    <a href="/add_user">Add new item</a>
</body>
</html>
