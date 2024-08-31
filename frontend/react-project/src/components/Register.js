import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Register() {
	const [username, setUsername] = useState("");
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const [confirmPassword, setConfirmPassword] = useState("");
	const [error, setError] = useState("");
	const navigate = useNavigate();

	const handleSignUp = async (e) => {
		e.preventDefault();

		if (password !== confirmPassword) {
			setError("Passwords do not match");
			return;
		}

		try {
			const response = await fetch("/register", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ username, email, password }),
			});

			if (response.ok) {
				const data = await response.json();
				localStorage.setItem("isLogged", "true");
				window.dispatchEvent(new Event("storage"));
				navigate("/");
			} else {
				const errorData = await response.json();
				setError(errorData.error || "Registration failed");
			}
		} catch (err) {
			setError("Something went wrong. Please try again later.");
		}
	};

	return (
		<div className="flex justify-center items-center mt-16 mb-8">
			<div className="w-full max-w-md">
				<h1 className="text-3xl font-bold text-center mb-4">Sign Up</h1>
				<form
					onSubmit={handleSignUp}
					className="bg-white shadow-md rounded px-8 pt-6 pb-8"
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
					<div className="mb-4">
						<label className="block text-gray-700 text-sm font-bold mb-2">
							Password
						</label>
						<input
							type="password"
							className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
							value={password}
							onChange={(e) => setPassword(e.target.value)}
							required
						/>
					</div>
					<div className="mb-6">
						<label className="block text-gray-700 text-sm font-bold mb-2">
							Confirm Password
						</label>
						<input
							type="password"
							className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
							value={confirmPassword}
							onChange={(e) => setConfirmPassword(e.target.value)}
							required
						/>
						{error && <p className="text-red-500 text-xs italic">{error}</p>}
					</div>
					<div className="flex items-center justify-center">
						<button
							type="submit"
							className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
						>
							Sign Up
						</button>
					</div>
				</form>
				<p className="text-center text-gray-500 text-xs mt-4">
					Already have an account?{" "}
					<a href="/login" className="text-blue-500 hover:text-blue-800">
						Login
					</a>
				</p>
			</div>
		</div>
	);
}

export default Register;
