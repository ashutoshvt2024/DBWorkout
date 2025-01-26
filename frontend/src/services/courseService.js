import axios from "./api";

// Fetch all courses
export const getCourses = async () => {
  try {
    const response = await axios.get("/courses");
    return response.data.courses;
  } catch (error) {
    console.error("Error fetching courses:", error.response?.data || error.message);
    throw error;
  }
};

// Create a course
export const createCourse = async (courseData) => {
  try {
    const response = await axios.post("/courses", courseData);
    return response.data;
  } catch (error) {
    console.error("Error creating course:", error.response?.data || error.message);
    throw error;
  }
};