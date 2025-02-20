import React, { useState } from 'react';
import Editor from '@monaco-editor/react';
import '../Styles/Workspace.css';
import Task from './Task';

function Workspace() {
  const [code, setCode] = useState('');

  const handleEditorChange = (value) => {
    setCode(value);
  };

  const options = {
    fontSize: 16,  // Slightly reduced for better alignment
    fontFamily: "Fira Code, Consolas, 'Courier New', monospace",
    wordWrap: 'on',
    minimap: { enabled: false },
    scrollbar: { vertical: 'auto', horizontal: 'auto' },
    automaticLayout: true,
    contextmenu: false,
    lineNumbers: 'on',
    lineHeight: 24, // Improves alignment
    letterSpacing: 0.5, // Adjusts spacing slightly to avoid gaps
  };

  return (
    <div className="workspace">
      {/* Task Container */}
      <Task />

      {/* Editor Container */}
      <div className="editor-container">
        <div className="sql-statement-container">
          <h2>SQL Statement</h2> 
        </div> 
        <div className="editor-wrapper">
          <Editor
            height="55vh"
            language="sql"
            theme="vs-dark"
            value={code}
            options={options}
            onChange={handleEditorChange}
          />
        </div>
        <div className="result-container">
          <h2>Result</h2> 
        </div>
      </div>
    </div>
  );
}

export default Workspace;