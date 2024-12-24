import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Dashboard from './components/Dashboard';
import Leaderboard from './components/Leaderboard';
import Login from './components/Login';
import Workspace from './components/Workspace';
import './App.css';
import Navbar from './components/Navbar';

function App() {
  return (
    <div id="root">
      <Router>
        {/* Navbar is outside the Routes */}
        <Navbar />
        <main className="container flex-fill">
          <Routes>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/leaderboard" element={<Leaderboard />} />
            <Route path="/workspace" element={<Workspace />} />
            <Route path="/login" element={<Login />} />
          </Routes>
        </main>
        
      </Router>
    </div>
  );
}

export default App;