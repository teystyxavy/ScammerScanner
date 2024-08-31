import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");
	const [error, setError] = useState("");
	const navigate = useNavigate();

	const handleLogin = async (e) => {
		e.preventDefault();

		try {
			const response = await fetch("http://localhost:5000/login", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ username, password }),
			});

			if (response.ok) {
				const userData = await response.json();
				localStorage.setItem("isLogged", "true");

				// Force re-render by updating state or causing side effect
				window.dispatchEvent(new Event("storage"));

				navigate("/"); // Redirect to home after login
			} else {
				const errorData = await response.json();
				setError(errorData.error || "Invalid username or password");
			}
		} catch (err) {
			setError("Something went wrong. Please try again later.");
		}
	};

	return (
		<div className="flex justify-center items-center mt-16 mb-8">
			<div className="w-full max-w-md">
				<h1 className="text-3xl font-bold text-center mb-4">Login</h1>
				<form
					onSubmit={handleLogin}
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
					<div className="mb-6">
						<label className="block text-gray-700 text-sm font-bold mb-2">
							Password
						</label>
						<input
							type="password"
							className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
							value={password}
							onChange={(e) => setPassword(e.target.value)}
							required
						/>
						{error && <p className="text-red-500 text-xs italic">{error}</p>}
					</div>
					<div className="flex items-center justify-center">
						<button
							type="submit"
							className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
						>
							Login
						</button>
					</div>
				</form>
				<p className="text-center text-gray-500 text-xs mt-4">
					Don't have an account?{" "}
					<a href="/register" className="text-blue-500 hover:text-blue-800">
						Sign up
					</a>
				</p>
			</div>
		</div>
	);
}

export default Login;
