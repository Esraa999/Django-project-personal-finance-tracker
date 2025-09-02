# 🏦 Personal Finance Tracker

A Django-based web application for tracking personal income and expenses with REST API, JWT authentication, and Docker deployment.

## 🚀 Features

- **User Authentication**: JWT-based authentication with registration/login
- **Transaction Management**: Full CRUD operations for financial transactions
- **Category System**: Income and expense categories
- **Advanced Filtering**: Search and filter transactions by date, amount, category, etc.
- **Monthly Summaries**: Automated monthly financial summaries
- **CSV Export**: Export transactions for external analysis
- **Dashboard API**: Real-time financial statistics
- **Admin Panel**: Django admin interface for management
- **Docker Ready**: Containerized with Docker Compose
- **PostgreSQL Database**: Production-ready database
- **Automated Cron Jobs**: Monthly summary generation

## 📂 Project Structure

The project follows a modular Django architecture with separate apps for accounts and transactions.

Djangoprojectpersonalfinancetracker/
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── transactions/
│   ├── management/
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       ├── create_sample_data.py
│   │       └── generate_monthly_summaries.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── filters.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/
│   └── index.html
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
├── manage.py
├── README.md
└── requirements.txt


## 🖼 Test Images

I have added a `test_images` folder that contains screenshots demonstrating the project setup and functionality.  
It includes the following subfolders:

- **postman_screenshot/** → Contains API testing screenshots from Postman.
- **postgres_screenshot/** → Contains PostgreSQL database setup and query screenshots.
- **django_website/** → Contains screenshots of the Django website interface.


## 🏗️ Tech Stack

- **Backend**: Django 4.2.7, Django REST Framework
- **Database**: PostgreSQL 15
- **Authentication**: JWT (Simple JWT)
- **Containerization**: Docker & Docker Compose
- **Task Scheduling**: Cron jobs
- **API Documentation**: Built-in API browser

## 📦 Installation & Setup

### Prerequisites
- Docker Desktop installed on your machine
- Git (optional, for version control)

### Quick Start

1. **Clone/Download the project**
   ```bash
   git clone https://github.com/Esraa999/Django-project-personal-finance-tracker
   cd personal-finance-tracker
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```

3. **Build and run with Docker**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - API Documentation: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin
   - Default admin credentials: `admin` / `admin123`

### Manual Setup (Without Docker)

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**
   - Copy `.env.example` to `.env` and update values

3. **Set up database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Run the server**
   ```bash
   python manage.py runserver
   ```

## 📊 Database Schema

### Models Overview

- **User**: Custom user model with authentication
- **Category**: Income/Expense categories
- **Transaction**: Financial transactions with amount, date, description
- **MonthlySummary**: Automated monthly financial summaries

### Database Access

#### Using pgAdmin (Recommended)
1. Download pgAdmin: https://www.pgadmin.org/download/
2. Connect with:
   - Host: `localhost`
   - Port: `5432`
   - Database: `finance_tracker`
   - Username: `postgres`
   - Password: `postgres123`

#### Using VS Code Extension
1. Install "PostgreSQL" extension by Chris Kolkman
2. Create new connection with the same credentials above

#### Using Command Line
```bash
# Access database via Docker
docker-compose exec db psql -U postgres -d finance_tracker

# Common commands
\dt              # List tables
\d table_name    # Describe table
SELECT * FROM accounts_user; # View users
```

## 🔌 API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register/` | Register new user | No |
| POST | `/auth/login/` | Login user | No |
| GET | `/auth/profile/` | Get user profile | Yes |
| POST | `/auth/token/refresh/` | Refresh JWT token | No |

### Transaction Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/categories/` | List all categories | Yes |
| POST | `/categories/` | Create new category | Yes |
| GET | `/transactions/` | List user transactions | Yes |
| POST | `/transactions/` | Create new transaction | Yes |
| GET | `/transactions/{id}/` | Get transaction details | Yes |
| PUT | `/transactions/{id}/` | Update transaction | Yes |
| DELETE | `/transactions/{id}/` | Delete transaction | Yes |

### Report Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/monthly-summaries/` | Get monthly summaries | Yes |
| GET | `/dashboard/` | Get dashboard statistics | Yes |
| GET | `/export-csv/` | Export transactions as CSV | Yes |

### Filtering & Search

The transactions endpoint supports advanced filtering:

| Parameter | Description | Example |
|-----------|-------------|---------|
| `start_date` | Filter from date | `?start_date=2024-01-01` |
| `end_date` | Filter to date | `?end_date=2024-12-31` |
| `category` | Filter by category ID | `?category=1` |
| `category_type` | Filter by income/expense | `?category_type=expense` |
| `amount_min` | Minimum amount | `?amount_min=100` |
| `amount_max` | Maximum amount | `?amount_max=1000` |
| `search` | Search description/category | `?search=grocery` |
| `ordering` | Sort results | `?ordering=-date` |

**Example combined filtering:**
```
/api/transactions/?category_type=expense&start_date=2024-01-01&amount_min=50&search=food&ordering=-amount
```

## 🔧 API Usage Examples

### 1. User Registration
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }'
```

### 2. User Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepassword123"
  }'
```

### 3. Create Category
```bash
curl -X POST http://localhost:8000/api/categories/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "name": "Groceries",
    "type": "expense"
  }'
```

### 4. Create Transaction
```bash
curl -X POST http://localhost:8000/api/transactions/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "category": 1,
    "amount": "150.00",
    "description": "Weekly grocery shopping",
    "date": "2024-01-15"
  }'
```

### 5. Get Transactions with Filtering
```bash
curl -X GET "http://localhost:8000/api/transactions/?category_type=expense&start_date=2024-01-01" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 6. Export Transactions as CSV
```bash
curl -X GET "http://localhost:8000/api/export-csv/?start_date=2024-01-01&end_date=2024-12-31" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -o transactions.csv
```

## ⏰ Cron Job Configuration

The application includes automated monthly summary generation:

### Cron Schedule
- **Frequency**: Monthly (1st day of each month at midnight)
- **Command**: `python manage.py generate_monthly_summaries`
- **Purpose**: Automatically calculates and stores monthly income/expense summaries

### Manual Execution
```bash
# Run the cron job manually
docker-compose exec web python manage.py generate_monthly_summaries

# Or without Docker
python manage.py generate_monthly_summaries
```

### Cron Job Details
- Processes all users' transactions from the previous month
- Calculates total income and expenses
- Creates/updates MonthlySummary records
- Runs automatically via Docker container cron service

## 🛠️ Development

### Project Structure
```
finance_tracker/
├── accounts/              # User authentication app
├── transactions/          # Main transactions app
├── config/               # Django settings
├── templates/            # HTML templates
├── docker-compose.yml    # Docker configuration
├── Dockerfile           # Docker image definition
├── requirements.txt     # Python dependencies
├── entrypoint.sh       # Docker entrypoint script
└── README.md           # This file
```

### Running Tests
```bash
# With Docker
docker-compose exec web python manage.py test

# Without Docker
python manage.py test
```

### Creating Sample Data
```bash
# Access Django shell
docker-compose exec web python manage.py shell

# Create sample categories
from transactions.models import Category
Category.objects.create(name='Salary', type='income')
Category.objects.create(name='Groceries', type='expense')
Category.objects.create(name='Transportation', type='expense')
```

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Validation**: Django's built-in password validators
- **CORS Configuration**: Configured for development
- **Database Security**: PostgreSQL with user credentials
- **Admin Interface**: Protected Django admin panel

## 📝 Environment Variables

Create a `.env` file with these variables:

```env
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=1
DATABASE_URL=postgresql://postgres:postgres123@db:5432/finance_tracker
JWT_SECRET_KEY=your-jwt-secret-key-here
```

## 🐳 Docker Services

The application runs three Docker services:

1. **web**: Django application server
2. **db**: PostgreSQL database
3. **cron**: Cron job service for automated tasks

### Docker Commands
```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop services
docker-compose down

# Rebuild and start
docker-compose up --build
```

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL container is running
   - Check database credentials in docker-compose.yml

2. **Port Already in Use**
   - Change port in docker-compose.yml from 8000 to another port
   - Or stop other services using port 8000

3. **Permission Denied (entrypoint.sh)**
   ```bash
   chmod +x entrypoint.sh
   ```

4. **Migration Issues**
   ```bash
   docker-compose exec web python manage.py makemigrations
   docker-compose exec web python manage.py migrate
   ```

### Logs and Debugging
```bash
# View Django logs
docker-compose logs web

# View database logs
docker-compose logs db

# Access container shell
docker-compose exec web bash

# View database data
docker-compose exec db psql -U postgres -d finance_tracker
```

## 📈 Future Enhancements

- **Frontend Interface**: React/Vue.js frontend
- **Charts and Visualizations**: Transaction trends and spending patterns
- **Budget Management**: Budget creation and tracking
- **Recurring Transactions**: Automated recurring income/expenses
- **Multi-currency Support**: Support for different currencies
- **Bank Integration**: Import transactions from bank APIs
- **Mobile App**: React Native mobile application



