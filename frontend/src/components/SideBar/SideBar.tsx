import React from 'react';


function SideBar () {
    return ( 
        <div className='fixed h-screen flex flex-col'>
            <ul>
                <li className="bg-gray-400 text-amber-300 shadow-1g">Dashboard</li>
                <li className="bg-gray-400 text-amber-300 shadow-1g">Tasks</li>
                <li className="bg-gray-400 text-amber-300 shadow-1g">Projects</li>
            </ul>
        </div>
    )
}

export default SideBar;