# Django Shop

A full-stack e-commerce application built with Django REST Framework and React.

## Project Structure

This project consists of two main parts:

1. **Backend (Django)**: Located in the `shoppit` directory
2. **Frontend (React)**: Located in the `shoppit_app` directory

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root (use `.env.example` as a template)

4. Run migrations:
   ```
   cd shoppit
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```
   python manage.py runserver
   ```

### Frontend Setup

1. Install dependencies:
   ```
   cd shoppit_app
   npm install
   ```

2. Create a `.env` file in the `shoppit_app` directory with:
   ```
   VITE_API_BASE_URL=http://127.0.0.1:8000
   ```

3. Start the development server:
   ```
   npm run dev
   ```

## Deployment

This project includes two deployment options:

1. **Django with Gunicorn/Whitenoise**: The standard Django deployment using the files in the `shoppit` directory.

2. **Flask Deployment for Railway**: The `main.py` file in the root directory is a minimal Flask application that can be used for deploying to Railway or similar platforms. This is separate from the Django application and serves as an alternative deployment option.

## Environment Variables

See `.env.example` for required environment variables.

## Features

- User authentication with JWT
- Product browsing and filtering
- Shopping cart functionality
- Checkout with PayPal and Flutterwave payment integration
- Order history