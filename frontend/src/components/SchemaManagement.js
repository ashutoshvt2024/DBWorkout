import React, { useState, useEffect } from "react";
import "../Styles/SchemaManagement.css";
import axios from "axios";
import TableManagement from "./TableManagement"; // Import the Table Management component

function SchemaManagement() {
  const [activeTab, setActiveTab] = useState("schemas");
  const [schemas, setSchemas] = useState([]);
  const [newSchemaName, setNewSchemaName] = useState("");
  const [message, setMessage] = useState("");
  const [showConfirm, setShowConfirm] = useState(false);
  const [schemaToDelete, setSchemaToDelete] = useState("");

  // Fetch schemas from backend
  const fetchSchemas = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/schemas");
      setSchemas(response.data.schemas);
      setMessage(""); // Clear any previous messages
    } catch (error) {
      setMessage(`Error fetching schemas: ${error.response?.data?.error || error.message}`);
    }
  };

  // Create a new schema
  const handleCreateSchema = async () => {
    try {
      if (!newSchemaName) {
        setMessage("Please enter a schema name.");
        return;
      }

      const payload = { schema_name: newSchemaName };
      const response = await axios.post("http://127.0.0.1:5000/schemas/", payload);
      setMessage(response.data.message);
      setNewSchemaName("");
      fetchSchemas(); // Refresh schema list
    } catch (error) {
      setMessage(`Error creating schema: ${error.response?.data?.error || error.message}`);
    }
  };

  // Confirm deletion of a schema
  const confirmDeleteSchema = (schema) => {
    setSchemaToDelete(schema);
    setShowConfirm(true);
  };

  // Delete a schema
  const handleDeleteSchema = async () => {
    try {
      await axios.delete(`http://127.0.0.1:5000/schemas/${schemaToDelete}`);
      setMessage("Schema deleted successfully.");
      setShowConfirm(false);
      setSchemaToDelete("");
      fetchSchemas(); // Refresh schema list
    } catch (error) {
      setMessage(`Error deleting schema: ${error.response?.data?.error || error.message}`);
      setShowConfirm(false);
    }
  };

  const cancelDelete = () => {
    setShowConfirm(false);
    setSchemaToDelete("");
  };

  useEffect(() => {
    fetchSchemas();
  }, []);

  return (
    <div className="schema-management">
      <h2>Schema & Table Management</h2>

      {/* Tabs for switching */}
      <div className="tabs">
        <button
          className={activeTab === "schemas" ? "active" : ""}
          onClick={() => setActiveTab("schemas")}
        >
          Schema Management
        </button>
        <button
          className={activeTab === "tables" ? "active" : ""}
          onClick={() => setActiveTab("tables")}
        >
          Table Management
        </button>
      </div>

      {/* Render active tab */}
      {activeTab === "schemas" ? (
        <div className="tab-content">
          <div className="schema-form">
            <h3>Create Schema</h3>
            <input
              type="text"
              value={newSchemaName}
              onChange={(e) => setNewSchemaName(e.target.value)}
              placeholder="Enter schema name"
            />
            <button onClick={handleCreateSchema}>Create Schema</button>
          </div>

          {/* List of Schemas */}
          <div className="schema-list">
            <h3>Existing Schemas</h3>
            {schemas.length === 0 ? (
              <p>No schemas found.</p>
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>Schema Name</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {schemas.map((schema) => (
                    <tr key={schema}>
                      <td>{schema}</td>
                      <td>
                        <button onClick={() => confirmDeleteSchema(schema)}>Delete</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>

          {message && <p className="message">{message}</p>}
        </div>
      ) : (
        <div className="tab-content">
          <TableManagement />
        </div>
      )}

      {/* Confirmation Modal */}
      {showConfirm && (
        <div className="modal-overlay">
          <div className="modal">
            <h4>Are you sure you want to delete this schema?</h4>
            <p>Schema: {schemaToDelete}</p>
            <div className="modal-actions">
              <button className="btn-danger" onClick={handleDeleteSchema}>
                Delete
              </button>
              <button className="btn-secondary" onClick={cancelDelete}>
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default SchemaManagement;