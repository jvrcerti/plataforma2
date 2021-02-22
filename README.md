**GENERAL**

Repository for Django RESTful API in order tu populate the intermediate database. This database will serve as the primary data source for the microgrid management platform;

---

## Technologies

* Python 3.6+
* Docker & Docker Compose
* Travis CI
* Django
* Django REST Framework
* TDD
* Postgres

---

## Test Strategy

* General automate tests by Travis CI
* Python code linter flake8 for check the code base against coding style (PEP8), programming errors (like “library imported but unused” and “Undefined name”) and to check cyclomatic complexity
* Unit tests will be written in tests.py
* `docker-compose run app sh -c "python manage.py test"`


## Test Case Scenarios
* Test to verify registration with invalid password.
* Test to verify registration with already exists username.
* Test to verify registration with valid datas.
* Tested API authentication endpoint validations.
* Tested authenticated user authorization.
* Create a todo with API.
* Update a todo with API.
* Update a todo with API.
* Delete a todo with API.
* Get todo list for a user.

## API Endpoints

**Users**

* /api/users/ (User registration endpoint)
* /api/users/login/ (User login endpoint)
* /api/users/logout/ (User logout endpoint)

**Todos**

* /api/todos/ (Todo create and list endpoint)
* /api/todos/{todo-id}/ (Todo retrieve, update and destroy endpoint)