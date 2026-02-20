# flask-news-api-webapp
A Flask-based personalized news web application with user authentication, preference management, and real-time news fetching using NewsAPI.

# Project Flow:
1️⃣ User Authentication

Users can Sign Up with name, email, and password.

Passwords are securely stored using hashing (Werkzeug security).

Users can Log In using their credentials.

Session management ensures protected routes require authentication.

2️⃣ Preference Selection

Users can select multiple news categories (Technology, Business, Sports, AI, etc.).

Preferences are stored in a local data.json file.

Users can update their preferences anytime.

3️⃣ News Fetching

Based on the selected category:

The app dynamically builds a request URL.

Fetches real-time news articles using NewsAPI.

Only articles containing a description and image are displayed.

Users can:

Search categories from the navbar

View news based on saved preferences

Browse latest news

4️⃣ Additional Features

Profile view and edit functionality

Preference management

Contact form

Logout functionality with session clearing

Secure environment variable handling for API keys

🛠️ Tech Stack

Backend: Flask

Frontend: HTML, CSS (Jinja Templates)

Authentication: Werkzeug Security

API Integration: NewsAPI

Data Storage: JSON (local file system)

Session Management: Flask Sessions

🔐 Security Features

Password hashing

Environment variable storage for SECRET_KEY and API_KEY

Protected routes requiring login
