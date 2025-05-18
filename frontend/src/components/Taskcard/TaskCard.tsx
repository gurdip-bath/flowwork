import React from 'react';

interface TaskCardProps {
  name: string;
  id: string;
  description: string;
  onButtonClick: () => void;
}

const TaskCard: React.FC <TaskCardProps> = ({name, id, description, onButtonClick}) => {
  return (
    <div className='bg-white shadow-md rounded-lg p-4 m-4 column'>
      <h1 className=''>this is the {name}</h1>
      <h1> this is the {id}</h1>
      <h1> this is the {description}</h1>
      <button onClick={onButtonClick}>Click me</button>
    </div>
  );
}

export default TaskCard;

// TODO: style the task card with tailwind css