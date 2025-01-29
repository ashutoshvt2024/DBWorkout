import axios from "axios";
import { useUser } from "../context/UserContext";

const api = axios.create({
  baseURL: "http://127.0.0.1:5000", // Backend API URL
  headers: {
    "Content-Type": "application/json",
  },
});

// ✅ Automatically include JWT token in all requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
    console.log("🔍 Sending Token in Headers:", token); // ✅ Debugging
  } else {
    console.warn("⚠️ No token found in localStorage");
  }
  return config;
});

// ✅ Auto Logout on Unauthorized Error
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      console.warn("Unauthorized access detected. Logging out...");
      const { logout } = useUser();
      logout(); // Trigger logout
    }
    return Promise.reject(error);
  }
);

export default api;