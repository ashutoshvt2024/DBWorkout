import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../services/api";
import { useUser } from "../context/UserContext";
import {jwtDecode} from "jwt-decode";
import "../Styles/Auth.css";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { setUser } = useUser();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("/login", { email, password });

      const token = response.data.access_token;
      localStorage.setItem("token", token);
      const decoded = jwtDecode(token);

      // Extract and save user data
      const userData = {
        userId: decoded.sub.user_id,
        role: decoded.sub.role,
      };
      localStorage.setItem("user", JSON.stringify(userData));
      setUser(userData);

      navigate(userData.role === "professor" ? "/instructor-panel" : "/dashboard");
    } catch (err) {
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