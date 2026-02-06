# 💰 Personal Expense Manager (API)

Backend project developed with **Python, FastAPI, SQLAlchemy, and MySQL/PostgreSQL** for managing, analyzing, and visualizing personal expenses.

This project goes beyond a traditional CRUD: it includes **advanced SQL queries**, **automatic textual insights**, and **charts generated directly from the API**, making it ideal as a portfolio project.

---

## 🚀 Main Features

* ✅ Category CRUD
* ✅ Expense CRUD
* ✅ Filtered queries (by date, category, amount)
* ✅ Aggregated SQL reports
* ✅ Automatic insights in natural language
* ✅ Expense charts (matplotlib)
* ✅ Bulk fake data generation for testing

---

## 🧠 Automatic Insights Examples

The API can generate dynamic conclusions such as:

* 📈 Highest spending month
* 📉 Lowest spending month
* 🔥 Most impactful category
* 🏠 Percentage of expenses spent on rent
* 📊 Overall spending trend

All insights are calculated dynamically from the data stored in the database.

---

## 📊 Available Charts

The API can generate charts directly as PNG images:

* Monthly expense evolution
* Easily extensible to category breakdowns, comparisons, etc.

Example endpoint:

```http
GET /charts/monthly-expenses
```

---

## 🏗️ Project Architecture

```
app/
 ├── database/
 │   ├── connection.py
 │   └── models.py
 │   
 ├── routers/
 │   ├── insights.py
 │   └── charts.py
 ├── routers/
 │   ├── categories.py
 │   ├── expenses.py
 │   └── reports.py
 ├── schemas/
 │   ├── categories.py
 │   ├── expenses.py
 │   ├── insights.py
 │   └── reports.py
 ├── services/
 │   └── insights_service.py
 └── main.py

scripts/
 └── generate_expenses.py
```

---

## 🛠️ Tech Stack

* **Python 3.10+**
* **FastAPI**
* **SQLAlchemy ORM**
* **SQLite / PostgreSQL / MySQL** (compatible)
* **Matplotlib**
* **Pydantic**

---

## 🗄️ Database Setup (PostgreSQL)

This project was tested with PostgreSQL. Follow these steps to create the database:

### 1️⃣ Install PostgreSQL

* **Linux (Ubuntu):**

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

* **Mac (Homebrew):**

```bash
brew install postgresql
brew services start postgresql
```

* **Windows:**
  Download the installer from [PostgreSQL official site](https://www.postgresql.org/download/windows/).

### 2️⃣ Create a database and user

```sql
-- Login to PostgreSQL
psql -U postgres

-- Create database
CREATE DATABASE expense_manager;

-- Create user (replace 'password' with a secure password)
CREATE USER expense_user WITH PASSWORD 'password';

-- Give privileges
GRANT ALL PRIVILEGES ON DATABASE expense_manager TO expense_user;

-- Exit
\q
```

### 3️⃣ Configure connection

Edit `app/database/connection.py` file with your **secure password**:

```python
DATABASE_URL = "postgresql+psycopg2://expense_user:password@localhost/expense_manager"
```

### 4️⃣ Create tables (if using SQLAlchemy `Base.metadata.create_all`)

```python
from app.database.connection import engine
from app.database.base import Base

Base.metadata.create_all(bind=engine)
```

Your PostgreSQL database is now ready.

---

## ▶️ Installation & Running

### 1️⃣ Clone the repository

```bash

```

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the application

```bash
uvicorn app.main:app --reload
```

Access the interactive API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Populate the database with test data

The project includes a script to generate realistic random expenses:

```
python -m scripts.generate_expenses   
```

This will automatically insert hundreds of records for testing and analysis.

---

## 🎯 Project Goal

This project demonstrates skills in:

* Professional backend development
* REST API design
* Advanced SQL and aggregations
* Business logic
* Data analysis
* Visualization

---

## 🔮 Possible Future Improvements

* Frontend dashboard (React + Chart.js)
* Report export (CSV / PDF)
* Automatic spending alerts
* User authentication
* Cloud deployment

---
