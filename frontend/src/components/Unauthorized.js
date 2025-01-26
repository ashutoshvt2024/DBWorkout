import React from "react";
import { useNavigate } from "react-router-dom";
import "../Styles/Unauthorized.css"; // Optional for styling

function Unauthorized() {
  const navigate = useNavigate();
  console.log("Redirected to Unauthorized");

  return (
    <div className="unauthorized-container" style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>403 - Unauthorized Access</h1>
      <p>You do not have permission to view this page.</p>
      <button className="btn" onClick={() => navigate("/dashboard")}>
        Go to Dashboard
      </button>
    </div>
  );
}

export default Unauthorized;