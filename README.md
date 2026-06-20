# 🔗 URL Shortener API

A simple REST API to shorten URLs, built with **Flask** and **SQLite**.

🌐 **Live Demo:** https://web-production-46279.up.railway.app

## Features

- ✅ Shorten any URL
- ✅ Custom alias support
- ✅ Auto-redirect to original URL
- ✅ Click tracking & stats
- ✅ Duplicate URL detection
- ✅ QR Code generator

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/aokway/url-shortener.git
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

Base URL: `https://web-production-46279.up.railway.app`

### `GET /`
Returns available endpoints.

---

### `POST /shorten`
Shorten a URL.

**Request body:**
```json
{
  "url": "https://www.google.com",
  "alias": "google"
}
```

**Response:**
```json
{
  "message": "URL shortened successfully",
  "data": {
    "short_code": "google",
    "short_url": "https://web-production-46279.up.railway.app/google",
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

---

### `GET /qr/<short_code>`
Generate a QR Code image for the shortened URL.

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
- **Railway** - Deployment platform

## License

MIT