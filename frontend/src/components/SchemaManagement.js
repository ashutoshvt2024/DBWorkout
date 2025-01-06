import React, { useState, useEffect } from "react";
import "../Styles/SchemaManagement.css";
import axios from "axios";
import TableManagement from "./TableManagement"; // Import the Table Management component

function SchemaManagement() {
  const [activeTab, setActiveTab] = useState("schemas");
  const [schemas, setSchemas] = useState([]);
  const [newSchemaName, setNewSchemaName] = useState("");
  const [message, setMessage] = useState("");

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

  // Delete a schema
  const handleDeleteSchema = async (schemaName) => {
    try {
      await axios.delete(`http://127.0.0.1:5000/schemas/${schemaName}`);
      setMessage("Schema deleted successfully.");
      fetchSchemas(); // Refresh schema list
    } catch (error) {
      setMessage(`Error deleting schema: ${error.response?.data?.error || error.message}`);
    }
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
                        <button onClick={() => handleDeleteSchema(schema)}>Delete</button>
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
    </div>
  );
}

export default SchemaManagement;