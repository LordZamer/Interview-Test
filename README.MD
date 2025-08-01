# Super Admin Dashboard Backend (Django)

This is the backend implementation for the **Super Admin Dashboard with Role-Based Access Control**. It uses Django and Django REST Framework with JWT authentication to manage user accounts, roles, page-level permissions, and comment histories.

---

## 🚀 Features

### ✅ Authentication

* JWT-based authentication (access + refresh)
* 1-hour session expiry on inactivity
* Super admin and regular user login flow

### ✅ Role-Based Access Control

* Super admin can:

  * Create users
  * Assign `view`, `edit`, `create`, `delete` permissions per page
* Regular users can:

  * Access only permitted pages
  * View/edit/delete comments based on access level

### ✅ Page & Comment Management

* 10 predefined pages
* Comments linked to pages
* Edit/delete restrictions based on permissions
* Super admin can view full comment history

---

## 📁 Directory Structure

```
backend/
├── permissions/           # User model, PagePermission model
├── comments/              # Page, Comment, CommentHistory models and views
├── serializers.py         # DRF serializers
├── views.py               # ViewSets for Pages and Comments
└── settings.py            # JWT setup, installed apps
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/LordZamer/Interview-Test.git
cd backend
```

### 2. Create virtual environment & install dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create superuser

```bash
python manage.py createsuperuser
```

### 5. Run server

```bash
python manage.py runserver
```

---

## 🔐 API Endpoints (Core)

| Method | Endpoint                | Description                    |
| ------ | ----------------------- | ------------------------------ |
| POST   | /api/token/             | Get JWT access & refresh token |
| POST   | /api/token/refresh/     | Refresh access token           |
| GET    | /pages/                 | List available pages           |
| GET    | /comments/?page\_id=xyz | List comments per page         |
| POST   | /comments/              | Add new comment                |
| PUT    | /comments//             | Edit comment                   |
| DELETE | /comments//             | Delete comment                 |

---

## 🔒 Permission Model

Permissions are assigned per user per page with access types:

* `view`
* `edit`
* `create`
* `delete`

---

---

## 📦 Requirements

```
django>=4.2
djangorestframework
djangorestframework-simplejwt
```

---

##

---

##
