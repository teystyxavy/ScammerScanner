import React, { useState, useEffect } from "react";
import PostCard from "./PostCard";
import PostDetail from "./PostDetail";

function Forum() {
	const [posts, setPosts] = useState([]);
	const [selectedPost, setSelectedPost] = useState(null);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState(null);

	useEffect(() => {
		// Fetch posts data from the backend API
		const fetchPosts = async () => {
			try {
				const response = await fetch("http://localhost:5000/api/posts");
				if (!response.ok) {
					throw new Error("Failed to fetch posts");
				}
				const data = await response.json();
				setPosts(data);
				setLoading(false);
			} catch (error) {
				setError(error.message);
				setLoading(false);
			}
		};

		fetchPosts();
	}, []);

	const handlePostClick = (post) => {
		setSelectedPost(post);
	};

	const handleCloseDetail = () => {
		setSelectedPost(null);
	};

	// Separate prominent (top 3) posts and remaining posts
	const topPosts = posts.slice(0, 3);
	const allPosts = posts.slice(3);

	if (loading) {
		return <div className="text-center">Loading...</div>;
	}

	if (error) {
		return <div className="text-center text-red-500">Error: {error}</div>;
	}

	return (
		<div className="max-w-6xl mx-auto p-4">
			{selectedPost ? (
				<PostDetail post={selectedPost} onClose={handleCloseDetail} />
			) : (
				<>
					<h1 className="text-3xl font-bold text-center mb-8">Recent Scams</h1>

					{/* Top 3 Prominent Posts with Fixed Height */}
					<div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
						{topPosts.map((post) => {
							const { post: postDetails, user, screenshot } = post || {};
							return (
								<div
									key={postDetails?.post_id}
									onClick={() => handlePostClick(post)}
									className="cursor-pointer transform transition duration-300 hover:scale-105 hover:shadow-lg"
									style={{ height: "300px" }}
								>
									<PostCard
										title={postDetails?.title || "No Title"}
										author={user?.username || "Anonymous"}
										content={postDetails?.content || "No Content"}
										imageUrl={
											screenshot?.image_path ||
											"https://via.placeholder.com/150"
										}
									/>
								</div>
							);
						})}
					</div>

					{/* All Posts Section */}
					<h2 className="text-2xl font-semibold text-center mb-4">All Posts</h2>
					<div className="space-y-4">
						{allPosts.map((post) => {
							const { post: postDetails, user, screenshot } = post || {};
							return (
								<div
									key={postDetails?.post_id}
									onClick={() => handlePostClick(post)}
									className="cursor-pointer transform transition duration-300 hover:scale-102 bg-white p-4 shadow-md rounded-lg flex items-center space-x-4"
								>
									<img
										src={
											screenshot?.image_path ||
											"https://via.placeholder.com/150"
										}
										alt={postDetails?.title || "No Title"}
										className="w-16 h-16 object-cover rounded-md"
									/>
									<div className="w-full">
										<h3 className="text-lg font-semibold">
											{postDetails?.title || "No Title"}
										</h3>
										<p className="text-sm text-gray-600">
											Posted By: {user?.username || "Anonymous"}
										</p>
										<p className="text-sm text-gray-800">
											{postDetails?.content || "No Content"}
										</p>
									</div>
								</div>
							);
						})}
					</div>
				</>
			)}
		</div>
	);
}

export default Forum;
