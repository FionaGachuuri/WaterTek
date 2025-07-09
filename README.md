# WaterTek

> A smart, role based water billing and issue reporting system built with Flask. 
Designed for modern utility management simple for users, powerful for admins.


---

## The Story Behind WaterTek

**The Problem:** Managing community water supply is tedious when it's decentralized, manual, or paper-based.
Utilities struggle with:
- Manual bill generation and payment tracking.
- No centralized system for issue reporting.
- Lack of role based access control.
- No real time insights into usage and revenue.

**The Solution:** WaterTek provides a unified platform that streamlines water utility management through:
- Automated bill generation and payment tracking.
- Centralized issue reporting for burst pipes, supply outages, etc.
- Role based access control for admins, clerks, and users.
- Real time dashboards with usage and revenue insights.

**When to Use WaterTek:**
- Small to medium water utilities
- Community water management systems
- Municipal water departments
- Private water service providers

---

##  Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Python 3.10+ | Core application logic |
| **Framework** | Flask 3.1 | Web framework |
| **Authentication** | Flask-JWT-Extended | Secure API authentication |
| **Database** | MySQL + PyMySQL | Data persistence |
| **ORM** | Flask-SQLAlchemy | Database abstraction |
| **Migrations** | Alembic | Database version control |
| **Production Server** | Gunicorn | WSGI server |
| **Templates** | Jinja2 | HTML rendering |

---

## Developer Journey

```bash
# Clone and navigate
git clone https://github.com/FionaGachuuri/WaterTek.git
cd WaterTek

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

####  Environment Configuration

Create a `.env` file in the project root:

```env
# Development Settings
FLASK_ENV=development
FLASK_DEBUG=True

# Security Keys (Generate your own!)
SECRET_KEY=your-settings
JWT_SECRET_KEY=your-settings
DB_USER=your-settings
DB_PASSWORD=your-settings
DB_HOST=your-settings
DB_PORT=your-settings
DB_NAME=your-settings

# Database Configuration
DATABASE_URL=mysql+pymysql://username:password@localhost/DB_NAME

```

 **Security Warning:** Never commit your `.env` file to version control. Add it to `.gitignore`.

#### First Run

```bash
# Initialize database
flask db upgrade

# Start development server
flask run
```

Your app will be running at `http://127.0.0.1:5000`

####  Common Setup Issues

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'dotenv'` | `pip install python-dotenv` |
| `Access denied for user` | Check MySQL credentials in `.env` |
| `Table doesn't exist` | Run `flask db upgrade` |
| `Port already in use` | Change port: `flask run --port 5001` |


##  Architecture Overview

```
WaterTek/
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── venv/                        # Python virtual environment (not versioned)
├── test/                        # Test files (unit/integration tests)

├── app/                         # Main application package
│   ├── __init__.py              # App level setup
│
│   ├── models/                  # Database models and ORM setup
│   │   ├── __init__.py
│   │   ├── base_model.py        # Common base class for all models
│   │   ├── bill.py              # Bill model
│   │   ├── issue.py             # Issue model
│   │   ├── meter_reading.py     # Meter reading model
│   │   ├── user.py              # User model
│   │   └── engine/
│   │       ├── db_storage.py    # SQLAlchemy DB engine configuration
│
│   ├── services/                # Business logic 
│   │   └── billing.py           # Billing logic and helpers
│
│   ├── utils/                   # Utility modules
│   │   ├── __init__.py
│   │   └── decorators.py        # Custom decorators
│
│   └── web_flask/               # Web app (Flask)
│       ├── run.py               # App entrypoint for running Flask
│       ├── routes/              # Flask Blueprints
│       │   ├── __init__.py
│       │   ├── admin.py
│       │   ├── auth.py
│       │   ├── billing.py
│       │   ├── dashboard.py
│       │   ├── issues.py
│       │   └── user.py
│       └── templates/           # HTML templates
│           ├── base.html        # Shared layout template
│           ├── login.html       # Login page
│           ├── register.html    # Registration page
│           ├── dashboard.html   # General dashboard
│           ├── admin/           # Admin-specific views
│           │   ├── bills.html
│           │   ├── dashboard.html
│           │   ├── issues.html
│           │   ├── user_detail.html
│           │   └── users.html
│           └── user/            # User-specific views
│               ├── dashboard.html
│               ├── report_issue.html
│               └── submit_reading.html

```

### Design Principles

1. **Separation of Concerns:** API and web interfaces are separate modules
2. **Role Based Access:** Every endpoint respects user permissions
3. **Database Abstraction:** SQLAlchemy ORM for database independence
4. **Scalable Architecture:** Blueprint-based structure for easy extension


## Contributing

### Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes.
4. Add tests for new functionality.
5. Ensure all tests pass: `pytest`
6. Commit your changes: `git commit -m 'Add amazing feature'`
7. Push to the branch: `git push origin feature/amazing-feature`
8. Open a Pull Request


## License

This project is licensed under the MIT License.


##  Acknowledgments

- Built by:
[Fiona Gachuuri](https://github.com/FionaGachuuri)
[Maurice Ngicho](https://github.com/MauriceNgicho)
[Alex Kinyanjui](https://github.com/xander254)
- Inspired by modern utility management needs

## Deployed version
https://watertek.onrender.com
