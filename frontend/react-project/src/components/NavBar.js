import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { FaUserCircle } from "react-icons/fa";

function NavBar() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const checkLoginStatus = () => {
      const user = localStorage.getItem("user");
      if (user) {
        setIsLoggedIn(true);
      } else {
        setIsLoggedIn(false);
      }
    };

    // Check login status on component mount
    checkLoginStatus();

    // Add event listener for localStorage changes
    window.addEventListener('storage', checkLoginStatus);

    // Cleanup listener on component unmount
    return () => {
      window.removeEventListener('storage', checkLoginStatus);
    };
  }, []);

  return (
    <nav className="bg-gradient-to-r from-blue-500 to-blue-700 shadow-lg">
      <div className="container mx-auto flex justify-between items-center px-4 lg:px-8 py-4">
        <div className="text-2xl font-bold text-white">ScammerScanner</div>
        <ul className="flex space-x-6 items-center">
          <li>
            <Link
              to="/"
              className="text-white hover:text-green-400 transition duration-300 ease-in-out"
            >
              Home
            </Link>
          </li>
          <li>
            <Link
              to="/forum"
              className="text-white hover:text-green-400 transition duration-300 ease-in-out"
            >
              Forum
            </Link>
          </li>
          <li>
            <Link
              to="/rewards"
              className="text-white hover:text-green-400 transition duration-300 ease-in-out"
            >
              Rewards
            </Link>
          </li>
          <li>
            <Link
              to={isLoggedIn ? "/profile" : "/login"}
              className="text-white hover:text-green-400 transition duration-300 ease-in-out flex items-center"
            >
              <FaUserCircle className="text-2xl mr-2" />
              {isLoggedIn ? "Profile" : "Login/Sign Up"}
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default NavBar;
