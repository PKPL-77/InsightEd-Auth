# User Management API Documentation

## Overview

The InsightED User Management API handles user profile operations within the LMS platform. This API provides access to user profile information and profile update capabilities with role-based access controls.

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/users/profile/` | GET | Retrieve current user's profile information |
| `/users/profile/` | POST | Update current user's profile information |
| `/users/profile/` | DELETE | Delete current user's account |

## User Management Flow

1. **Authentication**: User must be authenticated to access profile endpoints
2. **Profile Retrieval**: User can view their profile information
3. **Profile Updates**: User can update their profile details
4. **Account Deletion**: User can delete their account
5. **Role-Based Access**: Certain fields are only available for specific user roles

## API Usage

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

**Response (Error):**
```json
{
  "success": false,
  "message": "Error description"
}
```

## Token Usage

Include the access token in the Authorization header for all authenticated requests:

```http
Authorization: Bearer <access-token>
```

## Error Responses

User Management errors return appropriate HTTP status codes with descriptive messages:

```json
{
  "success": false,
  "message": "Error description"
}
```

Common HTTP status codes:
- 200: Success
- 400: Bad request (invalid input)
- 401: Unauthorized (authentication required)
- 404: Not Found (user profile not found)

## Example Scenarios

### Example: Retrieve Admin User Profile

**Request:**
```http
GET /users/profile/ HTTP/1.1
Authorization: Bearer <access-token>
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

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

### Example: Username Already Taken Error

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
```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "success": false,
  "message": "Username already taken"
}
```

### Example: Delete User Account

**Request:**
```http
DELETE /users/profile/ HTTP/1.1
Authorization: Bearer <access-token>
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "success": true,
  "message": "User account deleted successfully"
}
```

## Implementation Notes

- The profile update endpoint checks for username conflicts before making changes
- Role-specific fields can only be updated if the user has the correct role
- All endpoints require valid authentication via REST framework's IsAuthenticated permission
- Exceptions during profile updates are caught and returned with descriptive error messages
