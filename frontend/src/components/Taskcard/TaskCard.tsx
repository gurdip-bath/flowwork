import React from 'react';

interface TaskCardProps {
  name: string;
  id: string;
  description: string;
  onButtonClick: () => void;
}

const TaskCard: React.FC <TaskCardProps> = ({name, id, description, onButtonClick}) => {
  return (
  <div className="bg-white border-l-4 border-primary p-4 m-2 rounded shadow-md hover:shadow-lg">
    <h2 className="text-lg font-bold text-secondary py-2">{name}</h2>
    <p className="text-sm text-gray-500 py-2">ID: {id}</p>
    <p className="mt-1 py-2">{description}</p>
    <button className="mt-3 bg-primary text-white px-3 py-1 rounded text-sm"
      onClick={onButtonClick}>View Document</button>
  </div>
  );
}

export default TaskCard;

// TODO: style the task card with tailwind css