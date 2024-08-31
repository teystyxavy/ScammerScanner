import React from "react";

export default function Result({ result, file, onReset }) {
	return (
		<div className="flex flex-col items-center justify-center p-6 bg-white rounded-lg shadow-lg w-full max-w-md mx-auto my-9">
			<h2 className="font-semibold text-3xl mb-4 text-blue-500">
				Detection Results
			</h2>
			<div className="w-full text-left">
				<div className="mb-4">
					<h3 className="font-medium text-lg">Content:</h3>
					<div className="flex justify-center">
						{file && (
							<img
								src={URL.createObjectURL(file)}
								alt="Uploaded file"
								className="max-w-full h-auto rounded-md shadow-md"
							/>
						)}
					</div>
				</div>
				<div className="mb-4">
					<h3 className="font-medium text-lg">First Check:</h3>
					<p
						className={`p-2 rounded-md ${
							result.first_check
								? "bg-green-100 text-green-600"
								: "bg-red-100 text-red-600"
						}`}
					>
						{result.first_check ? "Passed" : "Failed"}
					</p>
				</div>
				<div className="mb-4">
					<h3 className="font-medium text-lg">Second Check (Is Scam?):</h3>
					<p
						className={`p-2 rounded-md ${
							result.second_check_is_scam
								? "bg-red-100 text-red-600"
								: "bg-green-100 text-green-600"
						}`}
					>
						{result.second_check_is_scam ? "Scam Detected" : "No Scam Detected"}
					</p>
				</div>
				<div className="mb-4">
					<h3 className="font-medium text-lg">Second Check Results:</h3>
					<p
						className={`p-2 rounded-md ${
							result.second_check_results
								? "bg-red-100 text-red-600"
								: "bg-green-100 text-green-600"
						}`}
					>
						{result.second_check_results ? "Failed" : "Passed"}
					</p>
				</div>
				<div className="mb-4">
					<h3 className="font-medium text-lg">Status:</h3>
					<p
						className={`p-2 rounded-md ${
							result.status === "success"
								? "bg-green-100 text-green-600"
								: "bg-red-100 text-red-600"
						}`}
					>
						{result.status === "success" ? "Success" : "Error"}
					</p>
				</div>
				<div className="mt-4">
					<h3 className="font-medium text-lg">Message:</h3>
					<p className="text-gray-700 bg-gray-100 p-2 rounded-md">
						{result.message || "No message provided"}
					</p>
				</div>
			</div>
			<button
				onClick={onReset}
				className="mt-6 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors duration-200"
			>
				Scan Another
			</button>
		</div>
	);
}
