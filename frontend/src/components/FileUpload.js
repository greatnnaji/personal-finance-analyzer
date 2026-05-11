import React, { useState, useRef } from 'react';
import './FileUpload.css';

const FileUpload = ({ onAnalysisComplete, onError, loading, setLoading }) => {
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleFile = async (file) => {
    if (!file) return;

     // Validate file type - NOW ACCEPTS PDF
    const validExtensions = ['.csv', '.pdf', '.xlsx', '.xls'];
    const fileExtension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'));
    
    if (!validExtensions.includes(fileExtension)) {
      onError('Please upload a CSV, Excel, or PDF file');
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:5050/api/upload-and-analyze', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (data.success) {
        onAnalysisComplete(data);
      } else {
        onError(data.error || 'Failed to analyze file');
      }
    } catch (error) {
      onError('Network error: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const onButtonClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="file-upload-container">
      <div 
        className={`file-upload-area ${dragActive ? 'drag-active' : ''} ${loading ? 'loading' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={onButtonClick}
      >
        <input
          ref={fileInputRef}
          type="file"
          className="file-input"
          accept=".csv,.pdf,.xlsx,.xls"
          onChange={handleChange}
          disabled={loading}
        />
        
        {loading ? (
          <div className="upload-content">
            <div className="spinner"></div>
            <p>Analyzing your transactions...</p>
          </div>
        ) : (
          <div className="upload-content">
            <div className="upload-icon">📊</div>
            <h3>Upload Your Transaction Data</h3>
            <p>Drag and drop your file here, or click to browse</p>
            <div className="file-format-info">
              <p><strong>Accepted formats:</strong> CSV, PDF, Excel (.xlsx, .xls)</p>
            </div>
            <button className="upload-button">Choose File</button>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUpload;