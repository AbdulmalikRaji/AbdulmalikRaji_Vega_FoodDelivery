# Food Delivery App

A Django & React-powered food delivery app with authentication, real-time order tracking, and background task processing using Celery & Redis.

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/food_delivery.git
cd food_delivery
```

## 2. Create a Virtual Environment & Install Dependencies

```bash
python -m venv .venv
source .venv/Scripts/activate  # For Windows
# OR
source .venv/bin/activate  # For Mac/Linux

pip install -r requirements.txt
```

## 3. Set Up Environment Variables

Create a .env file in the root directory and add:

```text
SECRET_KEY=your-secret-key
DEBUG=True 
GOOGLE_MAPS_API_KEY=apikey #optional only for hen users dont accept location permissions

# Database (PostgreSQL)
POSTGRES_NAME=food_delivery_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Redis (Celery Broker)
CELERY_BROKER_URL=redis://localhost:6379/0

# Auth Tokens Expiry
ACCESS_TOKEN_LIFETIME_MINUTES=30 
REFRESH_TOKEN_LIFETIME_MINUTES=1440

# API Base URL
API_BASE_URL=http://127.0.0.1:8000

# SMTP
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_ADDRESS="fooddelivery@gmail.com"
EMAIL_PASSWORD=yourpassword

# NPM path for tailwind build if needed
NPM_PATH ="C:/Program Files/nodejs/npm.cmd"
```

## 4. Apply Migrations

```bash
python manage.py migrate
```

## 5. Build Tailwind CSS

Build the tailwind styles before running the server:

```bash
python manage.py tailwind build
```

## 6. Create a Superuser (Admin Panel)

```bash
python manage.py createsuperuser
```

## 7. Start Redis (Message Broker)

Make sure Docker is installed, then run:

```bash
docker run --name redis-server -d -p 6379:6379 redis
```

Or, if using an existing container:

```bash
docker start redis-server
```

## 8. Start Celery Workers

Celery handles background tasks like order processing. Open a new terminal and run:

```bash
celery -A food_delivery worker --loglevel=info
```

## 9. Run the Development Server

```bash
python manage.py runserver
```

Visit ```http://127.0.0.1:8000/``` to see the app.

Visit ```http://127.0.0.1:8000/admin``` to login to admin panel.

## 10. API Endpoints

The API includes:

- User Authentication (/api/user/login/, /api/user/register/, /api/user/auth/token/refresh/)
- Food Menu (/api/restaurants/food/)
- Order Processing (/api/orders/order/)
- Order Rating (/api/orders/rate-order/)

For full API documentation, use Postman or check urls.py.
