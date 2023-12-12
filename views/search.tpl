<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Calendar - Search Results</title>
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

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            color: #606060;
        }

        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }

        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>Interactive Calendar - Search Results</h1>

    <!-- Search Results Section -->
    <section>
        <h2>Search Results for '{{ search_query }}'</h2>
        <table>
            <tr>
                <th>Title</th>
                <th>Start Datetime</th>
                <th>End Datetime</th>
                <th>Location</th>
            </tr>
            % for event in search_results:
                <tr>
                    <td>{{ event['title'] }}</td>
                    <td>{{ event['start_datetime'] }}</td>
                    <td>{{ event['end_datetime'] }}</td>
                    <td>{{ event['location'] }}</td>
                </tr>
            % end
        </table>
    </section>

    <!-- Home Link -->
    <div>
        <a href="/home">Back to Home</a>
    </div>
</body>
</html>
