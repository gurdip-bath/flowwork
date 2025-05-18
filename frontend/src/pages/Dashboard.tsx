import React from 'react';
import { useEffect, useState } from 'react';
import TaskCard from '../components/Taskcard/TaskCard';


const Dashboard = () => {
    return (
        <div className="min-h-screen bg-gray-100 flex flex-col justify-center items-center">
            <h1 className="text-3xl font-bold text-gray-800">Welcome to the Dashboard</h1>
            <p className="text-gray-600">This is where you can manage your tasks and projects.</p>
            <TaskCard
                name = "Task 1"
                id = "1"
                description = "Sign contract and new starter docs"
                onButtonClick = {() => console.log('Button clicked')}
            />
        </div>
    )
}

export default Dashboard;
// continue building out the dashboard with more features and components as needed.
