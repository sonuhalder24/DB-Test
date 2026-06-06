package com;

import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.util.UUID;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class CreateRepo extends HttpServlet {
	private static final long serialVersionUID = 1L;

	public CreateRepo() {
		super();
	}

	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		response.getWriter().append("Served at: ").append(request.getContextPath());
	}

	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		String userId = request.getParameter("userId");
		String repoName = request.getParameter("RepoName");
		String repoDesc = request.getParameter("RepoDesc");
		String repoDev = request.getParameter("RepoDev");

		Connection conn = null;
		try {
			conn = getConnection();

			String repoId = UUID.randomUUID().toString();
			PreparedStatement stmt = conn.prepareStatement(
				"INSERT INTO repos (repoId, userId, repoName, repoDesc, RepoDev) VALUES (?, ?, ?, ?, ?)");
			stmt.setString(1, repoId);
			stmt.setString(2, userId);
			stmt.setString(3, repoName);
			stmt.setString(4, repoDesc);
			stmt.setString(5, repoDev);
			stmt.executeUpdate();
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			if (conn != null) {
				try { conn.close(); } catch (Exception e) {}
			}
		}
	}

	private Connection getConnection() throws Exception {
		Class.forName("com.mysql.cj.jdbc.Driver");
		try {
			return DriverManager.getConnection(
				"jdbc:mysql://localhost:3306/DBConnection?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC",
				"root", "mysql");
		} catch (Exception e) {
			return DriverManager.getConnection(
				"jdbc:mysql://localhost:3306/DBConnection?serverTimezone=UTC",
				"root", "mysql");
		}
	}
}
