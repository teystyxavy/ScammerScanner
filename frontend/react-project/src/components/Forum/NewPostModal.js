import React, { useState } from "react";

function NewPostModal({ isOpen, onClose, onPostCreated }) {
	const [title, setTitle] = useState("");
	const [content, setContent] = useState("");
	const [screenshot, setScreenshot] = useState(null);
	const [error, setError] = useState("");

	const handleFileChange = (e) => {
		setScreenshot(e.target.files[0]);
	};

	const handleSubmit = async (e) => {
		e.preventDefault();

		const formData = new FormData();
		formData.append("title", title);
		formData.append("content", content);
		if (screenshot) {
			formData.append("screenshot", screenshot);
		}

		try {
			const response = await fetch("http://localhost:5000/api/posts", {
				method: "POST",
				body: formData,
			});

			if (response.ok) {
				const newPost = await response.json();
				onPostCreated(newPost);

				// Add 50 points to the user
				const addPointsResponse = await fetch(
					`/api/user/${newPost.user_id}/add_points`,
					{
						method: "POST",
						headers: {
							"Content-Type": "application/json",
						},
						body: JSON.stringify({ points: 50 }),
					}
				);

				if (!addPointsResponse.ok) {
					console.error("Failed to add points");
				}
			} else {
				const errorData = await response.json();
				setError(errorData.error || "Failed to create post");
			}
		} catch (err) {
			setError("Something went wrong. Please try again.");
		}
	};

	if (!isOpen) {
		return null;
	}

	return (
		<div className="fixed z-50 inset-0 flex items-center justify-center bg-black bg-opacity-50">
			<div className="bg-white rounded-lg p-6 w-full max-w-md">
				<h2 className="text-2xl font-semibold mb-4">Create New Post</h2>
				{error && <p className="text-red-500 text-sm mb-4">{error}</p>}
				<form onSubmit={handleSubmit}>
					<div className="mb-4">
						<label className="block text-sm font-bold mb-2">Title</label>
						<input
							type="text"
							className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
							value={title}
							onChange={(e) => setTitle(e.target.value)}
							required
						/>
					</div>
					<div className="mb-4">
						<label className="block text-sm font-bold mb-2">Content</label>
						<textarea
							className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
							value={content}
							onChange={(e) => setContent(e.target.value)}
							rows="10"
							style={{ height: "150px" }}
							required
						></textarea>
					</div>
					<div className="mb-4">
						<label className="block text-sm font-bold mb-2">Screenshot</label>
						<input
							type="file"
							className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none"
							onChange={handleFileChange}
						/>
					</div>
					<div className="flex justify-between">
						<button
							type="button"
							className="bg-gray-500 text-white py-2 px-4 rounded"
							onClick={onClose}
						>
							Cancel
						</button>
						<button
							type="submit"
							className="bg-blue-500 text-white py-2 px-4 rounded"
						>
							Create
						</button>
					</div>
				</form>
			</div>
		</div>
	);
}

export default NewPostModal;
