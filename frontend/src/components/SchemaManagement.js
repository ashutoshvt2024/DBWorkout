import React, { useState, useEffect } from "react";
import api from "../services/api";
import MonacoEditor from '@monaco-editor/react';
import "../Styles/SchemaManagement.css";

function SchemaManagement() {
  const [schemas, setSchemas] = useState([]);
  const [selectedSchema, setSelectedSchema] = useState("");
  const [tables, setTables] = useState([]);
  const [tableName, setTableName] = useState("");
  const [columns, setColumns] = useState([{ name: "", type: "" }]);
  const [sqlQuery, setSqlQuery] = useState("");
  const [executionResult, setExecutionResult] = useState("");
  const [isSqlMode, setIsSqlMode] = useState(false);

  useEffect(() => {
    fetchSchemas();
  }, []);

  const fetchSchemas = async () => {
    try {
      const response = await api.get("/schemas");
      setSchemas(response.data.schemas);
    } catch (error) {
      console.error("Error fetching schemas:", error);
    }
  };

  const fetchTables = async (schemaId) => {
    setSelectedSchema(schemaId);
    try {
      const response = await api.get(`/schemas/${schemaId}`);
      setTables(response.data.schema.tables || []);
    } catch (error) {
      console.error("Error fetching tables:", error);
    }
  };

  const handleColumnChange = (index, field, value) => {
    const updatedColumns = [...columns];
    updatedColumns[index][field] = value;
    setColumns(updatedColumns);
  };

  const addColumn = () => {
    setColumns([...columns, { name: "", type: "" }]);
  };

  const removeColumn = (index) => {
    setColumns(columns.filter((_, i) => i !== index));
  };

  const handleCreateTable = async () => {
    try {
      await api.post(`/schemas/${selectedSchema}/tables`, {
        table_name: tableName,
        columns,
      });
      fetchTables(selectedSchema);
    } catch (error) {
      console.error("Error creating table:", error);
    }
  };

  const executeSqlQuery = async () => {
    try {
      const response = await api.post(`/schemas/${selectedSchema}/execute`, {
        query: sqlQuery,
      });
      setExecutionResult(response.data.message || "Query executed successfully.");
      fetchTables(selectedSchema);
    } catch (error) {
      setExecutionResult(error.response?.data?.error || "Error executing query.");
    }
  };

  return (
    <div className="schema-management">
      <h1>Schema Management</h1>
      <div>
        <label>Select Schema:</label>
        <select onChange={(e) => fetchTables(e.target.value)}>
          <option value="">-- Select Schema --</option>
          {schemas.map((schema) => (
            <option key={schema.schema_id} value={schema.schema_id}>
              {schema.schema_name}
            </option>
          ))}
        </select>
      </div>

      <button onClick={() => setIsSqlMode(!isSqlMode)}>
        {isSqlMode ? "Switch to Manual Mode" : "Switch to SQL Mode"}
      </button>

      {isSqlMode ? (
        <div className="sql-editor">
          <MonacoEditor
            width="100%"
            height="300px"
            language="sql"
            theme="vs-dark"
            value={sqlQuery}
            onChange={setSqlQuery}
          />
          <button onClick={executeSqlQuery}>Run Query</button>
          {executionResult && <p>{executionResult}</p>}
        </div>
      ) : (
        <div className="manual-mode">
          <h3>Create Table</h3>
          <input
            type="text"
            placeholder="Table Name"
            value={tableName}
            onChange={(e) => setTableName(e.target.value)}
          />
          <table>
            <thead>
              <tr>
                <th>Column Name</th>
                <th>Type</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {columns.map((col, index) => (
                <tr key={index}>
                  <td>
                    <input
                      type="text"
                      value={col.name}
                      onChange={(e) => handleColumnChange(index, "name", e.target.value)}
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      value={col.type}
                      onChange={(e) => handleColumnChange(index, "type", e.target.value)}
                    />
                  </td>
                  <td>
                    <button onClick={() => removeColumn(index)}>Remove</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <button onClick={addColumn}>Add Column</button>
          <button onClick={handleCreateTable}>Create Table</button>
        </div>
      )}

      {tables.length > 0 && (
        <div>
          <h3>Existing Tables</h3>
          <ul>
            {tables.map((table, index) => (
              <li key={index}>{table.table_name}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default SchemaManagement;
