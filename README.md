# ALX Backend Caching - Property Listings

This project implements a Django-based property listing application with Redis caching at multiple levels. The system demonstrates various caching strategies including view-level caching, low-level queryset caching, and proper cache invalidation techniques.

## Project Structure

```
alx-backend-caching_property_listings/
├── alx_backend_caching_property_listings/
│   ├── settings.py          # Django settings with PostgreSQL and Redis configuration
│   ├── urls.py              # Main URL configuration
│   └── ...
├── properties/
│   ├── models.py            # Property model definition
│   ├── views.py             # Cached property list view
│   ├── urls.py              # Properties app URL configuration
│   ├── utils.py             # Caching utilities and metrics
│   ├── signals.py           # Cache invalidation signals
│   ├── apps.py              # App configuration with signal registration
│   └── __init__.py          # App initialization
├── docker-compose.yaml      # Docker configuration for PostgreSQL and Redis
├── manage.py                # Django management script
└── README.md                # This file
```

## Features Implemented

### Task 0: Django Project Setup with Dockerized PostgreSQL and Redis
- Django project initialized with `properties` app
- Property model with fields: title, description, price, location, created_at
- PostgreSQL database configured in Docker
- Redis cache backend configured
- Database migrations created and applied

### Task 1: Cache Property List View
- `property_list` view returns all properties as JSON
- View cached for 15 minutes using `@cache_page(60 * 15)` decorator
- URL mapped to `/properties/`

### Task 2: Low-Level Caching for Property Queryset
- `get_all_properties()` function in `properties/utils.py`
- Checks Redis cache first with `cache.get('all_properties')`
- Falls back to database if cache miss
- Stores queryset in cache for 1 hour (3600 seconds)

### Task 3: Cache Invalidation Using Signals
- Django signals in `properties/signals.py`
- `post_save` signal handler invalidates cache on Property create/update
- `post_delete` signal handler invalidates cache on Property delete
- Signals automatically registered in `properties/apps.py`

### Task 4: Cache Metrics Analysis
- `get_redis_cache_metrics()` function in `properties/utils.py`
- Retrieves keyspace_hits and keyspace_misses from Redis INFO
- Calculates and returns hit ratio percentage
- Logs metrics using Python's logging framework

## Setup Instructions

### Prerequisites
- Python 3.8+
- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/garisonmike/alx-backend-caching_property_listings.git
cd alx-backend-caching_property_listings
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
```

3. Install Python dependencies:
```bash
pip install django django-redis psycopg2-binary redis
```

4. Start PostgreSQL and Redis containers:
```bash
docker compose up -d
```

5. Apply database migrations:
```bash
python manage.py migrate
```

6. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Usage

### API Endpoints

#### Get All Properties
```bash
GET /properties/
```

Returns a JSON response with all properties:
```json
{
  "properties": [
    {
      "id": 1,
      "title": "Beach House",
      "description": "Beautiful beach house with ocean view",
      "price": "500000.00",
      "location": "Miami Beach",
      "created_at": "2025-11-02T14:15:14.080108+00:00"
    }
  ]
}
```

### Testing Cache Behavior

1. Create test properties using Django shell:
```bash
python manage.py shell
```

```python
from properties.models import Property
from decimal import Decimal

Property.objects.create(
    title="Beach House",
    description="Beautiful beach house with ocean view",
    price=Decimal("500000.00"),
    location="Miami Beach"
)
```

2. Test cache metrics:
```bash
python test_cache_metrics.py
```

3. Verify caching by making multiple requests:
```bash
curl http://127.0.0.1:8000/properties/
```

First request will hit the database, subsequent requests within 15 minutes will be served from cache.

### Cache Invalidation Testing

Create, update, or delete a property to see cache invalidation in action:

```python
from properties.models import Property

# This will automatically invalidate the cache
Property.objects.create(title="New Property", description="Test", price=100000, location="Test City")
```

## Docker Services

### PostgreSQL
- Image: `postgres:15`
- Port: `5432`
- Database: `property_db`
- User: `property_user`
- Password: `property_pass`

### Redis
- Image: `redis:7`
- Port: `6379`

## Configuration

### Database Settings (settings.py)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'property_db',
        'USER': 'property_user',
        'PASSWORD': 'property_pass',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Cache Settings (settings.py)
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

## Performance Benefits

- **View-level caching**: Reduces response time for frequently accessed endpoints
- **Queryset caching**: Minimizes database queries for expensive operations
- **Cache invalidation**: Ensures data consistency when records change
- **Metrics tracking**: Monitors cache effectiveness and hit ratios

## Monitoring

Check Redis cache metrics:
```python
from properties.utils import get_redis_cache_metrics

metrics = get_redis_cache_metrics()
print(f"Hit Ratio: {metrics['hit_ratio']}%")
```

## Development

### Running Tests
```bash
python manage.py test properties
```

### Checking Cache Status
```bash
# Connect to Redis CLI
docker exec -it property_redis redis-cli

# Check cached keys
KEYS *

# Get cache statistics
INFO stats
```

## Troubleshooting

### Cannot connect to PostgreSQL
- Ensure Docker containers are running: `docker compose ps`
- Check database connection settings in `settings.py`

### Cannot connect to Redis
- Verify Redis container is running: `docker compose ps`
- Check Redis connection: `docker exec -it property_redis redis-cli PING`

### Migrations not applying
- Stop the server
- Run: `python manage.py migrate`
- Restart the server

## License

This project is part of the ALX Backend Specialization curriculum.

## Author

Built as part of ALX Software Engineering Program
