# StudyBud - Django MVT

StudyBud is a web application built using Django's Model-View-Template (MVT) architecture. It allows users to create, join, and participate in study rooms where they can discuss topics, share knowledge, and collaborate.

## Prerequisites
Before setting up the project, ensure you have the following installed:
- Python (>= 3.8)
- pip (Python package manager)

## Installation and Setup

1. **Clone the Repository**
   ```sh
   git clone https://github.com/zhalgas-seidazym/studybud-django-mvt.git
   cd studybud-django-mvt
   ```

2. **Create a Virtual Environment**
   ```sh
   python -m venv venv
   source venv/scr/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Django and Django REST Framework**
   ```sh
   pip install django djangorestframework
   ```

4. **Make Migrations and Apply Migrations**
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a Superuser**
   ```sh
   python manage.py createsuperuser
   ```

6. **Run the Development Server**
   ```sh
   python manage.py runserver
   ```
   The application will be available at `http://127.0.0.1:8000/`

## License
This project is licensed under the MIT License.

