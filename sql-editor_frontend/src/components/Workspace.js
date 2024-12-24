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

    fontSize: 18,
    fontFamily: "Consolas, 'Courier New', monospace", // Monaco-friendly fonts
    wordWrap: 'on',
    minimap: { enabled: false },
    scrollbar: { vertical: 'auto', horizontal: 'auto' },
    automaticLayout: true,
    contextmenu: false,
    lineNumbers: 'on',
    

  };

  return (
    
      
    <div className="workspace">
    {/* Task Container */}
    <Task  />

    {/* Editor Container */}
    <div className="editor-container">
      <div className='sql-statement-container'>
        <h2>SQL Statement</h2> 
      </div> 
      <div className='editor'>
      <Editor
        height="55vh"
        language="sql"
        theme="vs-dark" // or "light"
        value={code}
        options={options}
        onChange={handleEditorChange}
      />
      </div>
      <div className='result-container'>
        <h2>Result</h2> 
      </div>
    </div>
  </div>
  );
}

export default Workspace;