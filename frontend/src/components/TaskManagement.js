import React, { useState } from "react";
import axios from "axios";
import "../Styles/TaskManagement.css"; // Add CSS file for styling

function TaskManagement() {
  const [tasks, setTasks] = useState([]);
  const [sessionID, setSessionID] = useState("");
  const [questionText, setQuestionText] = useState("");
  const [solutionQuery, setSolutionQuery] = useState("");
  const [category, setCategory] = useState("");
  const [message, setMessage] = useState("");
  const [editingTask, setEditingTask] = useState(null);

  // Fetch tasks for a session
  const fetchTasks = async () => {
    try {
      if (!sessionID) {
        setMessage("Please enter a Session ID.");
        return;
      }
      const response = await axios.get(
        `http://127.0.0.1:5000/tasks?session_id=${sessionID}`
      );
      setTasks(response.data.tasks);
      setMessage("");
    } catch (error) {
      setMessage(`Error fetching tasks: ${error.response?.data?.error || error.message}`);
    }
  };

  // Create a new task
  const handleCreateTask = async () => {
    try {
      const payload = {
        session_id: sessionID,
        question_text: questionText,
        solution_query: solutionQuery,
        category: category,
      };
      const response = await axios.post("http://127.0.0.1:5000/tasks/", payload);
      setMessage(response.data.message);
      fetchTasks();
    } catch (error) {
      setMessage(`Error creating task: ${error.response?.data?.error || error.message}`);
    }
  };

  // Edit an existing task
  const handleEditTask = async () => {
    try {
      const payload = {
        question_text: questionText,
        solution_query: solutionQuery,
        category: category,
      };
      await axios.put(`http://127.0.0.1:5000/tasks/${editingTask.task_id}`, payload);
      setMessage("Task updated successfully.");
      fetchTasks();
      setEditingTask(null);
    } catch (error) {
      setMessage(`Error updating task: ${error.response?.data?.error || error.message}`);
    }
  };

  // Delete a task
  const handleDeleteTask = async (taskId) => {
    try {
      await axios.delete(`http://127.0.0.1:5000/tasks/${taskId}`);
      setMessage("Task deleted successfully.");
      fetchTasks();
    } catch (error) {
      setMessage(`Error deleting task: ${error.response?.data?.error || error.message}`);
    }
  };

  // Render tasks in a table
  const renderTaskTable = () => {
    if (tasks.length === 0) {
      return <p>No tasks available for this session.</p>;
    }

    return (
      <table className="task-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Question</th>
            <th>Category</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map((task) => (
            <tr key={task.task_id}>
              <td>{task.task_id}</td>
              <td>{task.question_text}</td>
              <td>{task.category}</td>
              <td>
                <button onClick={() => startEditingTask(task)}>Edit</button>
                <button onClick={() => handleDeleteTask(task.task_id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  const startEditingTask = (task) => {
    setEditingTask(task);
    setQuestionText(task.question_text);
    setSolutionQuery(task.solution_query);
    setCategory(task.category);
  };

  return (
    <div className="task-management">
      <h2>Task Management</h2>

      {/* Task Form */}
      <div className="task-form">
        <h3>{editingTask ? "Edit Task" : "Create Task"}</h3>
        <input
          type="text"
          value={sessionID}
          onChange={(e) => setSessionID(e.target.value)}
          placeholder="Session ID"
          disabled={editingTask}
        />
        <textarea
          value={questionText}
          onChange={(e) => setQuestionText(e.target.value)}
          placeholder="Question Text"
        />
        <textarea
          value={solutionQuery}
          onChange={(e) => setSolutionQuery(e.target.value)}
          placeholder="Solution Query"
        />
        <input
          type="text"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          placeholder="Category"
        />
        <button onClick={editingTask ? handleEditTask : handleCreateTask}>
          {editingTask ? "Update Task" : "Create Task"}
        </button>
      </div>

      {/* Task List */}
      <div className="task-list">
        <h3>Tasks</h3>
        <button onClick={fetchTasks}>Load Tasks</button>
        {renderTaskTable()}
      </div>

      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default TaskManagement;