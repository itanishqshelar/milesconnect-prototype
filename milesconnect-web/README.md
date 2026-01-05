# MilesConnect Prototype

A modern Fleet Management System prototype featuring real-time tracking, predictive analytics, and dynamic fleet operations management.

## 🚀 Features

### Core Modules
- **Dashboard**: Real-time overview of fleet status, active shipments, and critical alerts.
- **Shipments**: Comprehensive delivery management with status tracking.
- **Drivers**: Driver onboarding, profiles, and performance monitoring.
- **Vehicles**: Fleet tracking, maintenance scheduling, and asset management.
- **Trip Sheets**: Digital trip management and financial tracking (revenue/expenses).

### 🧠 AI & Machine Learning (`ml-service`)
Powered by a dedicated Python/FastAPI service providing real-time intelligence:
- **Delay Prediction**: XGBoost model to predict shipment delays based on traffic, weather, and route data.
- **Incident Risk Assessment**: Predictive risk scoring for trips to proactively mitigate accidents.
- **Fuel Anomaly Detection**: Isolation Forest model to identify potential fuel theft or leaks.
- **Driver Clustering**: K-Means clustering to segment drivers by behavior (e.g., Eco-Friendly, Aggressive).
- **ETA Prediction**: High-precision arrival time estimation taking into account complex road factors.
- **Driver Scoring**: Automated performance rating (0-100) based on safety, efficiency, and reliability.
- **Demand Forecasting**: Predictive analytics for route demand planning.
- **Maintenance Prediction**: Early warning system for vehicle breakdowns.

### 🔔 Smart Notification System
- **Real-time Alerts**: Dynamic system-wide notifications.
- **Actionable**: Mark as read, dismiss, or bulk clear notifications.
- **Context-Aware**: Alerts for delivery completions, maintenance due, and risk warnings.

## 🛠️ Technology Stack

- **Frontend**: Next.js 15 (App Router), TypeScript, Tailwind CSS, Lucide Icons.
- **Backend Service**: Node.js, Express, Prisma ORM (SQLite/PostgreSQL).
- **ML Service**: Python 3.10+, FastAPI, XGBoost, Scikit-learn, Pandas.
- **State Management**: React Context (Logistics, Notification), TanStack Query.

## 📦 Installation & Setup

### Prerequisites
- Node.js (v18+)
- Python (v3.10+)
- npm or yarn

### 1. Backend Setup
```bash
cd backend
npm install
npx prisma generate
npx prisma db push  # or migrate dev
npm run build
npm start
```
*Runs on port 3001*

### 2. ML Service Setup
```bash
cd ml-service
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
# source venv/bin/activate

pip install -r requirements.txt
cd src/api
uvicorn app:app --reload --port 8000
```
*Runs on port 8000*

### 3. Frontend Setup
```bash
# Root directory
npm install
npm run dev
```
*Runs on port 3000*

## 🧪 Verification
To verify the system build and integrity:
1. **Backend**: `cd backend && npm run build`
2. **Frontend**: `npm run build`
3. **ML Service**: Check health at `http://localhost:8000/health`

## 🤝 Contribution
1. Fork the repo.
2. Create a feature branch.
3. Commit changes.
4. Push to branch & PR.

---
© 2024 MilesConnect
