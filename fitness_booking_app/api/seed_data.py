import os
import sys
import django
import pytz
from datetime import datetime, timedelta

# Add the project root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_booking_app.settings')
django.setup()

from api.models import FitnessClass

# Clear existing data
FitnessClass.objects.all().delete()

IST = pytz.timezone('Asia/Kolkata')
now = datetime.now(IST)

classes = [
    {"name": "Yoga", "instructor": "Aarti", "offset_hours": 24},
    {"name": "Zumba", "instructor": "Raj", "offset_hours": 48},
    {"name": "HIIT", "instructor": "Meera", "offset_hours": 72},
]

for cls in classes:
    dt = now + timedelta(hours=cls["offset_hours"])
    FitnessClass.objects.create(
        name=cls["name"],
        instructor=cls["instructor"],
        date_time=dt.astimezone(pytz.UTC),  # Save in UTC
        available_slots=10
    )

print("✅ Seed data created successfully.")