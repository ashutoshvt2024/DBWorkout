import React from "react";
import { Navigate } from "react-router-dom";
import { useUser } from "../context/UserContext";

function ProtectedRoute({ children, roles }) {
  const { user } = useUser();

  if (!user) {
    return <Navigate to="/login" />;
  }

  if (roles && !roles.includes(user.role)) {
    console.warn("Unauthorized access attempt by user:", user);
    return <Navigate to="/unauthorized" />;
  }

  return children;
}

export default ProtectedRoute;