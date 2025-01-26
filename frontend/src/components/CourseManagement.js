import React, { useState, useEffect } from "react";
import { getCourses, createCourse } from "../services/courseService";

function CourseManagement() {
  const [courses, setCourses] = useState([]);
  const [newCourseName, setNewCourseName] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    try {
      const data = await getCourses();
      setCourses(data);
    } catch (err) {
      console.error("Error fetching courses:", err);
      setError("Failed to load courses. Try again later.");
    }
  };

  const handleCreateCourse = async () => {
    if (!newCourseName.trim()) {
      alert("Course name cannot be empty");
      return;
    }
    try {
      await createCourse({ course_name: newCourseName });
      setNewCourseName("");
      fetchCourses();
    } catch (err) {
      console.error("Error creating course:", err);
      setError("Failed to create course. Try again.");
    }
  };

  return (
    <div>
      <h1>Course Management</h1>
      {error && <p className="error">{error}</p>}
      <div>
        <input
          type="text"
          placeholder="Enter course name"
          value={newCourseName}
          onChange={(e) => setNewCourseName(e.target.value)}
        />
        <button onClick={handleCreateCourse}>Add Course</button>
      </div>
      <ul>
        {courses.map((course) => (
          <li key={course.course_id}>{course.course_name}</li>
        ))}
      </ul>
    </div>
  );
}

export default CourseManagement;