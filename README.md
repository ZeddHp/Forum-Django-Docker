# MyForum Project

## Introduction
This project is built using Django and serves as a forum application.

## Clone the Repository
To get started, follow these steps to clone the repository to your local machine.
Create a folder where you want this repo on your local machine and navigate there using cmd.

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

5. **Build and Run the Docker Container:**
   To run project with docker you need to build container and then run it.

   ```bash
   docker build --tag python-django .
   docker run --publish 8000:8000 python-django
   ```
   If container is already built then you can just run:
   ```bash
   docker-compose up
   ```

![image](https://github.com/ZeddHp/Forum-Django-Docker/assets/68005483/31f40827-f4ea-411a-ba5e-86cb84ca82e6)
![image](https://github.com/ZeddHp/Forum-Django-Docker/assets/68005483/d7e2b580-542f-4d93-bee7-91ccc34c8505)
![image](https://github.com/ZeddHp/Forum-Django-Docker/assets/68005483/78711393-c32a-4c9d-88cd-08bab184459d)
![image](https://github.com/ZeddHp/Forum-Django-Docker/assets/68005483/c043d2c8-c332-4561-9e12-24cbe64b3f89)
![image](https://github.com/ZeddHp/Forum-Django-Docker/assets/68005483/717f3cca-2927-4db9-a612-d375e25d69cb)



