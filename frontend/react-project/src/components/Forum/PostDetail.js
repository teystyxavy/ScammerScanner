import React, { useState, useEffect } from 'react';
import { FaHeart, FaRegHeart } from 'react-icons/fa';

function PostDetail({ post, onClose }) {
  const { post: postDetails, user, screenshot } = post;
  const [likesCount, setLikesCount] = useState(0);
  const [isLiked, setIsLiked] = useState(false);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    const fetchLikesData = async () => {
      try {
        const response = await fetch(`/api/posts/${postDetails.post_id}/likes`);
        if (response.ok) {
          const likesData = await response.json();
          setLikesCount(likesData.likes_count);
          setIsLiked(likesData.isLiked);
        } else {
          console.error('Failed to fetch likes data');
        }
      } catch (error) {
        console.error('Error fetching likes data:', error);
      }
    };

    const fetchComments = async () => {
      try {
        const response = await fetch(`/api/posts/${postDetails.post_id}/comments`);
        if (response.ok) {
          const commentsData = await response.json();
          setComments(commentsData.comments);
        } else {
          console.error('Failed to fetch comments');
        }
      } catch (error) {
        console.error('Error fetching comments:', error);
      }
    };

    fetchLikesData();
    fetchComments();
  }, [postDetails.post_id]);

  const toggleLike = async () => {
    try {
      const response = await fetch(`/api/posts/${postDetails.post_id}/toggle_like`, {
        method: 'POST',
        credentials: 'include',
      });

      if (response.ok) {
        setIsLiked(!isLiked);
        setLikesCount(isLiked ? likesCount - 1 : likesCount + 1);
      } else {
        console.error('Failed to toggle like');
      }
    } catch (error) {
      console.error('Error toggling like:', error);
    }
  };

  const handleCommentSubmit = async (e) => {
    e.preventDefault();

    const isLogged = localStorage.getItem('isLogged');
    if (!isLogged) {
      setErrorMessage('You must be logged in to post a comment.');
      return;
    }

    if (newComment.trim() === '') {
      setErrorMessage('Comment cannot be empty.');
      return;
    }

    try {
      const response = await fetch(`/api/posts/${postDetails.post_id}/comments`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ comment_text: newComment }),
        credentials: 'include',
      });

      if (response.ok) {
        const addedComment = await response.json();
        setComments([...comments, addedComment]);
        setNewComment('');
        setErrorMessage(''); // Clear the error message on successful comment submission
      } else {
        setErrorMessage('Failed to add comment.');
      }
    } catch (error) {
      setErrorMessage('Error adding comment.');
    }
  };

  return (
    <article className="w-full max-w-3xl mx-auto px-4">
      <button 
        onClick={onClose} 
        className="mb-6 text-blue-500 hover:text-blue-700 transition-colors duration-300 ease-in-out font-semibold flex items-center"
      >
        <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7"></path>
        </svg>
        Back to Posts
      </button>
      
      <header className="mb-8">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">{postDetails?.title || "No Title"}</h1>
        <p className="text-gray-600">
          <span className="font-medium">Posted By:</span> {user?.username || "Anonymous"}
        </p>
      </header>
      
      {screenshot && (
        <figure className="mb-8">
          <img 
            src={screenshot.image_path} 
            alt={postDetails?.title || "No Title"} 
            className="w-full h-auto max-w-sm mx-auto rounded-lg"
          />
          <figcaption className="text-sm text-gray-500 mt-2 text-center">
            {postDetails?.title || "No Title"}
          </figcaption>
        </figure>
      )}

      <section className="prose prose-lg max-w-none mb-8">
        <p>{postDetails?.content || "No Content Available"}</p>
      </section>

      <div className="flex items-center space-x-4 mb-8">
        <button onClick={toggleLike}>
          {isLiked ? <FaHeart className="text-red-500" /> : <FaRegHeart />}
        </button>
        <span>{likesCount}</span>
      </div>

      {/* Comments Section */}
      <section className="mt-8">
        <h2 className="text-2xl font-bold mb-4">Comments</h2>
        {comments.length > 0 ? (
          <ul>
            {comments.map((comment, index) => (
              <li key={index} className="mb-4">
                <p className="text-gray-800"><strong>{comment.username}</strong>: {comment.comment_text}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p>No comments yet.</p>
        )}
      </section>

      {/* Add New Comment Section */}
      <section className="mt-8">
        <h2 className="text-xl font-semibold mb-4">Add a Comment</h2>
        {errorMessage && <p className="text-red-500 mb-4">{errorMessage}</p>}
        <form onSubmit={handleCommentSubmit}>
          <textarea
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            className="w-full p-2 border rounded mb-4"
            rows="3"
            placeholder="Write your comment here..."
            required
          ></textarea>
          <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
            Submit
          </button>
        </form>
      </section>
    </article>
  );
}

export default PostDetail;
