import React, { useState, useEffect } from "react";
import api from "../services/api";
import MonacoEditor from "@monaco-editor/react";
import "../Styles/SchemaManagement.css";

function SchemaManagement() {
  const [schemas, setSchemas] = useState([]);
  const [selectedSchema, setSelectedSchema] = useState("");
  const [tables, setTables] = useState([]);
  const [selectedTable, setSelectedTable] = useState("");
  const [tableData, setTableData] = useState([]);
  const [columns, setColumns] = useState([{ name: "", type: "" }]);
  const [rows, setRows] = useState([{ name: "", age: "" }]);
  const [sqlQuery, setSqlQuery] = useState("");
  const [executionResult, setExecutionResult] = useState("");
  const [isSqlMode, setIsSqlMode] = useState(false);
  const [isSchemaSqlMode, setIsSchemaSqlMode] = useState(false);
  const [schemaName, setSchemaName] = useState("");

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
      const response = await api.get(`/schemas/${schemaId}/tables`);
      setTables(response.data.tables || []);
      setSelectedTable(""); // Reset selected table
      setTableData([]); // Reset table data
    } catch (error) {
      console.error("Error fetching tables:", error);
    }
  };

  const fetchTableData = async (tableName) => {
    setSelectedTable(tableName);
    try {
      const response = await api.get(`/schemas/${selectedSchema}/tables/${tableName}/data`);
      setTableData(response.data.rows || []);
    } catch (error) {
      console.error("Error fetching table data:", error);
    }
  };

  const handleCreateSchema = async () => {
    try {
      await api.post("/schemas", { schema_name: schemaName });
      fetchSchemas();
      setSchemaName("");
    } catch (error) {
      console.error("Error creating schema:", error);
    }
  };

  const executeSchemaSqlQuery = async () => {
    try {
      const response = await api.post("/schemas/execute", { sql_command: sqlQuery });
      setExecutionResult(response.data.message || "Query executed successfully.");
      fetchSchemas();
    } catch (error) {
      setExecutionResult(error.response?.data?.error || "Error executing query.");
    }
  };

  const handleCreateTable = async () => {
    try {
      await api.post(`/schemas/${selectedSchema}/tables`, {
        table_name: selectedTable,
        columns,
      });
      fetchTables(selectedSchema);
      setColumns([{ name: "", type: "" }]);
    } catch (error) {
      console.error("Error creating table:", error);
    }
  };

  const executeTableSqlQuery = async () => {
    try {
      const response = await api.post(`/schemas/${selectedSchema}/execute`, {
        sql_command: sqlQuery,
      });
      setExecutionResult(response.data.message || "Query executed successfully.");
      fetchTables(selectedSchema);
    } catch (error) {
      setExecutionResult(error.response?.data?.error || "Error executing query.");
    }
  };

  const handleInsertData = async () => {
    try {
      await api.post(`/schemas/${selectedSchema}/tables/${selectedTable}/rows`, { rows });
      fetchTableData(selectedTable);
      setRows([{ name: "", age: "" }]);
    } catch (error) {
      console.error("Error inserting data:", error);
    }
  };

  return (
    <div className="schema-management">
      <h1>Schema Management</h1>

      {/* Schema Management */}
      <div>
        <h3>Manage Schemas</h3>
        <button onClick={() => setIsSchemaSqlMode(!isSchemaSqlMode)}>
          {isSchemaSqlMode ? "Switch to Manual Mode" : "Switch to SQL Mode"}
        </button>
        {isSchemaSqlMode ? (
          <div>
            <MonacoEditor
              width="100%"
              height="200px"
              language="sql"
              theme="vs-dark"
              value={sqlQuery}
              onChange={setSqlQuery}
            />
            <button onClick={executeSchemaSqlQuery}>Run Query</button>
            {executionResult && <p>{executionResult}</p>}
          </div>
        ) : (
          <div>
            <input
              type="text"
              placeholder="Schema Name"
              value={schemaName}
              onChange={(e) => setSchemaName(e.target.value)}
            />
            <button onClick={handleCreateSchema}>Create Schema</button>
          </div>
        )}
      </div>

      {/* Schema Selection */}
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

      {/* Table Management */}
      {selectedSchema && (
        <div>
          <h3>Manage Tables</h3>
          <button onClick={() => setIsSqlMode(!isSqlMode)}>
            {isSqlMode ? "Switch to Manual Mode" : "Switch to SQL Mode"}
          </button>
          {isSqlMode ? (
            <div>
              <MonacoEditor
                width="100%"
                height="200px"
                language="sql"
                theme="vs-dark"
                value={sqlQuery}
                onChange={setSqlQuery}
              />
              <button onClick={executeTableSqlQuery}>Run Query</button>
              {executionResult && <p>{executionResult}</p>}
            </div>
          ) : (
            <div>
              <input
                type="text"
                placeholder="Table Name"
                value={selectedTable}
                onChange={(e) => setSelectedTable(e.target.value)}
              />
              <button onClick={handleCreateTable}>Create Table</button>
            </div>
          )}

          {/* Existing Tables */}
          <div>
            <h4>Existing Tables</h4>
            <ul>
              {tables.map((table) => (
                <li key={table}>
                  <button onClick={() => fetchTableData(table)}>{table}</button>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Data Management */}
      {selectedTable && (
        <div>
          <h3>Manage Data in {selectedTable}</h3>
          <h4>Insert Data</h4>
          {rows.map((row, index) => (
            <div key={index}>
              <input
                type="text"
                placeholder="Name"
                value={row.name}
                onChange={(e) => {
                  const updatedRows = [...rows];
                  updatedRows[index].name = e.target.value;
                  setRows(updatedRows);
                }}
              />
              <input
                type="number"
                placeholder="Age"
                value={row.age}
                onChange={(e) => {
                  const updatedRows = [...rows];
                  updatedRows[index].age = e.target.value;
                  setRows(updatedRows);
                }}
              />
            </div>
          ))}
          <button onClick={() => setRows([...rows, { name: "", age: "" }])}>Add Row</button>
          <button onClick={handleInsertData}>Insert Data</button>

          {/* Display Table Data */}
          <h4>Table Data</h4>
          {tableData.length > 0 ? (
            <table>
              <thead>
                <tr>
                  {Object.keys(tableData[0]).map((col) => (
                    <th key={col}>{col}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {tableData.map((row, index) => (
                  <tr key={index}>
                    {Object.values(row).map((value, colIndex) => (
                      <td key={colIndex}>{value}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>No data available.</p>
          )}
        </div>
      )}
    </div>
  );
}

export default SchemaManagement;