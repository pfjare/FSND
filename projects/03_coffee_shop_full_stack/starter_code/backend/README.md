# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:drinks-detail`
   - `post:drinks`
   - `patch:drinks`
   - `delete:drinks`
6. Create new roles for:
   - Barista
     - can `get:drinks-detail`
   - Manager
     - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com). - Register 2 users - assign the Barista role to one and Manager role to the other. - Sign into each account and make note of the JWT. - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json` - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs). - Run the collection and correct any errors. - Export the collection overwriting the one we've included so that we have your proper JWTs during review!
   https://classudacity.auth0.com/authorize?audience=coffee&response_type=token&client_id=0p05fRWKlFcByjn0Jx2G1qmj0ioiglgI&redirect_uri=https://127.0.0.1:8080/
   pfjare@gmail.com Grapes20
   eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikg4UlMtbXlmM0lyaTFWM3k3QjRiWiJ9.eyJpc3MiOiJodHRwczovL2NsYXNzdWRhY2l0eS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViMDdmOTIxY2MxYWMwYzE0ODRlZDczIiwiYXVkIjoiY29mZmVlIiwiaWF0IjoxNTg4OTY3OTE0LCJleHAiOjE1ODg5NzUxMTQsImF6cCI6IjBwMDVmUldLbEZjQnlqbjBKeDJHMXFtajBpb2lnbGdJIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJwYXRjaDpkcmlua3MiLCJwb3N0OmRyaW5rcyJdfQ.TzE3ssr9i-q96ychhfStkA5HIl0aME5WIzAZfdeFrwOyDrAtT9G5IK1crru-1Z6F4olroV9gRMHv4_VTuKCDO57n6XMNeHNr6BaxtQstmbxmu7uvOyVFvDXCHNhITUb4j6W01sOeilReF3vF0-a8889GllQfMKpspomkaIdD5w13kZF3hzXztegk1UrPQ1g2vv8wyTaSU9xvNAL5Bh9wBSZdOEXzXuJ1CBPpf5BanZvo7nm7EmHGdW9dRQGqj3_PDyEtwn5iS389ZujVdKxWAdv6lLpaEX24yktOGFoZTsh7o3uUfxkVG4Ib5FiNhj7ZKUGl2ezb1qQh94A_9Yc3jg
   p.fjare@yahoo.com
   eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikg4UlMtbXlmM0lyaTFWM3k3QjRiWiJ9.eyJpc3MiOiJodHRwczovL2NsYXNzdWRhY2l0eS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViNWJhOGM2YjY5YmMwYzEyMDQ2Y2QxIiwiYXVkIjoiY29mZmVlIiwiaWF0IjoxNTg4OTY4MDg0LCJleHAiOjE1ODg5NzUyODQsImF6cCI6IjBwMDVmUldLbEZjQnlqbjBKeDJHMXFtajBpb2lnbGdJIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6W119.vtDYcKKZKd6vI2LaoPD45yVHVuC9xWZU6jKS3DVPIvSRKTP268_0dVuhwfvrwk-0jHwtDE_4U6pidC5BauX6G4AkKfzaLDzL_atUe9bJO3sTaCq408uiBWJ_XmIFZxHtFKuAAUe-Z_qCWVTnAb6rvKpuWD5NrPJ-TtsfxAryi04MCC9Is79w7dRtzajWnCRLMIHnLZWj0LAjyjltNExgo2lvOYEaigoxmx724PaFKj8aoJ1_VFbeaOd-ICLhafDIyatTp2mkZDJ7rn53xnOb_dAw0FZ4ESPXI40AU3TB9f8BgmQmCMjtuBnZaiQkOSOQ9RaOV3WAwIPcFgYWy6ugIQ

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`
