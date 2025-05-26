import React, { useState } from 'react';
import axios from 'axios';

interface TaskCardProps {
  name: string;
  id: string;
  description: string;
  onButtonClick: () => void;
}

const TaskCard: React.FC<TaskCardProps> = ({ name, id, description, onButtonClick }) => {
  const [emailStatus, setEmailStatus] = useState<string>('');

  const handleSendEmail = async () => {
    setEmailStatus('Sending...'); 
    try {
      await axios.get('/api/v1/test/send-basic-email');
      setEmailStatus('✓ Email sent!'); 
      
      setTimeout(() => setEmailStatus(''), 3000);
    } catch (error) {
      setEmailStatus('❌ Failed'); 
      setTimeout(() => setEmailStatus(''), 3000);
    }
  };

  const [ showDocModal, setShowDocModal ] = useState(false);
  
  const handleViewDocument = () => {
    setShowDocModal(true); // Toggle modal open
  };
  
  return (
    <div className="bg-white border-l-4 border-primary p-4 m-2 rounded shadow-md hover:shadow-lg">
      <h2 className="text-lg font-bold text-secondary py-2">{name}</h2>
      <p className="text-sm text-gray-500 py-2">ID: {id}</p>
      <p className="mt-1 py-2">{description}</p>
      
      <div className="flex gap-2 mt-3">
        <button 
          className="bg-primary text-white px-3 py-1 rounded text-sm"
          onClick={onButtonClick}
        >
          View Document
        </button>
        
        <button 
          className="bg-green-600 text-white px-3 py-1 rounded text-sm"
          onClick={handleSendEmail}
          disabled={emailStatus === 'Sending...'}
        >
          Send Email
        </button>
      </div>
      
      {emailStatus && (
        <p className="text-sm mt-2 font-medium">{emailStatus}</p>
      )}
    </div>
  );
};

export default TaskCard;