## CleanBuy
___
### Deploying on local
___
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
    
    DB_HOST                     - ip address of your database (e.g. localhost)
    DB_PORT                     - port of database (e.g. 5432)
    DB_USER                     - user name (owner) of database (e.g. postgres)
    DB_PASS                     - password for access to database (e.g. 1234)
    DB_NAME                     - database name (e.g. cleanbuy)
    SECRET_KEY                  - for auth (for JWT tokens)
    ALGORITHM                   - hash algorithm for auth (e.g. HS256)
    ACCESS_TOKEN_EXPIRE_MINUTES - (e.g. 30)

To get a string for *SECRET_KEY* run:
    
    openssl rand -hex 32

***Step 3:***

    pip install -r requirements.txt

***Step 4:***

    uvicorn src.main:app --reload
---
### Alembic Migrations
___
    alembic init -t async migrations
    alembic revision --autogenerate -m "Initiial"
    alembic upgrade head
---
### Testing
___
***PyTest*** is used for testing.
The following values need to be defined:

    DB_HOST_TEST         - DB_HOST analog
    DB_PORT_TEST         - DB_PORT analog 
    DB_NAME_TEST         - DB_NAME analog
    DB_USER_TEST         - DB_USSR analog
    DB_PASS_TEST         - DB_PASS analog

Then run the following command (to run the tests):

    pytest -v -s tests/unut/

where **-v** -- for **PASSED**&**FAILED** instead of **"."**&**"!"**

To view code coverage by tests, you can use the following commands:

    pytest --cov-report html:cov_html --cov=src tests/unit/           # generate a report in web format
or 

    pytest --cov-report term --cov=src tests/unit/                    # generate a report in the console
---
### Deploying via Docker
___

###### Image creating

    docker build . --tag cleanbuy
    docker run -p 80:80 cleanbuy

###### Docker-compose
    
    docker-compose up --build

---
### Author
___

Designed by _Alexey Klimovich_, 2024
