# XpertsHub

A Django-based service marketplace connecting customers with professional service providers across various categories including plumbing, painting, housekeeping, electrical work, and more.

## Features

- User registration and authentication for customers and companies
- Email-based login system
- User profiles displaying personal information and activity
- Service marketplace with multiple categories
- Responsive design with Tailwind CSS
- Component-based template architecture

## Technology Stack

- Django 5.2.8
- Python 3.12
- PostgreSQL
- Tailwind CSS
- Boxicons for UI icons

## Installation

### Prerequisites

- Python 3.12 or higher
- PostgreSQL
- Node.js (for Tailwind CSS)

### Clone Repository

```bash
git clone https://github.com/johneliud/xpertshub.git
cd xpertshub
```

### Setup Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Configuration

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=xpertshub_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Tailwind CSS Setup

```bash
python manage.py tailwind install
python manage.py tailwind build
```

### Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

## User Types

### Customers
- Register with username, email, and date of birth
- Browse and request services
- View service request history in profile

### Companies
- Register with company name, email, and field of work
- Offer services in their specialization
- Manage service listings through profile

## Service Categories

- Air Conditioner
- Carpentry
- Electricity
- Gardening
- Home Machines
- Housekeeping
- Interior Design
- Locks
- Painting
- Plumbing
- Water Heaters
- All in One (for companies offering multiple services)

## Development

### Running Tailwind in Watch Mode

```bash
python manage.py tailwind start
```

### Creating Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
