import React, { useState, useEffect } from "react";
import api from "../services/api"; // Use the API service
import { useUser } from "../context/UserContext";
import "../Styles/CourseManagement.css";

function CourseManagement() {
  const { user } = useUser();
  const [courses, setCourses] = useState([]);
  const [newCourse, setNewCourse] = useState(""); // New course input
  const [editingCourse, setEditingCourse] = useState(null); // Track editing mode
  const [updatedCourseName, setUpdatedCourseName] = useState(""); // New course name
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // ✅ Fetch courses when component loads
  useEffect(() => {
    async function fetchCourses() {
      try {
        const coursesRes = await api.get("/courses");
        console.log("Courses Data:", coursesRes.data); // Debugging
        setCourses(coursesRes.data.courses);
      } catch (err) {
        setError("Failed to load courses");
      } finally {
        setLoading(false);
      }
    }
    fetchCourses();
  }, []);

  // ✅ Create a new course (Professors Only)
  const createCourse = async () => {
    if (!newCourse.trim()) return alert("Course name cannot be empty");
  
    try {
      const response = await api.post("/courses", { course_name: newCourse });
      setCourses((prevCourses) => [...prevCourses, response.data.course]); // ✅ Updates immediately
      setNewCourse("");
    } catch (err) {
      setError("Failed to create course");
    }
  };

  // ✅ Update course (Professors Only)
  const updateCourse = async (courseId) => {
    if (!updatedCourseName.trim()) return alert("Course name cannot be empty");
  
    try {
      const response = await api.put(`/courses/${courseId}`, { course_name: updatedCourseName });
  
      setCourses((prevCourses) =>
        prevCourses.map((course) =>
          course.course_id === courseId ? { ...course, course_name: updatedCourseName } : course
        )
      ); // ✅ Update course locally in state
  
      setEditingCourse(null);
      setUpdatedCourseName("");
    } catch (err) {
      setError("Failed to update course");
    }
  };

  // ✅ Delete a course (Professors Only)
 const deleteCourse = async (courseId) => {
  if (!window.confirm("Are you sure you want to delete this course?")) return;

  try {
    await api.delete(`/courses/${courseId}`);

    setCourses((prevCourses) => {
      const updatedCourses = prevCourses.filter((course) => course.course_id !== courseId);
      return [...updatedCourses]; // ✅ Ensures React re-renders
    });

  } catch (err) {
    setError("Failed to delete course");
  }
};

  return (
    <div className="course-management">
      <h2>Course Management</h2>

      {loading && <p>Loading...</p>}
      {error && <p className="error">{error}</p>}

      {/* ✅ Professors can create courses */}
      {user?.role === "professor" && (
        <div className="create-course">
          <input
            type="text"
            placeholder="Enter course name"
            value={newCourse}
            onChange={(e) => setNewCourse(e.target.value)}
          />
          <button onClick={createCourse}>Create Course</button>
        </div>
      )}

      {/* ✅ Display Courses */}
      {courses.length === 0 ? (
        <p>No courses available</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Course ID</th>
              <th>Course Name</th>
              {user?.role === "professor" && <th>Actions</th>}
            </tr>
          </thead>
          <tbody>
            {courses.map((course) => (
              <tr key={course.course_id}>
                <td>{course.course_id}</td>
                <td>
                  {editingCourse === course.course_id ? (
                    <input
                      type="text"
                      value={updatedCourseName}
                      onChange={(e) => setUpdatedCourseName(e.target.value)}
                    />
                  ) : (
                    course.course_name
                  )}
                </td>
                {user?.role === "professor" && (
                  <td>
                    {editingCourse === course.course_id ? (
                      <>
                        <button
                          className="save-btn"
                          onClick={() => updateCourse(course.course_id)}
                        >
                          Save
                        </button>
                        <button
                          className="cancel-btn"
                          onClick={() => setEditingCourse(null)}
                        >
                          Cancel
                        </button>
                      </>
                    ) : (
                      <>
                        <button
                          className="edit-btn"
                          onClick={() => {
                            setEditingCourse(course.course_id);
                            setUpdatedCourseName(course.course_name);
                          }}
                        >
                          Edit
                        </button>
                        <button
                          className="delete-btn"
                          onClick={() => deleteCourse(course.course_id)}
                        >
                          Delete
                        </button>
                      </>
                    )}
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default CourseManagement;