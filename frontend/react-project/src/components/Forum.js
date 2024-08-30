import React, { useState } from 'react';
import PostCard from './PostCard';
import PostDetail from './PostDetail';

const posts = [
  {
    id: 1,
    title: 'POSB Scam CallPOSB Scam CallPOSB Scam CallPOSB Scam CallPOSB Scam CallPOSB Scam CallPOSB Scam CallPOSB Scam CallPOSB Scam CallPOSB Scam Call',
    author: 'Anonymous',
    content: 'Writing effectively is an art. Start by using simple, everyday words people can easily understand. Be clear and direct to the point...',
    fullContent: 'Writing effectively is an art. Start by using simple, everyday words people can easily understand. Be clear and direct to the point...',
    imageUrl: 'https://via.placeholder.com/150',
  },
  {
    id: 2,
    title: 'Suspicious Whatsapp Message',
    author: 'Sarah Lim',
    content: 'Writing effectively is an art. Start by using simple, everyday words people can easily understand. Be clear and direct to the point...',
    fullContent: 'This is the full content of the Suspicious Whatsapp Message post...',
    imageUrl: 'https://via.placeholder.com/150',
  },
  {
    id: 3,
    title: 'Job Listing?',
    author: 'Tan Jia Wei',
    content: 'Writing effectively is an art. Start by using simple, everyday words people can easily understand. Be clear and direct to the point...',
    fullContent: 'This is the full content of the Job Listing? post...',
    imageUrl: 'https://via.placeholder.com/150',
  },
  {
    id: 4,
    title: 'Suspicious Whatsapp Message',
    author: 'Sarah Lim',
    content: 'Writing effectively is an art. Start by using simple, everyday words people can easily understand...',
    fullContent: 'This is the full content of the second Suspicious Whatsapp Message post...',
    imageUrl: 'https://via.placeholder.com/150',
  },
  {
    id: 5,
    title: 'Email Phishing Scam',
    author: 'John Doe',
    content: 'Scammers are sending phishing emails...',
    fullContent: 'This is the full content of the phishing scam post...',
    imageUrl: 'https://via.placeholder.com/150',
  },
  {
    id: 6,
    title: 'Fake E-commerce Website',
    author: 'Jane Smith',
    content: 'Be aware of fake e-commerce websites...',
    fullContent: 'This is the full content of the e-commerce scam post...',
    imageUrl: 'https://via.placeholder.com/150',
  },
  {
    id: 7,
    title: 'Investment Scam Alert',
    author: 'Michael Lee',
    content: 'Investment scams are on the rise...',
    fullContent: 'This is the full content of the investment scam post...',
    imageUrl: 'https://via.placeholder.com/150',
  },
];

function Forum() {
  const [selectedPost, setSelectedPost] = useState(null);

  const handlePostClick = (post) => {
    setSelectedPost(post);
  };

  const handleCloseDetail = () => {
    setSelectedPost(null);
  };

  const topPosts = posts.slice(0, 3);  // The prominent posts
  const allPosts = posts.slice(3); // Remaining "All Posts"

  return (
    <div className="max-w-6xl mx-auto p-4">
      {selectedPost ? (
        <PostDetail post={selectedPost} onClose={handleCloseDetail} />
      ) : (
        <>
          <h1 className="text-3xl font-bold text-center mb-8">Recent Scams</h1>

          {/* Top 3 Prominent Posts with Fixed Height */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            {topPosts.map(post => (
              <div 
                key={post.id} 
                onClick={() => handlePostClick(post)}
                className="cursor-pointer transform transition duration-300 hover:scale-105 hover:shadow-lg"
                style={{ height: '300px' }} // Fixed height
              >
                <PostCard
                  title={post.title}
                  author={post.author}
                  content={post.content}
                  imageUrl={post.imageUrl}
                />
              </div>
            ))}
          </div>

          {/* All Posts Section */}
          <h2 className="text-2xl font-semibold text-center mb-4">All Posts</h2>
          <div className="space-y-4">
            {allPosts.map(post => (
              <div 
                key={post.id} 
                onClick={() => handlePostClick(post)}
                className="cursor-pointer transform transition duration-300 hover:scale-102 bg-white p-4 shadow-md rounded-lg flex items-center space-x-4"
              >
                <img 
                  src={post.imageUrl} 
                  alt={post.title} 
                  className="w-16 h-16 object-cover rounded-md"
                />
                <div>
                  <h3 className="text-lg font-semibold">{post.title}</h3>
                  <p className="text-sm text-gray-600">Posted By: {post.author}</p>
                  <p className="text-sm text-gray-800 truncate">{post.content}</p>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

export default Forum;
