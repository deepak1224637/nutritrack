# 🥗 NutriTrack Pro — AI Nutrition Tracker

A full-featured Django web app for tracking nutrition with AI-powered food image analysis.

## ✨ Features
- **Signup / Login / Logout** — full authentication
- **User Profile** — name, age, height, weight, work type, gym schedule, address, goals
- **AI Food Scan** — upload/take photo → Claude AI auto-detects calories, protein, fat, carbs
- **Manual Meal Entry** — log breakfast, lunch, dinner, snacks with custom macros
- **Water & Milk Tracking** — log drinks with one click, visual progress bar
- **Dashboard** — daily calorie summary, macro charts, weekly trends
- **Weight Log** — daily weight with BMI calculator
- **Meal History** — full log of all meals with nutritional breakdown

---

## 🚀 Setup & Run

### 1. Install Python (3.10+ required)
Download from: https://www.python.org/downloads/

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create admin user (optional)
```bash
python manage.py createsuperuser
```

### 5. Set your Anthropic API Key (for AI food scanning)
Get your free key from: https://console.anthropic.com

**Windows:**
```cmd
set ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

**Mac/Linux:**
```bash
export ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

##2nd Gemini API keys 

### 6. Run the server
```bash
python manage.py runserver
```

### 7. Open in browser
```
http://127.0.0.1:8000
```

---

## 📁 Project Structure
```
nutritrack/
├── accounts/          # Auth: signup, login, user profile
│   ├── models.py      # UserProfile model
│   ├── views.py       # Auth views
│   ├── forms.py       # Django forms
│   └── urls.py
├── tracker/           # Core: meals, water, weight
│   ├── models.py      # MealLog, WaterLog, WeightLog
│   ├── views.py       # Dashboard, log meal, AI analysis
│   └── urls.py
├── templates/
│   ├── base.html      # Base layout with nav
│   ├── accounts/      # Login, signup, profile templates
│   └── tracker/       # Dashboard, log meal, history
├── media/             # Uploaded food images
├── requirements.txt
└── manage.py
```

---

## 🌐 Deploy to Production

### Option 1: Railway (Easiest — Free tier available)
1. Push code to GitHub
2. Go to railway.app → New Project → Deploy from GitHub
3. Add environment variable: `ANTHROPIC_API_KEY`
4. Done! Live URL in minutes.

### Option 2: Render
1. Push to GitHub
2. render.com → New Web Service
3. Build command: `pip install -r requirements.txt && python manage.py migrate`
4. Start command: `gunicorn nutritrack.wsgi`
5. Add `ANTHROPIC_API_KEY` in environment variables

### Option 3: VPS (DigitalOcean/AWS)
```bash
pip install gunicorn whitenoise
gunicorn nutritrack.wsgi --bind 0.0.0.0:8000
```

---

## 🔑 Admin Panel
Visit: `http://127.0.0.1:8000/admin/`
Login with superuser credentials to manage all users and data.

---

## 💰 API Key Cost
- New Anthropic accounts get **$5 free credits**
- Each food image analysis costs ~$0.001-0.003
- $5 = **thousands of food scans**
- Get key: https://console.anthropic.com
