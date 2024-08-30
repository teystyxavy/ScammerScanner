import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { FaUserCircle } from "react-icons/fa"; // Import an icon from react-icons (you can choose a different one if needed)

function NavBar() {
	// State to check if the user is logged in
	const [isLoggedIn, setIsLoggedIn] = useState(false);

	// This effect simulates checking the user's login status
	useEffect(() => {
		// Example: Check login status from localStorage or an API call
		const user = localStorage.getItem("user"); // Assume a user object is stored in localStorage
		if (user) {
			setIsLoggedIn(true);
		}
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
							{isLoggedIn ? "Edit Profile" : "Login/Sign Up"}
						</Link>
					</li>
				</ul>
			</div>
		</nav>
	);
}

export default NavBar;
