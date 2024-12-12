# BeerHub

A web application

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <project-directory>
   
2. **Install dependencies:**
    ```bash
   poetry install
   
3. **Apply migrations:**
    ```bash
   python manage.py makemigrations beers
   python manage.py migrate

4. **Run the development server:**
    ```bash
   python manage.py runserver
   
## Creating an Admin User

1. Run the following command:
   ```bash
   python manage.py createsuperuser
   
2. Enter the required details (username, email, and password).

3. Access the admin interface at:
   ```bash
   http://127.0.0.1:8000/admin-<obscurity_str_look_urls.py>/
   
## Loading Sample Data

To populate the database with sample beers for development or testing purposes, follow these steps:

1. Ensure the `BeerHub` app has a `fixtures` folder with the `beers.json` file:

2. Run the following command to load the data into the database:
   ```bash
    python manage.py loaddata beers.json
