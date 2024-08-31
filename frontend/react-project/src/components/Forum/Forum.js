import React, { useState, useEffect } from "react";
import PostCard from "./PostCard";
import PostDetail from "./PostDetail";
import NewPostModal from "./NewPostModal";
import { FaHeart, FaRegHeart } from "react-icons/fa";

function Forum() {
    const [posts, setPosts] = useState([]); // Initialize posts as an empty array
    const [selectedPost, setSelectedPost] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [user, setUser] = useState(null);

    useEffect(() => {
        // Fetch current user data
        const fetchUser = async () => {
            try {
                const response = await fetch("/api/current_user", {
                    credentials: "include",
                });
                if (response.ok) {
                    const userData = await response.json();
                    setUser(userData);
                } else {
                    console.error("Failed to fetch user data");
                }
            } catch (error) {
                console.error("Error fetching user data:", error);
            }
        };

        fetchUser();
    }, []);

    useEffect(() => {
        const fetchPosts = async () => {
            try {
                const response = await fetch("/api/posts");
                if (!response.ok) {
                    throw new Error("Failed to fetch posts");
                }
                const data = await response.json();
                const updatedPosts = await fetchLikesCounts(data);
                setPosts(updatedPosts);
                setLoading(false);
            } catch (error) {
                setError(error.message);
                setLoading(false);
            }
        };

        fetchPosts();
    }, []);

    // Fetch likes count and isLiked status for each post
    const fetchLikesCounts = async (posts) => {
        const updatedPosts = await Promise.all(
            posts.map(async (post) => {
                const postId = post.post.post_id;
                try {
                    const response = await fetch(`/api/posts/${postId}/likes`);
                    if (response.ok) {
                        const likesData = await response.json();
                        return {
                            ...post,
                            likes_count: likesData.likes_count,
                            isLiked: likesData.isLiked,
                        };
                    } else {
                        console.error(`Failed to fetch likes count for post ${postId}`);
                        return { ...post, likes_count: 0, isLiked: false };
                    }
                } catch (error) {
                    console.error(
                        `Error fetching likes count for post ${postId}:`,
                        error
                    );
                    return { ...post, likes_count: 0, isLiked: false };
                }
            })
        );
        return updatedPosts;
    };

    const handlePostClick = (post) => {
        setSelectedPost(post);
    };

    const handleCloseDetail = () => {
        setSelectedPost(null);
    };

    const handleOpenModal = () => {
        setIsModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
    };

    const handlePostCreated = (newPost) => {
        // Add the new post at the end of the list
        setPosts((prevPosts) => {
            const formattedPost = {
                post: {
                    post_id: newPost.post_id,
                    title: newPost.title || "No Title",
                    content: newPost.content || "No Content",
                    category: newPost.category || "Discussion",
                    created_at: newPost.created_at,
                    updated_at: newPost.updated_at,
                },
                user: {
                    user_id: newPost.user_id,
                    username: user?.username || "Anonymous",
                },
                screenshot: newPost.screenshot_id ? {
                    screenshot_id: newPost.screenshot_id,
                    image_path: newPost.image_path || "https://via.placeholder.com/150",
                } : null,
                isLiked: false, // New posts start unliked by default
                likes_count: 0, // New posts start with 0 likes
            };
            return [...prevPosts, formattedPost];
        });
        setIsModalOpen(false);
    };

    const toggleLike = async (postId) => {
        try {
            const response = await fetch(`/api/posts/${postId}/toggle_like`, {
                method: "POST",
                credentials: "include", // Include session cookies
            });

            if (response.ok) {
                // Update the post's like count and liked status
                setPosts((prevPosts) =>
                    prevPosts.map((post) =>
                        post.post.post_id === postId
                            ? {
                                ...post,
                                isLiked: !post.isLiked,
                                likes_count: post.isLiked
                                    ? post.likes_count - 1
                                    : post.likes_count + 1,
                            }
                            : post
                    )
                );
            } else {
                console.error("Failed to toggle like");
            }
        } catch (error) {
            console.error("Error toggling like:", error);
        }
    };

    if (loading) {
        return <div className="text-center">Loading...</div>;
    }

    if (error) {
        return <div className="text-center text-red-500">Error: {error}</div>;
    }

    const topPosts = Array.isArray(posts) ? posts.slice(0, 3) : [];
    const allPosts = Array.isArray(posts) ? posts.slice(3) : [];

    return (
        <div className="max-w-6xl mx-auto p-4">
            {selectedPost ? (
                <PostDetail post={selectedPost} onClose={handleCloseDetail} />
            ) : (
                <>
                    <h1 className="text-3xl font-bold text-center mb-8">Recent Scams</h1>

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

                    <div className="flex justify-between items-center mb-4">
                        <h2 className="text-2xl font-semibold">All Posts</h2>
                        <button
                            className="bg-blue-500 text-white font-bold py-2 px-4 rounded"
                            onClick={handleOpenModal}
                        >
                            Create New Post
                        </button>
                    </div>

                    <NewPostModal
                        isOpen={isModalOpen}
                        onClose={handleCloseModal}
                        onPostCreated={handlePostCreated}
                    />

                    <div className="space-y-4">
                        {allPosts.map((post) => {
                            const {
                                post: postDetails,
                                user,
                                screenshot,
                                isLiked,
                                likes_count,
                            } = post || {};
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
                                        alt={postDetails.title}
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
                                            {postDetails.content}
                                        </p>
                                    </div>
                                    <div className="flex items-center space-x-2">
                                        <button
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                toggleLike(postDetails.post_id);
                                            }}
                                        >
                                            {isLiked ? (
                                                <FaHeart className="text-red-500" />
                                            ) : (
                                                <FaRegHeart />
                                            )}
                                        </button>
                                        <span>{likes_count}</span>
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
