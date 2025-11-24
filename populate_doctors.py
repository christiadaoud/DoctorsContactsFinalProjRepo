import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contacts_project.settings')
django.setup()

from contactlist.models import Doctor

doctors_data = [
    {"name": "Dr. Alice Smith", "specialty": "Surgeon", "city": "New York", "hospital": "NY General", "fee": 1800, "rating": 4.5, "latitude": 40.7128, "longitude": -74.0060},
    {"name": "Dr. Bob Johnson", "specialty": "Cardiologist", "city": "Los Angeles", "hospital": "LA Medical", "fee": 2000, "rating": 4.7, "latitude": 34.0522, "longitude": -118.2437},
    {"name": "Dr. Clara Lee", "specialty": "Dermatologist", "city": "Chicago", "hospital": "Chicago Health", "fee": 1500, "rating": 4.2, "latitude": 41.8781, "longitude": -87.6298},
]

for doc in doctors_data:
    Doctor.objects.update_or_create(name=doc["name"], defaults=doc)

print("Doctors added successfully!")

