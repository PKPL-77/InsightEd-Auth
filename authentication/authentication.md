# Authentication API Documentation

## Overview

The InsightED Authentication API provides JWT (JSON Web Token) based authentication services for the LMS platform. This API handles user registration (students and instructors only), login, logout, and token refresh operations.

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register/` | POST | Register a new user account |
| `/api/auth/login/` | POST | Authenticate user and issue JWT tokens |
| `/api/auth/logout/` | POST | Invalidate user session and blacklist tokens |
| `/api/auth/token/refresh/` | POST | Refresh access token using refresh token |

## Authentication Flow

1. **Registration**: New users create an account
2. **Login**: Client sends credentials to obtain access and refresh tokens
3. **Authorization**: Client includes access token in subsequent API requests
4. **Token Refresh**: When access token expires, client uses refresh token to obtain new tokens
5. **Logout**: Client sends refresh token to be blacklisted

## API Usage

### Register

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

## Token Usage

Include the access token in the Authorization header for all authenticated requests:

```http
Authorization: Bearer <access-token>
```

## Error Responses

Authentication errors return appropriate HTTP status codes with descriptive messages:

```json
{
  "status": "error",
  "message": "Error description"
}
```

Common HTTP status codes:
- 200: Success
- 400: Bad request (invalid input)
- 401: Unauthorized (invalid or expired token)
- 403: Forbidden (insufficient permissions)
