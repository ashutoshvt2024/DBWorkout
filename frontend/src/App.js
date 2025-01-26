import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Dashboard from "./components/Dashboard";
import Leaderboard from "./components/Leaderboard";
import Login from "./components/Login";
import Workspace from "./components/Workspace";
import InstructorPanel from "./components/InstructorPanel";
import ProtectedRoute from "./components/ProtectedRoute";
import Unauthorized from "./components/Unauthorized";
import { UserProvider } from "./context/UserContext";

function App() {
  return (
    <UserProvider>
      <Router>
        <Navbar />
        <main className="container flex-fill">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute roles={["professor", "student"]}>
                  <Dashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="/leaderboard"
              element={
                <ProtectedRoute roles={["student"]}>
                  <Leaderboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="/workspace"
              element={
                <ProtectedRoute roles={["professor", "student"]}>
                  <Workspace />
                </ProtectedRoute>
              }
            />
            <Route
              path="/instructor-panel"
              element={
                <ProtectedRoute roles={["professor"]}>
                  <InstructorPanel />
                </ProtectedRoute>
              }
            />
            <Route path="/unauthorized" element={<Unauthorized />} />
          </Routes>
        </main>
      </Router>
    </UserProvider>
  );
}

export default App;