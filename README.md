## CleanBuy

---

### Deploying on local

---

***Step 1:***

Create a virtual environment.

###### *Linux / macOS:*

    python3 -m venv venv
    source venv/bin/activate

###### *Windows:*

    python -m venv venv
    source venv/Scripts/activate

***Step 2:***

Create a **.env** file in the project directory and fill it with your data:
    
    DB_HOST                    - ip address of your database
    DB_PORT                    - port of database
    DB_USER                    - user name (owner) of database
    DB_PASS                    - password for access to database
    DB_NAME                    - database name

***Step 3:***

    pip install -r requirements.txt

***Step 4:***

    uvicorn src.main:app --reload

---

### Alembic Migrations

---

    alembic init -t async migrations
    alembic revision --autogenerate -m "Initiial"
    alembic upgrade head

---

### Deploying via Docker

---

    docker build . --tag cleanbuy
    docker run -p 80:80 cleanbuy

---

### Author

---

_Designed by Alexey Klimovich, 2024_
