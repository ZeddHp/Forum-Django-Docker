# MyForum Project

## Introduction
This project is built using Django and serves as a forum application.

## Clone the Repository
To get started, follow these steps to clone the repository to your local machine.
Create a folder where you want this repo on you local machine and navigate there using cmd.

```bash
git clone https://github.com/ZeddHp/Forum-Django-Docker.git
cd myforum
```

## Setup Instructions
Follow these steps to set up the project on your local machine:

1. **Activate Virtual Environment (Optional):**
   If you prefer to work within a virtual environment, create and activate it using `venv` or `virtualenv`.

2. **Install Dependencies:**
   Install project dependencies using `pip` and the provided `requirements.txt` file.

   ```bash
   pip install -r requirements.txt
   ```

3. **Database Migrations:**
   Run database migrations to create the necessary tables in the database.

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Start the Development Server:**
   Start the Django development server to run the project locally.

   ```bash
   python manage.py runserver
   ```

5. **Access the Application:**
   Once the server is running, you can access the application in your web browser at `http://localhost:8000`.
