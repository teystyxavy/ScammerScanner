import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Profile() {
	const [user, setUser] = useState(null);
	const [username, setUsername] = useState("");
	const [email, setEmail] = useState("");
	const [profileCurrentPassword, setProfileCurrentPassword] = useState(""); // Separate state for profile form
	const [passwordCurrentPassword, setPasswordCurrentPassword] = useState(""); // Separate state for password change form
	const [newPassword, setNewPassword] = useState("");
	const [confirmPassword, setConfirmPassword] = useState("");
	const [profileError, setProfileError] = useState("");
	const [profileSuccess, setProfileSuccess] = useState("");
	const [passwordError, setPasswordError] = useState("");
	const [passwordSuccess, setPasswordSuccess] = useState("");
	const navigate = useNavigate();

	useEffect(() => {
		const fetchUserData = async () => {
			try {
				const response = await fetch("/api/current_user", {
					method: "GET",
					credentials: "include", // Include cookies (sessions) with the request
				});

				if (response.ok) {
					const userData = await response.json();
					setUser(userData);
					setUsername(userData.username);
					setEmail(userData.email);
				} else {
					// If no user is found, redirect to the login page
					navigate("/login");
				}
			} catch (err) {
				console.error("Failed to fetch user data:", err);
				navigate("/login");
			}
		};

		fetchUserData();
	}, [navigate]);

  const handleLogout = async () => {
    try {
      const response = await fetch('/logout', {
        method: 'POST',
        credentials: 'include', // Include session cookies
      });
  
      if (response.ok) {
        // Clear user data from localStorage
        localStorage.removeItem('isLogged');
        window.dispatchEvent(new Event('storage'));
  
        // Redirect to the login page
        navigate('/login');
      } else {
        console.error('Failed to log out');
      }
    } catch (error) {
      console.error('Error logging out:', error);
    }
  };
  

	const handleProfileSave = async (e) => {
		e.preventDefault();
		if (!profileCurrentPassword) {
			setProfileSuccess("");
			setProfileError("Please enter your current password to save changes.");
			return;
		}

		try {
			const response = await fetch(`/api/user/${user.user_id}`, {
				method: "PUT",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({
					username,
					email,
					currentPassword: profileCurrentPassword,
				}),
			});

			if (response.ok) {
				const updatedUser = await response.json();
				setProfileSuccess("Profile updated successfully.");
				setProfileError("");
				setProfileCurrentPassword(""); // Clear the current password field
			} else {
				const errorData = await response.json();
				setProfileSuccess("");
				setProfileError(
					errorData.error || "Failed to update profile. Please try again."
				);
			}
		} catch (err) {
			setProfileSuccess("");
			setProfileError("Something went wrong. Please try again later.");
		}
	};

	const handleChangePassword = async (e) => {
		e.preventDefault();
		if (!passwordCurrentPassword) {
			setPasswordError("Please enter your current password.");
			return;
		}

		if (newPassword !== confirmPassword) {
			setPasswordSuccess("");
			setPasswordError("New passwords do not match.");
			return;
		}

		try {
			const response = await fetch(`/api/password`, {
				method: "PUT",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({
					currentPassword: passwordCurrentPassword,
					newPassword,
				}),
			});

			if (response.ok) {
				setPasswordSuccess("Password updated successfully.");
				setPasswordError("");
				setPasswordCurrentPassword(""); // Clear the current password field
				setNewPassword("");
				setConfirmPassword("");
			} else {
				const errorData = await response.json();
				setPasswordError(
					errorData.error || "Failed to update password. Please try again."
				);
			}
		} catch (err) {
			setPasswordSuccess("");
			setPasswordError("Something went wrong. Please try again later.");
		}
	};

	if (!user) {
		return <div>Loading...</div>;
	}

	return (
		<div className="flex flex-col justify-center items-center mt-16 mb-8">
			<div className="w-full max-w-md mb-8">
				<h1 className="text-3xl font-bold text-center mb-6">Profile</h1>
				<form
					onSubmit={handleProfileSave}
					className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
				>
					<div className="mb-4">
						<label className="block text-gray-700 text-sm font-bold mb-2">
							Username
						</label>
						<input
							type="text"
							className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
							value={username}
							onChange={(e) => setUsername(e.target.value)}
							required
						/>
					</div>
					<div className="mb-4">
						<label className="block text-gray-700 text-sm font-bold mb-2">
							Email
						</label>
						<input
							type="email"
							className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
							value={email}
							onChange={(e) => setEmail(e.target.value)}
							required
						/>
					</div>
					<div className="mb-6">
						<label className="block text-gray-700 text-sm font-bold mb-2">
							Current Password
						</label>
						<input
							type="password"
							className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
							value={profileCurrentPassword}
							onChange={(e) => setProfileCurrentPassword(e.target.value)}
							required
						/>
					</div>
					{profileError && (
						<p className="text-red-500 text-xs italic mb-4">{profileError}</p>
					)}
					{profileSuccess && (
						<p className="text-green-500 text-xs italic mb-4">
							{profileSuccess}
						</p>
					)}
					<div className="flex items-center justify-center mt-6">
						<button
							type="submit"
							className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
						>
							Save Profile
						</button>
					</div>
				</form>
			</div>

			<div className="w-full max-w-md">
				<h2 className="text-2xl font-bold text-center mb-6">Change Password</h2>
				<form
					onSubmit={handleChangePassword}
					className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
				>
					<div className="mb-4">
						<label className="block text-gray-700 text-sm font-bold mb-2">
							Current Password
						</label>
						<input
							type="password"
							className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
							value={passwordCurrentPassword}
							onChange={(e) => setPasswordCurrentPassword(e.target.value)}
							required
						/>
					</div>
					<div className="mb-4">
						<label className="block text-gray-700 text-sm font-bold mb-2">
							New Password
						</label>
						<input
							type="password"
							className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
							value={newPassword}
							onChange={(e) => setNewPassword(e.target.value)}
							required
						/>
					</div>
					<div className="mb-6">
						<label className="block text-gray-700 text-sm font-bold mb-2">
							Confirm New Password
						</label>
						<input
							type="password"
							className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
							value={confirmPassword}
							onChange={(e) => setConfirmPassword(e.target.value)}
							required
						/>
					</div>
					{passwordError && (
						<p className="text-red-500 text-xs italic mb-4">{passwordError}</p>
					)}
					{passwordSuccess && (
						<p className="text-green-500 text-xs italic mb-4">
							{passwordSuccess}
						</p>
					)}
					<div className="flex items-center justify-center mt-6">
						<button
							type="submit"
							className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
						>
							Change Password
						</button>
					</div>
				</form>
				<div className="flex items-center justify-center mt-6">
					<button
						onClick={handleLogout}
						className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
					>
						Sign Out
					</button>
				</div>
			</div>
		</div>
	);
}

export default Profile;
