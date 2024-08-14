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
### Switch on HTTPS
___

***Step 1. Installing Chocolatey***
- Open cmd.exe as Administrator
- Run the following command:

      @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"

- Check if Chocolatey is installed by the following command:

      choco
    
  You must see:

      Chocolatey v2.3.0
      Please run 'choco -?' or 'choco <command> -?' for help menu.

***Step 2. Installing mkcert***
- Run the following command:

      choco install mkcert

***Step 3. Run mkcert***
- Run the following command:

      mkcert -intall

      Created a new local CA 💥
      The local CA is now installed in the system trust store! ⚡️
      The local CA is now installed in Java's trust store! ☕️

- And run the last command:

      mkcert localhost 127.0.0.1

      Created a new certificate valid for the following names 📜
       - "localhost"
       - "127.0.0.1"

      The certificate is at "./localhost+1.pem" and the key at "./localhost+1-key.pem" ✅

      It will expire on 14 November 2026 🗓

- At the result we have two files: _localhost+1.pem_ and _localhost+1-key.pem_. \
I will rename these files on _cert.pem_ and _key.pem_ accordingly and move them to *_security* folder.

- Now we can use *HTTPS* running our app:

      uvicorn src.main:app --loop asyncio --host 0.0.0.0 --port 443 --ssl-keyfile=certs/key.pem --ssl-certfile=certs/cert.pem

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
