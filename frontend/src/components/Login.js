import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { useUser } from "../context/UserContext";
import { jwtDecode } from "jwt-decode";
import "../Styles/Auth.css";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { user, setUser } = useUser();

  // ✅ Check for token on page load
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      try {
        const decoded = jwtDecode(token);
        const userData = JSON.parse(decoded.sub); // Extract stored user data
        setUser(userData);
        navigate(userData.role === "professor" ? "/instructor-panel" : "/dashboard");
      } catch (error) {
        console.error("Invalid token:", error);
        localStorage.removeItem("token"); // Remove corrupted token
      }
    }
  }, [navigate, setUser]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post("/login", { email, password });

      console.log("Login API Response:", response.data); // ✅ Debugging

      if (!response.data.access_token) {
        throw new Error("Missing access token in response");
      }

      const token = response.data.access_token;
      localStorage.setItem("token", token);

      const decoded = jwtDecode(token);
      console.log("Decoded token:", decoded);

      const userData = JSON.parse(decoded.sub); // ✅ Extract stored user data

      if (!userData.user_id || !userData.role) {
        throw new Error("Invalid token format");
      }

      localStorage.setItem("user", JSON.stringify(userData));
      setUser(userData);

      // ✅ Redirect based on role
      navigate(userData.role === "professor" ? "/instructor-panel" : "/dashboard");

    } catch (err) {
      console.error("Login error:", err);
      setError(err.response?.data?.error || "Login failed");
    }
  };

  return (
    <div className="auth-container">
      <h1>Login</h1>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;