import React from "react";

function PostCard({ title, author, content, imageUrl }) {
	return (
		<div
			className="flex flex-col md:flex-row md:space-x-4 items-start bg-white shadow-md p-4 rounded-lg overflow-hidden"
			style={{ height: "300px" }}
		>
			{imageUrl && (
				<div className="w-full md:w-1/3 mb-4 md:mb-0 h-full">
					<img
						src={imageUrl}
						alt={title}
						className="object-cover w-full h-full rounded-lg"
					/>
				</div>
			)}
			<div className="flex-1 overflow-hidden">
				<h2 className="text-2xl font-semibold mb-2 truncate">{title}</h2>
				<p className="text-gray-500 mb-4 truncate">Posted By: {author}</p>
				<p className="line-clamp-4 overflow-hidden text-ellipsis">{content}</p>
			</div>
		</div>
	);
}

export default PostCard;
