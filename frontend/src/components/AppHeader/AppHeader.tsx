import React from 'react';

const AppHeader: React.FC = () => { 
  return (
      <div className="flex">
        <div className="w-64 bg-gray-100">Sidebar</div>
        <div className="flex-1">Main content</div>
      </div>
    );
  }
  
  export default AppHeader;