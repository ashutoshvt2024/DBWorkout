import React, { useState, useEffect } from "react";
import axios from "axios";
import "../Styles/TableManagement.css";

function TableManagement() {
  const [schemaName, setSchemaName] = useState("");
  const [tables, setTables] = useState([]);
  const [tableName, setTableName] = useState("");
  const [rows, setRows] = useState([]);
  const [columns, setColumns] = useState([]);
  const [newRow, setNewRow] = useState({});
  const [editingRowIndex, setEditingRowIndex] = useState(null);
  const [editingRow, setEditingRow] = useState({});
  const [message, setMessage] = useState("");
  const [loadingRows, setLoadingRows] = useState(false);

  // Fetch tables in the schema
  const fetchTables = async () => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:5000/schemas/${schemaName}/tables`
      );
      setTables(response.data.tables);
      setMessage("Tables fetched successfully!");
    } catch (error) {
      setMessage(`Error fetching tables: ${error.response?.data?.error || error.message}`);
    }
  };

  // Fetch rows from the selected table
  const fetchRows = async () => {
    setLoadingRows(true);
    try {
      const response = await axios.get(
        `http://127.0.0.1:5000/schemas/${schemaName}/tables/${tableName}/rows`
      );
      setRows(response.data.rows);
      setMessage("Rows fetched successfully!");
      if (response.data.rows.length > 0) {
        setColumns(Object.keys(response.data.rows[0]));
      }
    } catch (error) {
      setMessage(`Error fetching rows: ${error.response?.data?.error || error.message}`);
    } finally {
      setLoadingRows(false);
    }
  };

  // Insert a new row
  const insertRow = async () => {
    try {
      const payload = { rows: [newRow] };
      await axios.post(
        `http://127.0.0.1:5000/schemas/${schemaName}/tables/${tableName}/rows`,
        payload
      );
      setMessage("Row inserted successfully!");
      setNewRow({});
      fetchRows();
    } catch (error) {
      setMessage(`Error inserting row: ${error.response?.data?.error || error.message}`);
    }
  };

  // Edit an existing row
  const editRow = async () => {
    try {
      const payload = {
        updates: editingRow, // Data to update
        conditions: { id: editingRow.id }, // Identify the row by its unique identifier (e.g., `id`)
      };
      await axios.put(
        `http://127.0.0.1:5000/schemas/${schemaName}/tables/${tableName}/rows`,
        payload
      );
      setMessage("Row updated successfully!");
      setEditingRowIndex(null);
      setEditingRow({});
      fetchRows(); // Refresh the table rows
    } catch (error) {
      setMessage(`Error editing row: ${error.response?.data?.error || error.message}`);
    }
  };

  const deleteRow = async (id) => {
    if (!id) {
      setMessage("Invalid row ID.");
      return;
    }
  
    try {
      await axios.delete(
        `http://127.0.0.1:5000/schemas/${schemaName}/tables/${tableName}/rows`,
        { data: { conditions: { id } } } // Pass the id as a condition
      );
      setMessage("Row deleted successfully!");
      fetchRows();
    } catch (error) {
      setMessage(`Error deleting row: ${error.response?.data?.error || error.message}`);
    }
  };

  // Start editing a row
  const startEditing = (rowIndex, row) => {
    setEditingRowIndex(rowIndex);
    setEditingRow(row);
  };

  // Cancel editing
  const cancelEditing = () => {
    setEditingRowIndex(null);
    setEditingRow({});
  };

  // Handle schema selection
  const handleSchemaChange = (e) => {
    setSchemaName(e.target.value);
    setTables([]);
    setTableName("");
    setRows([]);
  };

  // Handle table selection
  const handleTableChange = (e) => {
    setTableName(e.target.value);
    setRows([]);
  };

  useEffect(() => {
    if (schemaName) fetchTables();
  }, [schemaName]);

  useEffect(() => {
    if (tableName) fetchRows();
  }, [tableName]);

  return (
    <div className="table-management">
      <h3>Table Management</h3>

      {/* Schema Selection */}
      <div className="form-group">
        <label>Schema Name:</label>
        <input
          type="text"
          value={schemaName}
          onChange={handleSchemaChange}
          placeholder="Enter schema name"
        />
        <button onClick={fetchTables} className="btn-primary">
          Fetch Tables
        </button>
      </div>

      {/* Table Selection */}
      {tables.length > 0 && (
        <div className="form-group">
          <label>Select Table:</label>
          <select value={tableName} onChange={handleTableChange}>
            <option value="">Select a table</option>
            {tables.map((table) => (
              <option key={table} value={table}>
                {table}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* Insert Row */}
      {tableName && (
        <div className="insert-row">
        <h4>Insert Row into Table: {tableName}</h4>
        <div className="insert-row-fields">
          {columns.map((col) => (
            <div key={col} className="field-group">
              <label>{col}:</label>
              <input
                type="text"
                value={newRow[col] || ""}
                onChange={(e) =>
                  setNewRow({ ...newRow, [col]: e.target.value })
                }
                placeholder={`Enter value for ${col}`}
              />
            </div>
          ))}
        </div>
        <button onClick={insertRow} className="btn-primary">
          Insert Row
        </button>
      </div>
      )}

      {/* Display Rows */}
      {tableName && (
        <div>
        <h4>Rows in Table: {tableName}</h4>
    
        {loadingRows ? (
          <div className="loading-spinner">Loading rows...</div>
        ) : rows.length > 0 ? (
          <div className="table-container">
            <table className="styled-table">
              <thead>
                <tr>
                  {columns.map((col) => (
                    <th key={col}>{col}</th>
                  ))}
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((row, index) => (
                  <tr key={index}>
                    {columns.map((col) => (
                      <td key={col}>
                        {editingRowIndex === index ? (
                          <input
                            type="text"
                            value={editingRow[col] || ""}
                            onChange={(e) =>
                              setEditingRow({
                                ...editingRow,
                                [col]: e.target.value,
                              })
                            }
                          />
                        ) : (
                          row[col]
                        )}
                      </td>
                    ))}
                    <td className="actions-cell">
                      {editingRowIndex === index ? (
                        <>
                          <button className="btn-primary" onClick={editRow}>
                            Save
                          </button>
                          <button className="btn-danger" onClick={cancelEditing}>
                            Cancel
                          </button>
                        </>
                      ) : (
                        <>
                          <button
                            className="btn-secondary"
                            onClick={() => startEditing(index, row)}
                          >
                            Edit
                          </button>
                          <button
                            className="btn-danger"
                            onClick={() => deleteRow({ id: row.id })}
                          >
                            Delete
                          </button>
                        </>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p>No rows found in this table.</p>
        )}
      </div>
      )}

      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default TableManagement;