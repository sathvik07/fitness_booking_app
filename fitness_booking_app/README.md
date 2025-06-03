# Fitness Studio Booking API (Django)

This is a simple Django REST API for managing class bookings at a fictional fitness studio. Clients can view available classes (Yoga, Zumba, HIIT) and book a spot. Timezone-aware scheduling is supported.

---

## Features

- View available classes (`GET /classes`)
- Book a class (`POST /book`)
- View bookings by client email (`GET /bookings?email=...`)
- Prevent overbooking
- Timezone-aware date/time display (default: IST → converted via query param)
- Input validation & clean API design
- Sample seed data
- Unit tests included

---

## Tech Stack

- Python 3.8+
- Django 4.x
- Django REST Framework
- SQLite (in-memory or file-based)
- `pytz` for timezone handling

---

## Setup Instructions

1. **Clone the repository**:

```bash
git clone https://github.com/yourusername/fitness-booking-django.git
cd fitness-booking-django
```
2. **Create a virtual environment** (optional but recommended):

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```
3. **Install dependencies**:

```bash
pip install -r requirements.txt
```
4. **Run migrations**:

```bash
python manage.py migrate
```
5. **Seed the database with initial data** (optional):

```bash
python api/seed_data.py
```
6. **Run the development server**:

```bash
python manage.py runserver
```

