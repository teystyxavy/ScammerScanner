import "./App.css";
import { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./components/Scanner/HomePage";
import NavBar from "./components/NavBar";
import Forum from "./components/Forum/Forum";
import Login from "./components/Login";
import Register from "./components/Register";
import Rewards from "./components/Rewards";
import Profile from "./components/Profile";
import FileDisplay from "./components/Scanner/FileDisplay";
import Result from "./components/Scanner/Result";
import Loading from "./components/Scanner/Loading";

function App() {
	const [file, setFile] = useState(null);
	const [output, setOutput] = useState(null);
	const [loading, setLoading] = useState(false);

	const isFileAvailable = file;

	function handleFileReset() {
		setFile(null);
		setOutput(null);
	}

	return (
		<Router>
			<div className="w-full">
				<NavBar />
				<div className="flex flex-col px-4 lg:px-8">
					<Routes>
						<Route
							path="/"
							element={
								<section className="min-h-screen flex flex-col">
									{output ? (
										<Result
											result={output}
											file={file}
											onReset={handleFileReset}
										/>
									) : loading ? (
										<Loading file={file} />
									) : isFileAvailable ? (
										<FileDisplay
											handleFileReset={handleFileReset}
											setOutput={setOutput}
											setLoading={setLoading}
											file={file}
										/>
									) : (
										<HomePage setFile={setFile} />
									)}
								</section>
							}
						/>
						<Route path="/forum" element={<Forum />} />
						<Route path="/rewards" element={<Rewards />} />
						<Route path="/login" element={<Login />} />
						<Route path="/register" element={<Register />} />
						<Route path="/profile" element={<Profile />} />
					</Routes>
					<footer></footer>
				</div>
			</div>
		</Router>
	);
}

export default App;
