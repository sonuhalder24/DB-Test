package com;

import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.UUID;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class CreateUser extends HttpServlet {
	private static final long serialVersionUID = 1L;

	public CreateUser() {
		super();
	}

	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		response.getWriter().append("Served at: ").append(request.getContextPath());
	}

	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		String userName = request.getParameter("userName");
		String status = "failed";
		Connection conn = null;
		try {
			conn = getConnection();
			PreparedStatement checkStmt = conn.prepareStatement(
				"SELECT * FROM users WHERE userName = ?");
			checkStmt.setString(1, userName);
			ResultSet rs = checkStmt.executeQuery();
			if (rs.next()) {
				status = "exists";
			} else {
				String userId = UUID.randomUUID().toString();
				PreparedStatement insertStmt = conn.prepareStatement(
					"INSERT INTO users (userId, userName) VALUES (?, ?)");
				insertStmt.setString(1, userId);
				insertStmt.setString(2, userName);
				insertStmt.executeUpdate();
				status = "success";
			}
		} catch (Exception e) {
			status = "failed";
			e.printStackTrace();
		} finally {
			if (conn != null) {
				try { conn.close(); } catch (Exception e) {}
			}
		}
		response.sendRedirect("index.jsp?status=" + status);
	}

	private Connection getConnection() throws Exception {
		try {
			Class.forName("com.mysql.cj.jdbc.Driver");
		} catch (ClassNotFoundException e) {
			Class.forName("com.mysql.jdbc.Driver");
		}
		try {
			return DriverManager.getConnection(
				"jdbc:mysql://localhost:3306/DBConnection?useSSL=false&allowPublicKeyRetrieval=true",
				"root", "mysql");
		} catch (Exception e) {
			return DriverManager.getConnection(
				"jdbc:mysql://localhost:3306/DBConnection",
				"root", "mysql");
		}
	}
}
