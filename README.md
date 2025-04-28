Action Suggester API
A Django-based API that analyzes text messages and suggests relevant actions based on tone and intent.
Setup Instructions

Prerequisites
Python 3.8+
PostgreSQL



Clone the repository:
git clone https://github.com/yourusername/action-suggester-api.git
cd action-suggester-api

Create and activate a virtual environment:
python -m venv venv

venv\scripts\activate  

Install dependencies:
pip install -r requirements.txt

Set up environment variables:
Create a .env file in the project root with the following variables:
SECRET_KEY=your_django_secret_key
DEBUG=True
DB_NAME=action_suggester
DB_USER=postgres
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
OPEN_API_KEY=open_api_key

Run migrations:
python manage.py migrate

Create a superuser (optional):
python manage.py createsuperuser

Run the development server:
python manage.py runserver


API Endpoints
POST /api/analyze/
Analyzes a text message and suggests relevant actions.
Request Format:
json{
  "query": "I want to order pizza"
}
Response Format:
json{
  "query": "I want to order pizza",
  "analysis": {
    "tone": "Hungry",
    "intent": "Order Food"
  },
  "suggested_actions": [
    {
      "action_code": "ORDER_FOOD",
      "display_text": "Order food online"
    },
    {
      "action_code": "FIND_NEARBY_RESTAURANT",
      "display_text": "Find nearby restaurants"
    },
    {
      "action_code": "FIND_RECIPE",
      "display_text": "Find recipes"
    }
  ]
}
Testing with Postman

Open Postman
Create a new POST request to http://localhost:8000/api/analyze/
In the "Body" tab, select "raw" and "JSON"
Enter a sample request:
json{
  "query": "I want to order pizza"
}

Click "Send" to test the endpoint
