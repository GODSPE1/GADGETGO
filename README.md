
<h1>WEBSTACK PORTFOLIO PROJECT</h1>
This is an E-commerce api

RESTful HTTP API using Python Flask that allows users to manage their ecommerce platform.

### Signin User
- Create a user 
- users can login
- user can logout
- Create an order

### Admin Priviledges
Add New Product
Update a product
See all users
Create a user
# GADGETGO — E-commerce REST API

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

**GADGETGO** is a robust, production-ready RESTful API for an e-commerce platform. It provides a complete backend solution for managing users, products, categories, orders, and payments. Built with Flask and SQLAlchemy, it features secure JWT authentication, role-based access control, and image handling.

## 🚀 Features

- **User Management**: Registration, Login (JWT), Logout (Token Blacklist), Profile management.
- **Product Catalog**: CRUD operations for products and categories.
- **Order Processing**: Create, view, update, and cancel orders.
- **Image Handling**: Support for product images (via Pillow).
- **Security**: Password hashing (Bcrypt), JWT Authentication, Token Blacklisting.
- **Database**: SQLAlchemy ORM with SQLite (default) or PostgreSQL/MySQL support.
- **Migrations**: Database schema migrations using Flask-Migrate.
- **Deployment Ready**: Gunicorn configuration included.

## 🛠️ Tech Stack

- **Framework**: Flask
- **Database**: SQLAlchemy (ORM), SQLite (Dev)
- **Authentication**: PyJWT, Flask-Login
- **Forms/Validation**: Flask-WTF
- **Utilities**: Pillow (Images), Flask-Mail (Email), Flask-Migrate (DB Migrations)
- **Server**: Gunicorn

## 📂 Project Structure

```
GADGETGO/
├── app/
│   └── v1/
│       ├── models/       # Database models (User, Product, Order)
│       ├── routes/       # API endpoints (Blueprints)
│       ├── utils/        # Helper functions (Auth, Tokens)
│       ├── templates/    # HTML templates (if using UI)
│       └── __init__.py   # App factory
├── instance/             # SQLite database location
├── migrations/           # Database migration scripts
├── config.py             # Configuration settings
├── run.py                # Entry point
├── requirements.txt      # Dependencies
└── README.md             # Documentation
```

## ⚡ Installation & Setup

### Prerequisites
- Python 3.8+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/GODSPE1/GADGETGO.git
cd GADGETGO
```

### 2. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```bash
export SECRET_KEY="your-super-secret-key"
export FLASK_APP=run.py
export FLASK_ENV=development
```

### 5. Initialize Database
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```
*Note: If you just want to run with the default setup, the app will create the DB on first run if configured in `__init__.py`.*

### 6. Run the Application
```bash
flask run
```
The API will be available at `http://127.0.0.1:5000`.

## 📖 API Documentation

### Authentication
| Method | Endpoint | Description | Auth |
| :--- | :--- | :--- | :--- |
| `POST` | `/auth/register` | Register a new user | No |
| `POST` | `/auth/login` | Login & get JWT token | No |
| `POST` | `/auth/logout` | Logout (Blacklist token) | **Yes** |

### Products
| Method | Endpoint | Description | Auth |
| :--- | :--- | :--- | :--- |
| `GET` | `/products` | Get all products | No |
| `GET` | `/products/<id>` | Get product details | No |
| `POST` | `/products` | Create a product | **Admin** |
| `PUT` | `/products/<id>` | Update a product | **Admin** |
| `DELETE` | `/products/<id>` | Delete a product | **Admin** |

### Orders
| Method | Endpoint | Description | Auth |
| :--- | :--- | :--- | :--- |
| `GET` | `/orders` | Get all orders | **Admin** |
| `POST` | `/orders` | Place a new order | **User** |
| `GET` | `/orders/<id>` | Get order details | **User/Admin** |

## 🧪 Testing

Run the tests (if available) or use `curl` to test endpoints manually.

**Example: Login**
```bash
curl -X POST http://127.0.0.1:5000/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"admin", "password":"password"}'
```

## 🚀 Deployment

To run in production using Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
