# API Documentation

## Overview

This document provides an overview of the API endpoints available in the ScamDetector application. The API allows users to interact with community posts, manage user accounts, and handle authentication and authorization.

## Base URL

All API requests should be made to the following base URL: localhost:3000


## Authentication

Authentication is required for most of the endpoints. A user session is maintained through the use of cookies. Users need to be logged in to perform actions such as creating posts, liking posts, adding comments, and claiming rewards.

## Endpoints

### Posts

#### Create a New Post

- **URL:** `/api/posts`
- **Method:** `POST`
- **Authentication:** Required
- **Request Parameters:**
  - `title`: The title of the post
  - `content`: The content of the post
  - `screenshot`: (optional) An image file
- **Response:**
  - `201 Created`: Returns the details of the newly created post.
  - `401 Unauthorized`: If the user is not logged in.
  - `400 Bad Request`: If required fields are missing.

#### Get a Post

- **URL:** `/api/posts/<int:post_id>`
- **Method:** `GET`
- **Authentication:** Not required
- **Response:**
  - `200 OK`: Returns the post details, including user and screenshot information.
  - `404 Not Found`: If the post does not exist.

#### Get All Posts

- **URL:** `/api/posts`
- **Method:** `GET`
- **Authentication:** Not required
- **Response:**
  - `200 OK`: Returns a list of all posts with associated user and screenshot information.

#### Update a Post

- **URL:** `/api/posts/<int:post_id>`
- **Method:** `PUT`
- **Authentication:** Required
- **Request Parameters:**
  - `user_id`: The ID of the user who owns the post.
  - `screenshot_id`: (optional) The ID of the screenshot associated with the post.
  - `content`: The updated content of the post.
  - `category`: The category of the post.
- **Response:**
  - `200 OK`: Returns the updated post details.
  - `404 Not Found`: If the post does not exist.
  - `401 Unauthorized`: If the user is not logged in.

#### Delete a Post

- **URL:** `/api/posts/<int:post_id>`
- **Method:** `DELETE`
- **Authentication:** Required
- **Response:**
  - `204 No Content`: If the post is successfully deleted.
  - `404 Not Found`: If the post does not exist.
  - `401 Unauthorized`: If the user is not logged in.

### Users

#### Get User Details

- **URL:** `/api/user/<int:user_id>`
- **Method:** `GET`
- **Authentication:** Required
- **Response:**
  - `200 OK`: Returns the user's details.
  - `404 Not Found`: If the user does not exist.

#### Update User Details

- **URL:** `/api/user/<int:user_id>`
- **Method:** `PUT`
- **Authentication:** Required
- **Request Parameters:**
  - `username`: The new username.
  - `email`: The new email address.
  - `currentPassword`: The current password for verification.
- **Response:**
  - `200 OK`: Returns the updated user details.
  - `403 Forbidden`: If the current password is incorrect.
  - `404 Not Found`: If the user does not exist.

#### Update User Password

- **URL:** `/api/password`
- **Method:** `PUT`
- **Authentication:** Required
- **Request Parameters:**
  - `currentPassword`: The current password for verification.
  - `newPassword`: The new password.
- **Response:**
  - `200 OK`: If the password is updated successfully.
  - `403 Forbidden`: If the current password is incorrect.
  - `401 Unauthorized`: If the user is not logged in.

#### Add Points to a User

- **URL:** `/api/user/<int:user_id>/add_points`
- **Method:** `POST`
- **Authentication:** Required
- **Request Parameters:**
  - `points`: The number of points to add to the user.
- **Response:**
  - `200 OK`: Returns the new points total.
  - `401 Unauthorized`: If the user is not logged in.
  - `400 Bad Request`: If the points parameter is invalid.

### Authentication

#### Register

- **URL:** `/register`
- **Method:** `POST`
- **Authentication:** Not required
- **Request Parameters:**
  - `username`: The desired username.
  - `email`: The user's email address.
  - `password`: The user's password.
- **Response:**
  - `201 Created`: If the user is registered successfully.
  - `400 Bad Request`: If required fields are missing or if the username/email is already taken.

#### Login

- **URL:** `/login`
- **Method:** `POST`
- **Authentication:** Not required
- **Request Parameters:**
  - `username`: The user's username.
  - `password`: The user's password.
- **Response:**
  - `200 OK`: If the login is successful.
  - `401 Unauthorized`: If the username or password is incorrect.
  - `400 Bad Request`: If required fields are missing.

#### Logout

- **URL:** `/logout`
- **Method:** `POST`
- **Authentication:** Required
- **Response:**
  - `200 OK`: If the logout is successful.

#### Get Current User

- **URL:** `/api/current_user`
- **Method:** `GET`
- **Authentication:** Required
- **Response:**
  - `200 OK`: Returns the current user's details.
  - `401 Unauthorized`: If the user is not logged in.

### Comments

#### Get Comments of a Post

- **URL:** `/api/posts/<int:post_id>/comments`
- **Method:** `GET`
- **Authentication:** Not required
- **Response:**
  - `200 OK`: Returns a list of comments for the specified post.
  - `404 Not Found`: If the post does not exist or has no comments.

#### Create a New Comment

- **URL:** `/api/posts/<int:post_id>/comments`
- **Method:** `POST`
- **Authentication:** Required
- **Request Parameters:**
  - `comment_text`: The content of the comment.
- **Response:**
  - `201 Created`: If the comment is created successfully.
  - `401 Unauthorized`: If the user is not logged in.
  - `400 Bad Request`: If the comment text is missing.

### Likes

#### Toggle Like on a Post

- **URL:** `/api/posts/<int:post_id>/toggle_like`
- **Method:** `POST`
- **Authentication:** Required
- **Response:**
  - `201 Created`: If the post is liked successfully.
  - `200 OK`: If the like is removed successfully.
  - `401 Unauthorized`: If the user is not logged in.

#### Get Likes of a Post

- **URL:** `/api/posts/<int:post_id>/likes`
- **Method:** `GET`
- **Authentication:** Required
- **Response:**
  - `200 OK`: Returns the total number of likes and whether the current user has liked the post.
  - `401 Unauthorized`: If the user is not logged in.
  - `404 Not Found`: If the post does not exist.

### Rewards

#### Get Rewards

- **URL:** `/api/rewards`
- **Method:** `GET`
- **Authentication:** Not required
- **Response:**
  - `200 OK`: Returns a list of rewards available for users to claim.

#### Claim a Reward

- **URL:** `/api/claim_reward`
- **Method:** `POST`
- **Authentication:** Required
- **Request Parameters:**
  - `reward_id`: The ID of the reward to claim.
- **Response:**
  - `200 OK`: If the reward is claimed successfully.
  - `400 Bad Request`: If the user does not have enough points or if the reward ID is missing.
  - `401 Unauthorized`: If the user is not logged in.
  - `404 Not Found`: If the reward does not exist.
