import React, { useState, useEffect } from 'react';
import Editor from '@monaco-editor/react';
import '../Styles/Workspace.css';
import api from '../services/api'; // Axios instance for API calls
import { Bar } from 'react-chartjs-2'; // For leaderboard visualization

function Workspace() {
  const [tasks, setTasks] = useState([]);
  const [selectedTask, setSelectedTask] = useState(null);
  const [code, setCode] = useState('');
  const [timer, setTimer] = useState(0);
  const [isSolving, setIsSolving] = useState(false);
  const [feedback, setFeedback] = useState(null); // Feedback from the backend
  const [leaderboardData, setLeaderboardData] = useState(null);
  const timerRef = React.useRef(null);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const response = await api.get('/tasks?published=true'); // Fetch only published tasks
      setTasks(response.data.tasks);
    } catch (error) {
      console.error('Error fetching tasks:', error);
    }
  };

  const handleSolveTask = (task) => {
    if (isSolving) return; // Prevent solving multiple tasks at the same time
    setSelectedTask(task);
    setCode(''); // Clear the editor for the new task
    setIsSolving(true);
    setTimer(0); // Reset the timer
    setFeedback(null); // Clear previous feedback
    startTimer();
  };

  const startTimer = () => {
    timerRef.current = setInterval(() => {
      setTimer((prev) => prev + 1);
    }, 1000);
  };

  const stopTimer = () => {
    clearInterval(timerRef.current);
  };

  const handleSubmitTask = async () => {
    try {
      const payload = {
        assignment_id: selectedTask.task_id, // Ensure this matches the backend field
        submitted_query: code, // Ensure this matches the backend field
        time_taken: timer, // Ensure this matches the backend field
      };
  
      console.log('Submitting payload:', payload); // Debugging: Log the payload
  
      const response = await api.post('/submissions', payload);
  
      const { is_correct, feedback } = response.data;
      setFeedback({ is_correct, message: feedback });
  
      if (is_correct) {
        stopTimer(); // Stop the timer only if the query is correct
        fetchLeaderboard(); // Fetch leaderboard data after a correct submission
        setIsSolving(false);
        setSelectedTask(null);
      }
    } catch (error) {
      console.error('Error submitting task:', error);
      setFeedback({ is_correct: false, message: 'An error occurred while submitting the task.' });
    }
  };

  const fetchLeaderboard = async () => {
    try {
      const response = await api.get(`/leaderboard?task_id=${selectedTask.task_id}`); // Fetch leaderboard for the selected task
      setLeaderboardData(response.data);
    } catch (error) {
      console.error('Error fetching leaderboard:', error);
    }
  };

  const options = {
    fontSize: 16,
    fontFamily: "Fira Code, Consolas, 'Courier New', monospace",
    wordWrap: 'on',
    minimap: { enabled: false },
    scrollbar: { vertical: 'auto', horizontal: 'auto' },
    automaticLayout: true,
    contextmenu: false,
    lineNumbers: 'on',
    lineHeight: 24,
    letterSpacing: 0.5,
  };

  return (
    <div className="workspace">
      {/* Task List */}
      <div className="task-list">
        <h2>Available Tasks</h2>
        <ul>
          {tasks.map((task) => (
            <li key={task.task_id} className="task-item">
              <div>
                <strong>{task.task_title}</strong>
                <p>{task.task_description}</p>
              </div>
              <button
                className="solve-btn"
                onClick={() => handleSolveTask(task)}
                disabled={isSolving} // Disable the button if a task is being solved
              >
                Solve
              </button>
            </li>
          ))}
        </ul>
      </div>

      {/* Editor and Timer */}
      {isSolving && (
        <div className="editor-container">
          <div className="sql-statement-container">
            <h2>Solving: {selectedTask.task_title}</h2>
            <p>{selectedTask.task_description}</p>
            <p className="timer">Time Elapsed: {timer} seconds</p>
          </div>
          <div className="editor-wrapper">
            <Editor
              height="55vh"
              language="sql"
              theme="vs-dark"
              value={code}
              options={options}
              onChange={(value) => setCode(value)}
            />
          </div>
          <button className="submit-btn" onClick={handleSubmitTask}>
            Submit
          </button>
        </div>
      )}

      {/* Feedback */}
      {feedback && (
        <div className={`feedback ${feedback.is_correct ? 'correct' : 'incorrect'}`}>
          {feedback.message}
        </div>
      )}

      {/* Leaderboard */}
      {leaderboardData && (
        <div className="leaderboard-container">
          <h2>Leaderboard</h2>
          <Bar
            data={{
              labels: leaderboardData.map((entry) => entry.user_name),
              datasets: [
                {
                  label: 'Time Taken (seconds)',
                  data: leaderboardData.map((entry) => entry.time_taken),
                  backgroundColor: 'rgba(75, 192, 192, 0.6)',
                },
              ],
            }}
            options={{
              responsive: true,
              scales: {
                y: {
                  beginAtZero: true,
                },
              },
            }}
          />
        </div>
      )}
    </div>
  );
}

export default Workspace;