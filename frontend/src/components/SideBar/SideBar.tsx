import React from 'react';


function SideBar () {
    return ( 
        <div className='fixed top-16 left-0 w-30 m-0 h-screen flex flex-col bg-secondary text-white shadow-lg pt'>
            <ul>
                <li className="bg-secondary/90 border-l-4 border-primary p-4 my-2 rounded-r">Dashboard</li>
                <li className="bg-secondary/90 hover:border-l-4 hover:border-primary p-4 my-2 rounded-r">Tasks</li>
                <li className="bg-secondary/90 hover:border-l-4 hover:border-primary p-4 my-2 rounded-r">Projects</li>
            </ul>
        </div>
    )
}

export default SideBar;