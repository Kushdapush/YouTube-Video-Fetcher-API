# YouTube Video Fetcher API

A Django-based project for fetching, storing, and serving YouTube videos using the YouTube Data API. The system supports periodic fetching of the latest videos, API key management, and a RESTful API for querying video data.

---

## 🚀 Features
- Fetch the latest YouTube videos based on a search query
- Automatic handling of YouTube API key quotas with fallback to alternate keys
- RESTful API for querying video data with pagination
- Admin interface for managing videos and API keys
- Background task processing using Celery and Redis
- Periodic fetching of videos using Celery Beat
- **Environment-based configuration using .env**

---

## 🛠 Tech Stack
- **Django** (Web framework)
- **Django REST Framework** (API development)
- **PostgreSQL** (Database for storing video and API key data)
- **Celery** (Task queue for background processing)
- **Redis** (Message broker for Celery)
- **Python-dotenv** (Environment variable management)

---

## 🏗️ System Architecture

```
┌───────────────────┐       ┌────────────────────┐       ┌──────────────────┐
│                   │       │                    │       │                  │
│   YouTube API     ├──────►│   Celery Worker    ├──────►│   PostgreSQL     │
│                   │       │   - Fetch Videos   │       │   - Video Data   │
│                   │       │   - API Key Mgmt   │       │   - API Keys     │
└───────────────────┘       └─────────┬──────────┘       └──────────────────┘
                                      │
                                      │
                                      ▼
┌───────────────────┐       ┌────────────────────┐
│                   │       │                    │
│   Django REST     │◄──────┤      Redis         │
│   Framework API   │       │   - Task Queue     │
│                   │       │                    │
└───────────────────┘       └────────────────────┘
```

---

## 📖 API Documentation

### 🔹 Endpoints

#### **Video Management**
| Method | Endpoint       | Description                     |
|--------|----------------|---------------------------------|
| `GET`  | `/api/videos/` | List all videos with pagination |
| `GET`  | `/api/videos/{id}/` | Retrieve details of a specific video |

---

## 🛠 Local Setup

### 1️⃣ Prerequisites
- Install **Python 3.12+**
- Install **PostgreSQL**
- Install **Redis**
- Install **pip** and **virtualenv**

### 2️⃣ Clone the Repository
```sh
git clone <repository-url>
cd <repository-folder>
```

### 3️⃣ Create a Virtual Environment
```sh
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 4️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 5️⃣ Configure Environment Variables
Create a .env file in the project root with the following content:
```
# Django settings
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True

# Database
DB_NAME=youtube_videos
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# YouTube API Keys
YOUTUBE_API_KEYS=your-api-key-1,your-api-key-2
```

### 6️⃣ Apply Migrations
```sh
python manage.py migrate
```

### 7️⃣ Run the Development Server
```sh
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000`.

---

## 📡 API Usage Examples

### **1️⃣ Fetch Videos**
```sh
curl -X GET "http://127.0.0.1:8000/api/videos/"
```

---

## 🏗️ Workflow

1. **Periodic Fetching**: The Celery task `fetch_latest_videos` fetches the latest YouTube videos every 10 seconds.
2. **API Key Management**: The system rotates through available API keys when quota limits are reached.
3. **Data Storage**: Videos are stored in a PostgreSQL database with metadata like title, description, and published date.
4. **REST API**: The Django REST Framework provides endpoints for querying video data.

---

## 💻 Development

### Key Features

#### **API Key Management**
- API keys are stored in the database and managed via the Django admin interface.
- The system automatically deactivates keys when their quota is exceeded and switches to the next available key.

#### **Video Fetching**
- Videos are fetched using the YouTube Data API and stored in the database.
- The `fetch_videos_from_youtube` utility handles API requests, error handling, and retries.

#### **Background Tasks**
- Celery is used for background processing, such as fetching videos and managing API keys.
- Redis serves as the message broker for Celery.

---

## 📌 Design Choices & Assumptions

### Key Design Choices
- **Django REST Framework**: Provides a robust and flexible API layer.
- **PostgreSQL**: Chosen for its reliability and support for complex queries.
- **Celery + Redis**: Enables asynchronous task processing and scheduling.

### Assumptions
- The system is designed to handle moderate traffic (~10,000 videos/day).
- API keys are rotated to ensure uninterrupted operation.

---

## 📌 Cost Analysis

| Component       | Resource Specs | Free Tier Allowance | Cost |
|------------------|----------------|---------------------|------|
| Web Service      | 512MB RAM, 1 vCPU | 750 hours/month   | $0   |
| PostgreSQL       | 1GB storage       | 1 free instance    | $0   |
| Redis            | 30MB storage      | 1 free instance    | $0   |

---

## 📂 Project Structure
```
.
├── youtube_api/
│   ├── settings.py       # Django settings
│   ├── urls.py           # Project URLs
│   ├── wsgi.py           # WSGI entry point
│   ├── celery.py         # Celery configuration
│   └── __init__.py       # App initialization
├── videos/
│   ├── models.py         # Database models
│   ├── views.py          # API views
│   ├── serializers.py    # DRF serializers
│   ├── tasks.py          # Celery tasks
│   ├── utils.py          # Utility functions
│   ├── urls.py           # App URLs
│   └── admin.py          # Admin interface
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── .env                  # Environment variables
```

---

## ⚙️ Configuration Options

| Environment Variable | Description | Default |
|-----------------------|-------------|---------|
| `DJANGO_SECRET_KEY`   | Django secret key | `django-insecure-default-key` |
| `DEBUG`               | Debug mode | `False` |
| `DB_NAME`             | PostgreSQL database name | `youtube_videos` |
| `DB_USER`             | PostgreSQL username | `postgres` |
| `DB_PASSWORD`         | PostgreSQL password | `postgres` |
| `DB_HOST`             | PostgreSQL host | `localhost` |
| `DB_PORT`             | PostgreSQL port | `5432` |
| `REDIS_HOST`          | Redis host | `localhost` |
| `REDIS_PORT`          | Redis port | `6379` |
| `YOUTUBE_API_KEYS`    | Comma-separated YouTube API keys | `None` |

---

## 📌 Scaling Considerations
- **Database Indexing**: Indexes on frequently queried fields like `published_at` improve performance.
- **Horizontal Scaling**: Add more Celery workers to handle increased task loads.
- **Caching**: Use Redis for caching frequently accessed data.

---

## 🛠 Future Enhancements
- Add support for advanced search filters (e.g., by channel, date range).
- Implement user authentication for API access.
- Add monitoring and alerting for task failures and API key usage.

--- 

## 🏗️ Deployment
- Use Docker for containerization.