import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Logout() {
  const navigate = useNavigate();

  useEffect(() => {
    // ✅ Clear user session on logout
    localStorage.removeItem("token");
    localStorage.removeItem("user");

    // ✅ Redirect to login page
    navigate("/login");
  }, [navigate]);

  return (
    <div className="logout-container">
      <h2>Logging out...</h2>
    </div>
  );
}

export default Logout;