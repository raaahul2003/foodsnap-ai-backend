# 🍽️ FoodSnap AI — Backend (Django REST Framework)

> AI-powered food calorie and nutrient estimation system — Backend & Admin Portal

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-4.x-green?style=for-the-badge&logo=django)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange?style=for-the-badge&logo=tensorflow)
![MySQL](https://img.shields.io/badge/MySQL-8.0-blue?style=for-the-badge&logo=mysql)
![IJSRD](https://img.shields.io/badge/Published-IJSRD_Vol.14_Issue_2_2026-red?style=for-the-badge)

---

## 📖 About

**FoodSnap AI** is a complete dietary monitoring system that allows users to photograph a meal and instantly receive food identification, calorie estimation, and personalized nutritional insights. This repository contains the **Django REST Framework backend** and **Bootstrap-based Admin Web Portal**.

The AI model (AA-MobileNetV2) achieves **93.2% Top-1 accuracy** across 151 food categories including Indian and Kerala-specific cuisines, with a **162ms on-device inference time**.

📄 **Research Paper**: Published in IJSRD — International Journal for Scientific Research & Development, Vol. 14, Issue 2, 2026
> *"FoodSnap AI: An Attention-Augmented MobileNetV2 Framework for Real-Time Food Recognition, Nutritional Estimation, and Personalized Dietary Recommendations on Mobile Devices"*

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  PRESENTATION LAYER                      │
│         Flutter Mobile App  |  Bootstrap Admin Portal    │
└───────────────────┬─────────────────────────────────────┘
                    │ HTTPS / REST API
┌───────────────────▼─────────────────────────────────────┐
│                  APPLICATION LAYER                       │
│     Django REST Framework  |  TFLite Inference Engine    │
│     JWT Auth  |  Recommendation Engine  |  OCR Module   │
└───────────────────┬─────────────────────────────────────┘
                    │ ORM / CRUD
┌───────────────────▼─────────────────────────────────────┐
│                    DATA LAYER                            │
│          MySQL 8.0 — Users, Food Logs, Nutrition DB      │
└─────────────────────────────────────────────────────────┘
```

---

## ✨ Features

### 🤖 AI Module
- **AA-MobileNetV2** — Attention-Augmented MobileNetV2 with Squeeze-and-Excitation blocks
- Trained on **153,000 images** across **151 food categories**
- Includes the **first annotated Kerala Cuisine Dataset** (10 dishes, 2,000 images)
- **OCR (Tesseract 5.0)** for packaged food label scanning (~87% accuracy)
- TensorFlow Lite export for on-device mobile inference

### 🖥️ Admin Web Portal
- Secure admin login with session management
- View and manage registered users
- Handle user feedback and complaints with reply system
- Food database management
- Generate analytical reports and system statistics
- Change password functionality

### 🔌 REST API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/myapp/register/` | POST | User registration |
| `/myapp/login/` | POST | JWT authentication |
| `/myapp/predict/` | POST | Food image prediction |
| `/myapp/foodlog/` | GET/POST | Daily food logging |
| `/myapp/nutrient/` | GET | Nutritional data lookup |
| `/myapp/recommend/` | GET | Personalized meal recommendations |
| `/myapp/userviewhishealth/` | POST | Health profile management |
| `/myapp/find_daily_intake/` | GET | Weekly nutrition summary |
| `/myapp/ocrscan/` | POST | Ingredient label OCR scan |

### ⚡ API Performance
| Operation | Response Time |
|-----------|--------------|
| Authentication | ~85 ms |
| Food Prediction | ~980 ms |
| Nutritional Lookup | ~42 ms |
| Log Operations | ~55 ms |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10+ |
| Framework | Django 4.x + Django REST Framework |
| AI Training | TensorFlow 2.x / Keras |
| On-Device AI | TensorFlow Lite |
| OCR | Tesseract 5.0 (pytesseract) |
| Database | MySQL 8.0 |
| Admin UI | Bootstrap 5 + HTML/CSS/JS |
| Server | Gunicorn + Nginx |
| Testing | pytest (47 unit tests) |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- MySQL 8.0
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/foodsnap-ai-backend.git
cd foodsnap-ai-backend

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env with your MySQL credentials and secret key

# 5. Run database migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create superuser for admin portal
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver
```

### Environment Variables (`.env`)
```env
SECRET_KEY=your_django_secret_key
DEBUG=True
DB_NAME=foodsnap_db
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

---

## 🧠 AI Model — AA-MobileNetV2

### Model Performance

| Metric | Value |
|--------|-------|
| Top-1 Accuracy | **93.2%** |
| Top-5 Accuracy | **98.7%** |
| F1-Score (Macro) | **0.928** |
| Model Size | **11.4 MB** |
| Inference Time (on-device) | **162 ms** |

### Comparison with Baselines

| Model | Top-1 | F1 | Size | Mobile |
|-------|-------|----|------|--------|
| ResNet-50 | 87.4% | 0.868 | 102.8 MB | ❌ |
| EfficientNet-B0 | 89.8% | 0.891 | 21.2 MB | ⚠️ |
| MobileNetV2 | 90.9% | 0.903 | 9.8 MB | ✅ |
| **AA-MobileNetV2 (Ours)** | **93.2%** | **0.928** | **11.4 MB** | ✅ |

### Dataset
- **Food-101**: 101,000 images, 101 classes
- **IndianFoodNet**: 50,000 images, 50+ regional categories
- **Kerala Cuisine Dataset** *(Novel)*: 2,000 images — Puttu, Appam, Kerala Fish Curry, Sadya, Karimeen Pollichathu, Avial, Payasam, Beef Fry, Parotta, Kallappam

---

## 📁 Project Structure

```
web_project/
├── myapp/
│   ├── models.py          # Database models
│   ├── views.py           # API views & business logic
│   ├── urls.py            # URL routing
│   ├── admin.py           # Admin configurations
│   ├── foodalgo/          # Food recognition AI module
│   └── foodalgo 2/        # OCR & recommendation module
├── templates/             # Admin portal HTML templates
├── static/                # CSS, JS, images
├── media/                 # Uploaded food images
├── web_project/
│   ├── settings.py
│   └── urls.py
├── manage.py
└── requirements.txt
```

---

## 👥 Team — Group 9, MGM Technological Campus

| Name | Roll No | Role |
|------|---------|------|
| Arun Raj M R | CCV22CS005 | UI/UX Web Design |
| Rahil Abdul Razakh | CCV22CS037 | AI Model Integration |
| Rahul Raj C P | CCV22CS038 | UI/UX App Design |
| Suhaib V P | CCV22CS045 | Backend Development |

**Guide**: Ms. Ramsheena P, Asst. Professor, Dept. of CSE
**Institution**: MGM Technological Campus, Valanchery, Kerala
**Course**: B.Tech CSE — Semester 8 (2026)

---

## 🔗 Related Repository

📱 **Flutter Mobile App**: [foodsnap-ai-flutter](https://github.com/raaahul2003/foodsnap-ai-flutter)

---

## 📜 License

This project is submitted as a final year academic project at MGM Technological Campus under APJ Abdul Kalam Technological University, Kerala.

---

*Published in IJSRD — Vol. 14, Issue 2, 2026 | Department of CSE, MGM Technological Campus, Valanchery, Kerala, India*
