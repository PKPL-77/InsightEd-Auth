# InsightED API Documentation

## Overview

The InsightED API provides authentication and user management services for the LMS platform. This documentation covers user registration, authentication, and profile management with role-based access controls.

## Authentication API

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register/` | POST | Register a new user account |
| `/api/auth/login/` | POST | Authenticate user and issue JWT tokens |
| `/api/auth/logout/` | POST | Invalidate user session and blacklist tokens |
| `/api/auth/token/refresh/` | POST | Refresh access token using refresh token |

### Authentication Flow

1. **Registration**: New users create an account
2. **Login**: Client sends credentials to obtain access and refresh tokens
3. **Authorization**: Client includes access token in subsequent API requests
4. **Token Refresh**: When access token expires, client uses refresh token to obtain new tokens
5. **Logout**: Client sends refresh token to be blacklisted

### Registration

**Request for Student:**
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "newstudent",
  "password": "securepassword",
  "password2": "securepassword",
  "email": "student@example.com",
  "first_name": "First",
  "last_name": "Last",
  "role": "student"
}
```

**Request for Instructor:**
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "newinstructor",
  "password": "securepassword",
  "password2": "securepassword",
  "email": "instructor@example.com",
  "first_name": "First",
  "last_name": "Last",
  "role": "instructor",
  "keahlian": 5
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Student registered successfully",
  "user": {
    "id": "user-uuid",
    "username": "newuser",
    "email": "user@example.com",
    "role": "student"
  },
  "tokens": {
    "access": "access-token-string",
    "refresh": "refresh-token-string"
  }
}
```

**Note:** Admin registration is not allowed through the API. Admin accounts must be created through the Django admin interface or command-line tools.

### Login

**Request:**
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "username",
  "password": "password"
}
```

**Response:**
```json
{
  "status": "success",
  "user": {
    "id": "user-uuid",
    "username": "username",
    "role": "student|admin|instructor"
  },
  "tokens": {
    "access": "access-token-string",
    "refresh": "refresh-token-string"
  }
}
```

### Logout

**Request:**
```http
POST /api/auth/logout/
Authorization: Bearer <access-token>
Content-Type: application/json

{
  "refresh": "refresh-token-string"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "User logged out successfully"
}
```

### Token Refresh

**Request:**
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "refresh-token-string"
}
```

**Response:**
```json
{
  "status": "success",
  "tokens": {
    "access": "new-access-token-string",
    "refresh": "new-refresh-token-string"
  }
}
```

## User Management API

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/users/profile/` | GET | Retrieve current user's profile information |
| `/users/profile/` | POST | Update current user's profile information |
| `/users/profile/` | DELETE | Delete current user's account |

### User Management Flow

1. **Authentication**: User must be authenticated to access profile endpoints
2. **Profile Retrieval**: User can view their profile information
3. **Profile Updates**: User can update their profile details
4. **Account Deletion**: User can delete their account
5. **Role-Based Access**: Certain fields are only available for specific user roles

### Get User Profile

**Request:**
```http
GET /users/profile/
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "instructor",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "instruktur_id": "550e8400-e29b-41d4-a716-446655440001",
  "keahlian": 5
}
```

**Note:** The response will include role-specific fields depending on the user's role (admin, instructor, or student).

### Update User Profile

**Request for General User Data:**
```http
POST /users/profile/
Authorization: Bearer <access-token>
Content-Type: application/json

{
  "email": "new_email@example.com",
  "first_name": "Updated",
  "last_name": "Name",
  "username": "new_username"
}
```

**Request for Instructor-specific Data:**
```http
POST /users/profile/
Authorization: Bearer <access-token>
Content-Type: application/json

{
  "email": "instructor@example.com",
  "keahlian": 8
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Profile updated successfully"
}
```

**Response (Error):**
```json
{
  "success": false,
  "message": "Error description"
}
```

### Delete User Account

**Request:**
```http
DELETE /users/profile/
Authorization: Bearer <access-token>
```

**Response (Success):**
```json
{
  "success": true,
  "message": "User account deleted successfully"
}
```

## Token Usage

Include the access token in the Authorization header for all authenticated requests:

```http
Authorization: Bearer <access-token>
```

## Error Responses

API errors return appropriate HTTP status codes with descriptive messages:

```json
{
  "status": "error",
  "message": "Error description"
}
```

Common HTTP status codes:
- 200: Success
- 400: Bad request (invalid input)
- 401: Unauthorized (authentication required)
- 403: Forbidden (insufficient permissions)
- 404: Not Found (user profile not found)

## Example Scenarios

### Retrieve Admin User Profile

**Request:**
```http
GET /users/profile/ HTTP/1.1
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "username": "admin_user",
  "email": "admin@example.com",
  "first_name": "Admin",
  "last_name": "User",
  "role": "admin",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "admin_id": "550e8400-e29b-41d4-a716-446655440001",
  "is_staff": true,
  "is_superuser": true
}
```

### Username Already Taken Error

**Request:**
```http
POST /users/profile/ HTTP/1.1
Content-Type: application/json
Authorization: Bearer <access-token>

{
  "username": "existing_username"
}
```

**Response:**
```json
{
  "success": false,
  "message": "Username already taken"
}
```

## Implementation Notes

- The profile update endpoint checks for username conflicts before making changes
- Role-specific fields can only be updated if the user has the correct role
- All endpoints require valid authentication via REST framework's IsAuthenticated permission
- Exceptions during profile updates are caught and returned with descriptive error messages
