# 🎭 Theatre API

A RESTful Django-based API for managing theatre performances, users, and ticket bookings.


🚀 Features

1. **User registration and authentication**
2. **CRUD operations for:**
   1. Performances  
   2. Plays  
   3. Bookings  
3. **PostgreSQL database**
4. **Django REST Framework**
5. **OpenAPI 3 schema**  
   (Swagger + ReDoc via `drf-spectacular`)
6. **Admin panel**
7. **Django Debug Toolbar** (for development)


🛠️ Tech Stack

1. Python 3.9+
2. Django 4.2+
3. Django REST Framework
4. PostgreSQL
5. Docker + docker-compose (optional)
6. drf-spectacular (for API documentation)
 

Image of Database



🎭 Theatre API Endpoints
Resource	Endpoint	Description
Genres	/api/theatre/genres/	🎨 Manage play genres. Supports full CRUD operations.
Actors	/api/theatre/actors/	🎭 Manage theatre actors. Create, view, update, or delete actor profiles.
Theatre Halls	/api/theatre/theatre-halls/	🏛️ Manage theatre halls (name, capacity, and location).
Plays	/api/theatre/plays/	📚 Manage theatre plays. Add scripts, cast, and other metadata.
Performances	/api/theatre/performances/	📅 Schedule and manage specific play performances with date and time.
Reservations	/api/theatre/reservations/	🧾 Manage ticket reservations for upcoming performances.
Tickets	/api/theatre/tickets/	🎟️ Manage issued tickets, including assigned seats and pricing details.


🔧 All endpoints support standard RESTful operations where applicable:
GET – Retrieve data • POST – Create • PUT/PATCH – Update • DELETE – Remove


How to run this project

git clone https://github.com/igorchapy/REST_project1.git
cd bookstore-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver

