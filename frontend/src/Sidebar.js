import React from 'react';
import { Link } from 'react-router-dom';

const Sidebar = () => {
    return (
        <div className="flex h-screen">
            <div className="bg-gray-800 w-64 flex-shrink-0">
                <div className="flex items-center justify-center h-14 text-white font-bold text-xl">
                    Sidebar
                </div>
                <ul className="py-4">
                    <li className="pl-6">
                        <Link to="/" className="text-gray-300 hover:bg-gray-700 py-2">
                            Home
                        </Link>
                    </li>
                    <li className="pl-6">
                        <Link to="/about" className="text-gray-300 hover:bg-gray-700 py-2">
                            About
                        </Link>
                    </li>
                    {/* Add more links as needed */}
                </ul>
            </div>
            <div className="flex-grow bg-gray-100">
                {/* Add your main content here */}
            </div>
        </div>
    );
};

export default Sidebar;
