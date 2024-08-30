import React from 'react';
import { Link } from 'react-router-dom';

function NavBar() {
  return (
    <nav className="bg-gradient-to-r from-blue-500 to-blue-700 shadow-lg">
      <div className="container mx-auto flex justify-between items-center px-4 lg:px-8 py-4">
        <div className="text-2xl font-bold text-white">ScammerScanner</div>
        <ul className="flex space-x-6">
          <li>
            <Link to="/" className="text-white hover:text-green-400 transition duration-300 ease-in-out">
              Home
            </Link>
          </li>
          <li>
            <Link to="/scanner" className="text-white hover:text-green-400 transition duration-300 ease-in-out">
              Scanner
            </Link>
          </li>
          <li>
            <Link to="/forum" className="text-white hover:text-green-400 transition duration-300 ease-in-out">
              Forum
            </Link>
          </li>
          <li>
            <Link to="/rewards" className="text-white hover:text-green-400 transition duration-300 ease-in-out">
                Rewards
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default NavBar;
