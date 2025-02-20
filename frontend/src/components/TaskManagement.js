import React, { useEffect, useState } from "react";
import api from "../services/api"; // Import axios instance
import "../Styles/TaskManagement.css";

function TaskManagement() {
  const [tasks, setTasks] = useState([]);
  const [courses, setCourses] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [schemas, setSchemas] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [showEditForm, setShowEditForm] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [currentTask, setCurrentTask] = useState(null);
  const [newTask, setNewTask] = useState({
    task_title: "",
    task_description: "",
    course_id: "",
    session_id: "",
    schema_id: "",
    difficulty: "medium",
    deadline: "",
    correct_answer: "",
  });

  useEffect(() => {
    fetchTasks();
    fetchCourses();
    fetchSchemas();
  }, []);

  const fetchTasks = async () => {
    try {
      const response = await api.get("/tasks");
      setTasks(response.data.tasks);
    } catch (error) {
      console.error("Error fetching tasks:", error);
    }
  };

  const fetchCourses = async () => {
    try {
      const response = await api.get("/courses");
      setCourses(response.data.courses);
    } catch (error) {
      console.error("Error fetching courses:", error);
    }
  };

  const fetchSessions = async (courseId) => {
    try {
      const response = await api.get(`/sessions?course_id=${courseId}`);
      setSessions(response.data.sessions);
    } catch (error) {
      console.error("Error fetching sessions:", error);
    }
  };

  const fetchSchemas = async () => {
    try {
      const response = await api.get("/schemas");
      setSchemas(response.data.schemas);
    } catch (error) {
      console.error("Error fetching schemas:", error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewTask({ ...newTask, [name]: value });
  };

  const handleCourseChange = (e) => {
    const courseId = e.target.value;
    setNewTask({ ...newTask, course_id: courseId, session_id: "" });
    fetchSessions(courseId);
  };

  const handleCreateTask = async () => {
    try {
      await api.post("/tasks", newTask);
      fetchTasks();
      setShowForm(false);
    } catch (error) {
      console.error("Error creating task:", error);
    }
  };

  const handleUpdateTask = async () => {
    try {
      await api.put(`/tasks/${currentTask.task_id}`, currentTask);
      fetchTasks();
      setShowEditForm(false);
    } catch (error) {
      console.error("Error updating task:", error);
    }
  };

  const handleDeleteTask = async () => {
    try {
      await api.delete(`/tasks/${currentTask.task_id}`);
      fetchTasks();
      setShowDeleteConfirm(false);
    } catch (error) {
      console.error("Error deleting task:", error);
    }
  };

  return (
    <div className="task-management">
      <h1>Task Management</h1>
      <button className="create-btn" onClick={() => setShowForm(true)}>+ Create Task</button>

      <table className="task-table">
        <thead>
          <tr>
            <th>Title</th>
            <th>Description</th>
            <th>Difficulty</th>
            <th>Deadline</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map((task) => (
            <tr key={task.task_id}>
              <td>{task.task_title}</td>
              <td>{task.task_description}</td>
              <td>{task.difficulty}</td>
              <td>{task.deadline}</td>
              <td>
                <button onClick={() => { setCurrentTask(task); setShowEditForm(true); }}>Edit</button>
                <button onClick={() => { setCurrentTask(task); setShowDeleteConfirm(true); }}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {showForm && (
        <div className="modal">
          <div className="modal-content">
            <h2>Create Task</h2>
            <input type="text" name="task_title" placeholder="Task Title" onChange={handleInputChange} />
            <textarea name="task_description" placeholder="Task Description" onChange={handleInputChange} />
            <select name="course_id" onChange={handleCourseChange}>
              <option value="">Select Course</option>
              {courses.map(course => <option key={course.course_id} value={course.course_id}>{course.course_name}</option>)}
            </select>
            <select name="session_id" onChange={handleInputChange}>
              <option value="">Select Session</option>
              {sessions.map(session => <option key={session.session_id} value={session.session_id}>{session.session_name}</option>)}
            </select>
            <select name="schema_id" onChange={handleInputChange}>
              <option value="">Select Schema</option>
              {schemas.map(schema => <option key={schema.schema_id} value={schema.schema_id}>{schema.schema_name}</option>)}
            </select>
            <button onClick={handleCreateTask}>Create</button>
            <button onClick={() => setShowForm(false)}>Cancel</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default TaskManagement;