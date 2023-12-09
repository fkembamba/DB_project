<html>
<body>
<h2>User List</h2>
<hr/>
<table>
% for item in interactive_db:
  <tr>
    <td>{{item['username']}}</td>
    <td><a href="/update/{{str(item['id'])}}">update</a></td>
    <td><a href="/delete/{{str(item['id'])}}">delete</a></td>
  </tr>
% end
</table>
<hr/>
<a href="/add">Add new item</a>
</body>
</html>