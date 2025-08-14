# Shortify


*A modern and responsive web app for smart URL shortening with analytics.*

🔗 **Live Demo:** [Visit Shortify](https://shortify-hhe2.onrender.com/)

---

## ✨ Features

- 🔗 Shorten long URLs instantly
- 👤 User accounts with link history and analytics
- 📊 Track click count, creation date
- 🛠 Guest mode for quick, no-login link shortening
- 📱 Mobile-friendly and responsive design


---

## 🚀 How to Use

1. Open Shortify and paste your long URL into the input box.
2. Click **Shorten**.
3. Copy your short link using the one-click button.
4. (If logged in) View analytics for each shortened link.

---

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS (Bootstrap), JavaScript
- **Backend:** Django (Python)
- **Database:** SQLite (Development) 
- **Other:** Django Authentication

```bash
## ⚙️ Setup Instructions

# Clone the repository
git clone https://github.com/yourusername/shortify.git
cd shortify

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run the development server
python manage.py runserver
