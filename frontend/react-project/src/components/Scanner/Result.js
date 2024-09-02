import React from "react";

export default function Result({ result, file, onReset }) {
	const spellingCheck = result.first_check;
	const isInTheDatabase = result.second_check_results;
	const text_classification = result.second_check_is_scam;

	// result = {
	// 	first_check: false,
	// 	second_check_results: true,
	// 	second_check_is_scam: true,
	// };

	var colour = "G";

	if (spellingCheck) {
		colour = "R";
	} else if (!isInTheDatabase) {
		colour = "Y";
	} else if (text_classification) {
		colour = "R";
	} else {
		colour = "G";
	}

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
					<h3 className="font-medium text-lg">
						Spelling and Malicious Links Test
					</h3>
					<p
						className={`p-2 rounded-md ${
							!result.first_check
								? "bg-green-100 text-green-600"
								: "bg-red-100 text-red-600"
						}`}
					>
						{!result.first_check ? "Passed" : "Failed"}
					</p>
				</div>
				{!spellingCheck && (
					<div className="mb-4">
						<h3 className="font-medium text-lg">In our database?</h3>
						<p
							className={`p-2 rounded-md ${
								!isInTheDatabase
									? "bg-yellow-100 text-yellow-600"
									: "bg-green-100 text-green-600"
							}`}
						>
							{!isInTheDatabase ? "No" : "Yes"}
						</p>
					</div>
				)}

				{isInTheDatabase && (
					<div className="mb-4">
						<h3 className="font-medium text-lg">Text Classification</h3>
						<p
							className={`p-2 rounded-md ${
								text_classification
									? "bg-red-100 text-red-600"
									: "bg-green-100 text-green-600"
							}`}
						>
							{text_classification ? "Failed" : "Passed"}
						</p>
					</div>
				)}
				<div className="mb-4">
					<h3 className="font-medium text-lg">Final Result:</h3>
					<p
						className={`p-2 rounded-md ${
							colour === "G"
								? "bg-green-100 text-green-600"
								: colour === "R"
								? "bg-red-100 text-red-600"
								: "bg-yellow-100 text-yellow-600"
						}`}
					>
						{colour === "G"
							? "Not a Scam"
							: colour === "R"
							? "It is a Scam"
							: "Cannot Determine"}
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
