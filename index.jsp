<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<title>DBConnection</title>
</head>
<body>
<%
    String status = request.getParameter("status");
    String alertMsg = null;
    if ("success".equals(status)) {
        alertMsg = "User created";
    } else if ("exists".equals(status)) {
        alertMsg = "user already exists";
    } else if ("failed".equals(status)) {
        alertMsg = "something went wrong";
    } else if ("create".equals(status)) {
        alertMsg = "more users are required to create repo";
    }
    if (alertMsg != null) {
%>
<script type="text/javascript">alert("<%= alertMsg %>");</script>
<%
    }
%>
<h2>Create User</h2>
<form action="CreateUser" method="post">
    <input type="text" id="userName" name="userName" />
    <input type="submit" id="create" value="Create" />
</form>
</body>
</html>
