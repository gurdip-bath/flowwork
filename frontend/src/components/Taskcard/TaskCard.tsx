import React from 'react';

interface TaskCardProps {
  name: string;
  id: string;
  description: string;
  onButtonClick: () => void;
}

const TaskCard: React.FC <TaskCardProps> = ({name, id, description, onButtonClick}) => {
  return (
    <div>
      <h1>this is the {name}</h1>
      <h1> this is the {id}</h1>
      <h1> this is the {description}</h1>
      <button onClick={onButtonClick}>Click me</button>
    </div>
  );
}

export default TaskCard;

// TODO: style the task card with tailwind css