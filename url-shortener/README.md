# 🔗 URL Shortener API

A simple REST API to shorten URLs, built with **Flask** and **SQLite**.

## Features

- ✅ Shorten any URL
- ✅ Custom alias support
- ✅ Auto-redirect to original URL
- ✅ Click tracking & stats
- ✅ Duplicate URL detection

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/url-shortener.git
cd url-shortener
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python run.py
```

API is now running at `http://localhost:5000`

---

## API Endpoints

### `GET /`
Returns available endpoints.

---

### `POST /shorten`
Shorten a URL.

**Request body:**
```json
{
  "url": "https://www.google.com",
  "alias": "google"  // optional custom alias
}
```

**Response:**
```json
{
  "message": "URL shortened successfully",
  "data": {
    "short_code": "google",
    "short_url": "http://localhost:5000/google",
    "original_url": "https://www.google.com",
    "clicks": 0,
    "created_at": "2024-01-01T00:00:00"
  }
}
```

---

### `GET /<short_code>`
Redirects to the original URL and increments click count.

---

### `GET /stats/<short_code>`
Get stats for a shortened URL.

**Response:**
```json
{
  "data": {
    "short_code": "google",
    "original_url": "https://www.google.com",
    "clicks": 42,
    "created_at": "2024-01-01T00:00:00"
  }
}
```

---

### `GET /all`
Get all shortened URLs.

---

### `DELETE /<short_code>`
Delete a shortened URL.

---

## Tech Stack

- **Python** - Programming language
- **Flask** - Web framework
- **SQLAlchemy** - ORM for database
- **SQLite** - Database

## License

MIT
