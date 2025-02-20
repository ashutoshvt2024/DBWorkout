import React, { useEffect, useState } from "react";
import api from "../services/api"; // Axios instance for API requests
import "../Styles/SessionManagement.css"; // CSS styles

function SessionManagement() {
  const [sessions, setSessions] = useState([]);
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [showEditForm, setShowEditForm] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [currentSession, setCurrentSession] = useState(null);
  const [newSession, setNewSession] = useState({
    course_id: "",
    session_name: "",
    session_date: "",
  });

  // Fetch courses for dropdown
  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    try {
      const response = await api.get("/courses");
      setCourses(response.data.courses);
    } catch (error) {
      console.error("Error fetching courses:", error);
    }
  };

  // Fetch sessions based on selected course
  useEffect(() => {
    if (selectedCourse) fetchSessions(selectedCourse);
  }, [selectedCourse]);

  const fetchSessions = async (courseId) => {
    try {
      const response = await api.get(`/sessions?course_id=${courseId}`);
      setSessions(response.data.sessions);
    } catch (error) {
      console.error("Error fetching sessions:", error);
    }
  };

  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewSession({ ...newSession, [name]: value });
  };

  // Create new session
  const handleCreateSession = async () => {
    try {
      const payload = { ...newSession, course_id: selectedCourse };
      await api.post("/sessions", payload);
      fetchSessions(selectedCourse);
      setShowForm(false);
    } catch (error) {
      console.error("Error creating session:", error);
    }
  };

  // Open edit form
  const openEditForm = (session) => {
    setCurrentSession(session);
    setShowEditForm(true);
  };

  // Update session
  const handleUpdateSession = async () => {
    try {
      await api.put(`/sessions/${currentSession.session_id}`, currentSession);
      fetchSessions(selectedCourse);
      setShowEditForm(false);
    } catch (error) {
      console.error("Error updating session:", error);
    }
  };

  // Open delete confirmation
  const openDeleteConfirm = (session) => {
    setCurrentSession(session);
    setShowDeleteConfirm(true);
  };

  // Delete session
  const handleDeleteSession = async () => {
    try {
      await api.delete(`/sessions/${currentSession.session_id}`);
      fetchSessions(selectedCourse);
      setShowDeleteConfirm(false);
    } catch (error) {
      console.error("Error deleting session:", error);
    }
  };

  return (
    <div className="session-management">
      <h1>Session Management</h1>

      {/* Course Selection Dropdown */}
      <select value={selectedCourse} onChange={(e) => setSelectedCourse(e.target.value)}>
        <option value="">Select Course</option>
        {courses.map((course) => (
          <option key={course.course_id} value={course.course_id}>
            {course.course_name}
          </option>
        ))}
      </select>

      <button className="create-btn" onClick={() => setShowForm(true)} disabled={!selectedCourse}>
        + Create Session
      </button>

      {/* Session List */}
      <table className="session-table">
        <thead>
          <tr>
            <th>Session Name</th>
            <th>Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {sessions.map((session) => (
            <tr key={session.session_id}>
              <td>{session.session_name}</td>
              <td>{session.session_date}</td>
              <td>
                <button className="edit-btn" onClick={() => openEditForm(session)}>Edit</button>
                <button className="delete-btn" onClick={() => openDeleteConfirm(session)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Create Session Modal */}
      {showForm && (
        <div className="modal">
          <div className="modal-content">
            <h2>Create Session</h2>
            <input type="text" name="session_name" placeholder="Session Name" onChange={handleInputChange} />
            <input type="date" name="session_date" onChange={handleInputChange} />
            <button onClick={handleCreateSession}>Create</button>
            <button onClick={() => setShowForm(false)}>Cancel</button>
          </div>
        </div>
      )}

      {/* Edit Session Modal */}
      {showEditForm && (
        <div className="modal">
          <div className="modal-content">
            <h2>Edit Session</h2>
            <input
              type="text"
              name="session_name"
              value={currentSession.session_name}
              onChange={(e) => setCurrentSession({ ...currentSession, session_name: e.target.value })}
            />
            <button onClick={handleUpdateSession}>Update</button>
            <button onClick={() => setShowEditForm(false)}>Cancel</button>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="modal">
          <div className="modal-content">
            <h2>Are you sure you want to delete this session?</h2>
            <button onClick={handleDeleteSession}>Yes</button>
            <button onClick={() => setShowDeleteConfirm(false)}>No</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default SessionManagement;