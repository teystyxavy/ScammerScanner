import React from 'react';

function PostDetail({ post, onClose }) {
  // Extract necessary fields from the post object
  const { post: postDetails, user, screenshot } = post;

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
      
      <section className="prose prose-lg max-w-none">
        <p>{postDetails?.content || "No Content Available"}</p>
      </section>
    </article>
  );
}

export default PostDetail;
