# Base43 API Documentation

## Overview

Base43 provides a RESTful API built with Django REST Framework. All API endpoints are prefixed with `/api/v1/`.

## Authentication

The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-token>
```

### Authentication Endpoints

#### Register
`POST /api/v1/auth/register/`

Request:
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### Login
`POST /api/v1/auth/login/`

Request:
```json
{
  "username": "johndoe",
  "password": "securepassword"
}
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1...",
  "refresh": "eyJ0eXAiOiJKV1...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  }
}
```

#### Refresh Token
`POST /api/v1/auth/refresh/`

Request:
```json
{
  "refresh": "eyJ0eXAiOiJKV1..."
}
```

## Common Endpoints Pattern

Most modules follow a similar RESTful pattern:

- `GET /api/v1/{module}/` - List all items (paginated)
- `POST /api/v1/{module}/` - Create new item
- `GET /api/v1/{module}/{id}/` - Get specific item
- `PUT /api/v1/{module}/{id}/` - Update specific item
- `PATCH /api/v1/{module}/{id}/` - Partial update
- `DELETE /api/v1/{module}/{id}/` - Delete specific item

### Common Query Parameters

- `page` - Page number for pagination
- `page_size` - Number of items per page (default: 20)
- `search` - Search term for filtering
- `ordering` - Field to order by (prefix with `-` for descending)

## Module-Specific Endpoints

### Projects (`/api/v1/proyectos/`)

Additional endpoints:
- `GET /api/v1/proyectos/categories/` - List project categories
- `GET /api/v1/proyectos/{id}/updates/` - Get project updates
- `POST /api/v1/proyectos/{id}/publish/` - Publish a project
- `POST /api/v1/proyectos/{id}/unpublish/` - Unpublish a project

### News (`/api/v1/noticias/`)

Query parameters:
- `category` - Filter by category ID
- `is_featured` - Filter featured articles
- `published_after` - Filter articles published after date

### Chat (`/api/v1/chat/`)

WebSocket endpoint: `ws://localhost:8000/ws/chat/{room_name}/`

REST endpoints:
- `GET /api/v1/chat/rooms/` - List chat rooms
- `GET /api/v1/chat/rooms/{id}/messages/` - Get room messages
- `POST /api/v1/chat/rooms/{id}/join/` - Join a room

### Contact (`/api/v1/contacto/`)

Public endpoint:
- `POST /api/v1/contacto/messages/` - Submit contact form

Admin endpoints:
- `GET /api/v1/contacto/messages/` - List all messages
- `GET /api/v1/contacto/stats/` - Get contact statistics

## Response Format

### Success Response
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    // Response data
  }
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error description",
  "errors": {
    "field_name": ["Error message"]
  }
}
```

### Paginated Response
```json
{
  "count": 100,
  "next": "http://api.example.com/resource/?page=2",
  "previous": null,
  "results": [
    // Array of items
  ]
}
```

## Status Codes

- `200 OK` - Request succeeded
- `201 Created` - Resource created successfully
- `204 No Content` - Resource deleted successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Rate Limiting

API requests are limited to:
- Anonymous users: 100 requests per hour
- Authenticated users: 1000 requests per hour

## CORS

CORS is configured to allow requests from the frontend domain. Update `CORS_ALLOWED_ORIGINS` in settings for production.

## API Documentation Tools

- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`

These tools provide interactive API documentation and testing capabilities.