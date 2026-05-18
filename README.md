
# GoalSync — Enterprise Goal Tracking & Performance Management System

GoalSync is an AI-powered enterprise performance management platform built using Django.  
The platform enables organizations to manage employee goals, quarterly progress tracking, performance analytics, manager reviews, AI insights, and organizational dashboards in a production-ready environment.

---

# Live Deployment

🔗 Production URL:  
https://enterprise-goal-tracking-system-v2.onrender.com

---

# Features

## Authentication & Role-Based Access Control

- Custom Django User Model
- Employee Dashboard
- Manager Dashboard
- HR/Admin Dashboard
- Secure Login & Logout
- Role-Based Routing
- Session Management

---

## Goal Management System

- Goal Creation
- Goal Approval Workflow
- Goal Weightage Validation
- Goal Status Tracking
- Goal Completion Analytics
- Quarterly Goal Reviews

---

## Performance Analytics

- Employee KPI Tracking
- Manager Analytics Dashboard
- HR Analytics Dashboard
- Performance Leaderboards
- Goal Completion Percentage
- Organization-Level Analytics

---

## AI-Powered Features

- AI Employee Insights
- AI Copilot Assistant
- AI Performance Recommendations
- Risk Detection & Analytics
- Executive AI Dashboard
- Organization Performance Summaries

---

## Organizational Management

- Department Management
- Team Hierarchy
- Employee-Manager Structure
- Department-Level Analytics

---

## Reporting System

- PDF Report Generation
- Performance Export System
- Enterprise Reporting Architecture

---

## Production Deployment

- Render Cloud Deployment
- PostgreSQL Production Database
- Gunicorn WSGI Server
- WhiteNoise Static File Serving
- CSRF & Security Hardening
- Environment Variable Management

---

# Tech Stack

## Backend

- Django 5
- Python 3.11
- SQLite (Development)
- PostgreSQL (Production)

---

## Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Chart.js

---

## AI Integration

- Gemini AI
- Ollama (Local LLM Support)
- phi3:mini

---

## Deployment & DevOps

- Render
- Gunicorn
- WhiteNoise
- GitHub
- dotenv

---

# System Architecture


User
   ↓
Django Authentication System
   ↓
Role-Based Access Control
   ↓
Dashboard Layer
   ↓
Analytics Engine
   ↓
AI Insight Engine
   ↓
PostgreSQL Database


---

# Dashboards

## HR/Admin Dashboard

* Organization KPIs
* Employee Analytics
* Manager Analytics
* Goal Approval Metrics
* Performance Leaderboards
* Executive AI Insights

---

## Manager Dashboard

* Team Performance Tracking
* Goal Approval Workflow
* Team Analytics
* Quarterly Reviews
* Performance Monitoring

---

## Employee Dashboard

* Personal Goals
* Quarterly Progress
* Performance Metrics
* AI Recommendations
* Goal Completion Tracking

---

# Production Security Features

* CSRF Protection
* Secure Session Cookies
* Environment-Based Secrets
* Secure Static File Serving
* Production WSGI Configuration
* Role-Based Access Control

---

# Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/goal_tracking_portal.git

cd goal_tracking_portal
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

---

## Activate Environment

### Windows

```bash
.venv\\Scripts\\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Apply Migrations

```bash
python manage.py migrate
```

---

## Run Server

```bash
python manage.py runserver
```

---

# Production Deployment (Render)

## Build Command

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

---

## Start Command

```bash
gunicorn goal_tracking_portal.wsgi
```

---

# Environment Variables

```env
SECRET_KEY=your_secret_key

DEBUG=False

DATABASE_URL=your_postgresql_url

GEMINI_API_KEY=your_api_key
```

---

# Demo Credentials

## HR/Admin

```text
Username: hr_admin
Password: Admin@1234
```

---

## Manager

```text
Username: manager1
Password: Manager@1234
```

---

## Employee

```text
Username: employee1
Password: Employee@1234
```

---

# Future Enhancements

* Advanced AI Analytics
* Real-Time Notifications
* Dark Mode
* AI Chat Memory
* Mobile Responsiveness
* Advanced Charts & Forecasting
* Export to Excel/CSV
* Multi-Tenant Architecture
* Real-Time Collaboration

---

# Project Status

## Current Phase

Production Deployment & Enterprise Analytics Stabilization

---

# Author

Anugya Jain

---

# License

This project is built for educational, internship, and hackathon purposes.

```
```
