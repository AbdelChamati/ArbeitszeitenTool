# Arbeitszeiten Tool

A modern desktop work-hours tracking application built with Python and CustomTkinter.

## Features

- Secure authentication (bcrypt)
- Work shift tracking
- Monthly filtering
- Income calculation
- PDF export
- Excel export
- Email reporting
- Light/Dark mode auto-save
- Data visualization (matplotlib)

## Tech Stack

- Python 3.10+
- CustomTkinter
- SQLite
- Bcrypt
- ReportLab
- OpenPyXL
- Matplotlib

## Installation

1. Clone repository

git clone https://github.com/YOUR_USERNAME/ArbeitszeitenTool.git
cd ArbeitszeitenTool

2. Create virtual environment

python -m venv venv
venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Run application

python app.py

## Build .exe

pip install pyinstaller
pyinstaller --onefile --windowed app.py

Executable will be in:

dist/

## Versioning

Current Version: v1.0.0

## Architecture

This project follows a modular src-based structure:

- UI Layer (CustomTkinter)
- Business Logic (utils/)
- Authentication (bcrypt)
- Data Layer (SQLite)
- Reporting (PDF / Excel)
- Visualization (Matplotlib)

The architecture separates UI, logic, and persistence to ensure scalability.

## Screenshots

### Login

![Login](assets/screenshots/login.png)

### Dashboard

![Dashboard](assets/screenshots/dashboard.png)
