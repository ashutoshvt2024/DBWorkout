import React, { useState, useEffect } from "react";
import "../Styles/SessionManagement.css";
import axios from "axios";

function SessionManagement() {
  const [sessions, setSessions] = useState([]);
  const [newSessionName, setNewSessionName] = useState("");
  const [newSchemaId, setNewSchemaId] = useState("");
  const [newCourseInstanceId, setNewCourseInstanceId] = useState("");
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("");
  const [showDeletePrompt, setShowDeletePrompt] = useState(false);
  const [sessionToDelete, setSessionToDelete] = useState(null);
  const [showEditModal, setShowEditModal] = useState(false); // To control edit modal visibility
  const [editingSession, setEditingSession] = useState(null); // Session being edited
  const [tasks, setTasks] = useState([]); // Tasks for a session
  const [showTasksModal, setShowTasksModal] = useState(false); // Task modal visibility
  const [selectedSession, setSelectedSession] = useState(null); // Selected session for viewing tasks
  const [schemas, setSchemas] = useState([]); // Store available schemas
  const [selectedSchemaId, setSelectedSchemaId] = useState(""); // Track selected schema
  const [selectedSessionId, setSelectedSessionId] = useState(null); // Track selected session for association
  // Fetch all sessions
  const fetchSessions = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/sessions/");
      setSessions(response.data.sessions);
      setMessage("");
    } catch (error) {
      setMessageType("error");
      setMessage(`Error fetching sessions: ${error.response?.data?.error || error.message}`);
    }
  };
   // Fetch all schemas
   const fetchSchemas = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/schemas");
      setSchemas(response.data.schemas);
    } catch (error) {
      setMessageType("error");
      setMessage(`Error fetching schemas: ${error.response?.data?.error || error.message}`);
    }
  };
  // Associate schema with a session
  const associateSchema = async () => {
    try {
      if (!selectedSessionId || !selectedSchemaId) {
        setMessageType("error");
        setMessage("Please select a session and schema.");
        return;
      }

      const payload = {
        session_id: selectedSessionId,
        schema_id: selectedSchemaId,
      };

      await axios.put("http://127.0.0.1:5000/sessions/associate-schema", payload);
      setMessageType("success");
      setMessage("Schema associated successfully!");
      fetchSessions(); // Refresh session data
    } catch (error) {
      setMessageType("error");
      setMessage(`Error associating schema: ${error.response?.data?.error || error.message}`);
    }
  };

  // Fetch tasks for a session
  const fetchTasks = async (sessionId) => {
    try {
      const response = await axios.get(`http://127.0.0.1:5000/sessions/${sessionId}/tasks`);
      setTasks(response.data.tasks);
      setSelectedSession(sessionId);
      setShowTasksModal(true); // Show tasks modal
    } catch (error) {
      setMessageType("error");
      setMessage(`Error fetching tasks: ${error.response?.data?.error || error.message}`);
    }
  };

  // Close tasks modal
  const closeTasksModal = () => {
    setShowTasksModal(false);
    setTasks([]);
    setSelectedSession(null);
  };

  // Create a new session
  const createSession = async () => {
    try {
      const payload = {
        session_name: newSessionName,
        schema_id: newSchemaId || null,
        course_instance_id: newCourseInstanceId,
      };

      await axios.post("http://127.0.0.1:5000/sessions/", payload);
      setMessageType("success");
      setMessage("Session created successfully!");
      setNewSessionName("");
      setNewSchemaId("");
      setNewCourseInstanceId("");
      fetchSessions(); // Refresh sessions list
    } catch (error) {
      setMessageType("error");
      setMessage(`Error creating session: ${error.response?.data?.error || error.message}`);
    }
  };

  // Confirm delete
  const confirmDelete = (session) => {
    setSessionToDelete(session);
    setShowDeletePrompt(true);
  };

  // Delete a session
  const deleteSession = async () => {
    try {
      if (!sessionToDelete) return;
      await axios.delete(`http://127.0.0.1:5000/sessions/${sessionToDelete.session_id}`);
      setMessageType("success");
      setMessage("Session deleted successfully!");
      fetchSessions(); // Refresh sessions list
      closeDeletePrompt();
    } catch (error) {
      setMessageType("error");
      setMessage(`Error deleting session: ${error.response?.data?.error || error.message}`);
    }
  };

  // Close delete prompt
  const closeDeletePrompt = () => {
    setShowDeletePrompt(false);
    setSessionToDelete(null);
  };

  // Open edit modal
  const openEditModal = (session) => {
    setEditingSession(session);
    setShowEditModal(true);
  };

  // Close edit modal
  const closeEditModal = () => {
    setShowEditModal(false);
    setEditingSession(null);
  };
    // Toggle session status
    const toggleSessionStatus = async (session) => {
      try {
        const payload = { is_active: !session.is_active };
        await axios.put(`http://127.0.0.1:5000/sessions/${session.session_id}/status`, payload);
        setMessageType("success");
        setMessage("Session status updated successfully!");
        fetchSessions(); // Refresh sessions list
      } catch (error) {
        setMessageType("error");
        setMessage(`Error updating session status: ${error.response?.data?.error || error.message}`);
      }
    };

  // Save edited session
  const saveEditedSession = async () => {
    try {
      const payload = {
        session_name: editingSession.session_name,
        schema_id: editingSession.schema_id || null,
        course_instance_id: editingSession.course_instance_id,
      };

      await axios.put(`http://127.0.0.1:5000/sessions/${editingSession.session_id}`, payload);
      setMessageType("success");
      setMessage("Session updated successfully!");
      fetchSessions(); // Refresh session list
      closeEditModal();
    } catch (error) {
      setMessageType("error");
      setMessage(`Error updating session: ${error.response?.data?.error || error.message}`);
    }
  };

  useEffect(() => {
    fetchSessions();
    fetchSchemas();
  }, []);

  return (
    <div className="session-management">
      <h2>Session Management</h2>

      {/* Message Display */}
      {message && <div className={`message ${messageType}`}>{message}</div>}

      {/* Form for creating new session */}
      <div className="form-container">
        <h3>Create New Session</h3>
        <label>Session Name</label>
        <input
          type="text"
          placeholder="Enter session name"
          value={newSessionName}
          onChange={(e) => setNewSessionName(e.target.value)}
        />
        <label>Schema ID (Optional)</label>
        <input
          type="text"
          placeholder="Enter schema ID"
          value={newSchemaId}
          onChange={(e) => setNewSchemaId(e.target.value)}
        />
        <label>Course Instance ID</label>
        <input
          type="text"
          placeholder="Enter course instance ID"
          value={newCourseInstanceId}
          onChange={(e) => setNewCourseInstanceId(e.target.value)}
        />
        <button onClick={createSession}>Create Session</button>
      </div>

      {/* Table for displaying sessions */}
      <div className="table-container">
        <table className="styled-table">
          <thead>
            <tr>
              <th>Session Name</th>
              <th>Schema ID</th>
              <th>Course Instance</th>
              <th>Active</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {sessions.map((session) => (
              <tr key={session.session_id}>
                <td>{session.session_name}</td>
                <td>{session.schema_id !== null ? session.schema_id : "N/A"}</td>
                <td>{session.course_instance_id}</td>
                <td>{session.is_active ? "Yes" : "No"}</td>
                <td className="actions-cell">
                  <button className="btn-edit" onClick={() => openEditModal(session)}>Edit</button>
                  <button className="btn-delete" onClick={() => confirmDelete(session)}>Delete</button>
                  <button className="btn-toggle" onClick={() => toggleSessionStatus(session)}>
                    {session.is_active ? "Deactivate" : "Activate"}
                  </button>
                  <button className="btn-view-tasks" onClick={() => fetchTasks(session.session_id)}>
                    View Tasks
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      

      {/* Delete Confirmation Prompt */}
      {showDeletePrompt && (
        <div className="delete-prompt">
          <div className="delete-prompt-content">
            <p>Are you sure you want to delete the session "{sessionToDelete?.session_name}"?</p>
            <button className="btn-danger" onClick={deleteSession}>Yes, Delete</button>
            <button className="btn-secondary" onClick={closeDeletePrompt}>Cancel</button>
          </div>
        </div>
      )}

      {/* Edit Modal */}
      {showEditModal && (
        <div className="modal">
          <div className="modal-content">
            <h3>Edit Session</h3>
            <label>Session Name</label>
            <input
              type="text"
              value={editingSession?.session_name || ""}
              onChange={(e) =>
                setEditingSession({ ...editingSession, session_name: e.target.value })
              }
            />
            <label>Schema ID</label>
            <input
              type="text"
              value={editingSession?.schema_id || ""}
              onChange={(e) =>
                setEditingSession({ ...editingSession, schema_id: e.target.value || null })
              }
            />
            <label>Course Instance ID</label>
            <input
              type="text"
              value={editingSession?.course_instance_id || ""}
              onChange={(e) =>
                setEditingSession({ ...editingSession, course_instance_id: e.target.value })
              }
            />
            <button onClick={saveEditedSession} className="btn-primary">Save</button>
            <button onClick={closeEditModal} className="btn-secondary">Cancel</button>
          </div>
        </div>
      )}

      {/* Tasks Modal */}
      {showTasksModal && (
        <div className="modal">
          <div className="modal-content">
            <h3>Tasks for Session {selectedSession}</h3>
            <ul>
              {tasks.map((task,index) => (
                <li key={task.task_id}>
                  <div><strong>Task {index + 1}:</strong></div>
                  <strong>Question:</strong> {task.question_text} <br />
                  <strong>Solution Query:</strong> {task.solution_query} <br />
                  <strong>Category:</strong> {task.category}
                </li>
              ))}
            </ul>
            <button onClick={closeTasksModal} className="btn-secondary">Close</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default SessionManagement;





