import React from 'react';

function Leaderboard() {
  // Dummy data for demonstration
  const leaderboardData = [
    { name: 'Alice', tasksCompleted: 10, timeTaken: '2h 30m' },
    { name: 'Bob', tasksCompleted: 8, timeTaken: '3h 15m' },
    { name: 'Charlie', tasksCompleted: 7, timeTaken: '4h 0m' },
  ];

  return (
    <div className="container">
      <h1>Leaderboard</h1>
      <table className="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Tasks Completed</th>
            <th>Time Taken</th>
          </tr>
        </thead>
        <tbody>
          {leaderboardData.map((entry, index) => (
            <tr key={index}>
              <td>{entry.name}</td>
              <td>{entry.tasksCompleted}</td>
              <td>{entry.timeTaken}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Leaderboard;