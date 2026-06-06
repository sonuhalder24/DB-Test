<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="java.sql.*,java.io.*,java.util.*" %>
<!DOCTYPE html>
<html>
<head><title>Create Repo</title></head>
<body>
<%@ include file="Header.jsp" %>
<h2>Create Repository</h2>
<%
    List<String[]> users = new ArrayList<String[]>();
    Connection conn = null;
    try {
        try { Class.forName("com.mysql.cj.jdbc.Driver"); } catch (ClassNotFoundException e1) { Class.forName("com.mysql.jdbc.Driver"); }
        try {
            conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/DBConnection?useSSL=false&allowPublicKeyRetrieval=true", "root", "mysql");
        } catch (Exception e1) {
            conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/DBConnection", "root", "mysql");
        }
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery("SELECT userId, userName FROM users");
        while (rs.next()) {
            users.add(new String[]{rs.getString("userId"), rs.getString("userName")});
        }
    } catch (Exception e) {
        e.printStackTrace();
    } finally {
        if (conn != null) try { conn.close(); } catch (Exception e) {}
    }
%>
<form action="CreateRepo" method="post">
    <label>Who are you?</label>
    <select name="userId">
    <% for (String[] u : users) { %>
        <option value="<%= u[0] %>"><%= u[1] %></option>
    <% } %>
    </select><br/>
    <label>Repo Name:</label>
    <input type="text" name="RepoName" /><br/>
    <label>Repo Description:</label>
    <input type="text" name="RepoDesc" /><br/>
    <label>Assign Developer:</label>
    <select name="RepoDev">
    <% for (String[] u : users) { %>
        <option value="<%= u[0] %>"><%= u[1] %></option>
    <% } %>
    </select><br/>
    <input type="submit" value="Create Repo" />
</form>
</body>
</html>
