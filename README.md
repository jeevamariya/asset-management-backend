# Smart Asset & Inventory Management System — Backend

Django REST API backend for the Smart Asset & Inventory Management System.

## Technologies

* Python
* Django
* Django REST Framework
* PostgreSQL
* JWT Authentication
* Google Gemini API
* Docker
* Gunicorn
* NGINX
* Render

## Features

* JWT-based user authentication
* Admin and Employee roles
* Asset management
* Inventory management
* Asset assignments
* Repair ticket management
* Dashboard analytics
* Search and filtering
* Pagination
* AI Assistant using Google Gemini
* AI conversation history
* PostgreSQL database
* Dockerized backend
* Production deployment on Render

## User Roles

### Admin

Admins can:

* Add, edit and delete assets
* Manage inventory
* Manage assignments
* Manage repair tickets
* Access Django Admin

### Employee

Employees can:

* View assets
* View inventory
* View assignments
* View repair tickets
* Use the AI Assistant

Employees have read-only access to the main system data.

## API Endpoints

### Authentication

```text
POST /api/token/
POST /api/token/refresh/
POST /api/token/logout/
```

### Assets

```text
GET/POST /api/assets/
GET/PUT/PATCH/DELETE /api/assets/<id>/
```

### Inventory

```text
GET/POST /api/inventory/
GET/PUT/PATCH/DELETE /api/inventory/<id>/
```

### Assignments

```text
GET/POST /api/assignments/
GET/PUT/PATCH/DELETE /api/assignments/<id>/
```

### Repair Tickets

```text
GET/POST /api/tickets/
GET/PUT/PATCH/DELETE /api/tickets/<id>/
```

### Dashboard

```text
GET /api/dashboard/
```

### User Information

```text
GET /api/me/
GET /api/users/
```

### AI Assistant

```text
POST /api/ai/chat/
GET /api/ai/conversations/
```

## Database

The application uses PostgreSQL.

PostgreSQL is used locally through Docker Compose and in production through Render PostgreSQL.

Database credentials, secret keys and API keys are stored as environment variables and are not committed to the repository.

## AI Assistant

The backend integrates Google Gemini API for the AI Assistant.

The system stores:

* AI conversations
* User messages
* Assistant responses

The AI Assistant is designed to provide responses while avoiding unsupported information about the asset management system.

## Docker

The backend is Dockerized and runs with Gunicorn.

The local project includes:

* Django backend
* PostgreSQL
* React frontend
* NGINX reverse proxy

### Local Docker Setup

```bash
docker compose build
docker compose up
```

Local application:

```text
http://localhost/
```

Django Admin:

```text
http://localhost/admin/
```

## Production Deployment

The backend is deployed on Render using Docker.

Backend:

https://asset-management-backend-s6nx.onrender.com

The production database is PostgreSQL hosted by Render.

Deployment is connected to the GitHub repository for automatic deployment when changes are pushed to the configured branch.

## Project Structure

```text
asset_management/
├── asset_management/
├── assets/
├── nginx/
├── Dockerfile
├── docker-compose.yml
├── startup.sh
├── requirements.txt
├── manage.py
└── README.md
```

## Security

* JWT authentication is used for API access.
* Admin-only modification permissions are enforced.
* Secret keys and API keys are stored using environment variables.
* Database credentials are not committed to GitHub.
* Debug mode is disabled in production.

## Project Status

The backend is Dockerized, connected to PostgreSQL, integrated with the React frontend, deployed on Render, and available through the production API.
