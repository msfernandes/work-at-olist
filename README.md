[![Build Status](https://travis-ci.org/msfernandes/work-at-olist.svg?branch=master)](https://travis-ci.org/msfernandes/work-at-olist)
[![Coverage Status](https://coveralls.io/repos/github/msfernandes/work-at-olist/badge.svg?branch=master)](https://coveralls.io/github/msfernandes/work-at-olist?branch=master)

# Work at Olist

This project was developed as a test for a Python Developer job application at
[Olist](https://olist.com/) and consist in an HTTP REST API responsible for
register phone call records and generate monthly bills.

#### [You can find the API running here](https://olist-call-api.herokuapp.com/)

## Development

0. If you don't have `pipenv` installed on you workstation:
```
pip install --user pipenv
```

1. Install project dependencies. If you don't have a python 3.6 installed
on your workstation, you can pass the specific version that you have as parameter:
```
pipenv install
# or
pipenv install --python /path/to/python3
```

2. Run migrations:
```
pipenv run src/manage.py migrate
```

3. Run development server:
```
pipenv run src/manage.py runserver  # Running on http://localhost:8000
```

*Optional -* By default the project will run using SQLite. If you want to use
PostgreSQL or other database, you can create a configuration file (must be in
`src/call_api/settings.ini`) and specify the new database connection.

```
[settings]
ENGINE = postgresql_psycopg2
NAME = dbname
USER = dbuser
PASSWORD = dbpassword
HOST = dbhost
PORT = 5432
```

*Optional -* If you want to use django admin, to update call charges values:
```
pipenv run src/manage.py createsuperuser
```

#### Testing

All project test was made using the default Django test tools and the code
coverage was defined by `coverage` library. To run the tests and see the coverage:
```
pipenv run coverage run src/manage.py test src/
pipenv run coverage report
```

## Implementation Details

### Work Environment

| Computer                         | OS           | IDE            | Python |
|----------------------------------|--------------|----------------|--------|
| MacBook Air, i5, 4GB, 128GB SSD  | MacOS Mojave | Sublime Text 3 | 3.6    |
| DELL Desktop, i7, 8GB, 256GB SSD | Fedora 28    | Sublime Text 3 | 3.6    |

### Libraries

The main libraries used was:

* Django 2.2.2
* django-rest-framework 3.9.4
* drf-yasg 1.16.0 (For API documentation)

But I used some libraries to auxiliate the development:

* python-decouple 3.1 - Decouple allows you to change settings values using a
configuration file (`settings.ini`) or using environment variables.
* django-constance 2.4.0 - Constance allows you to create settings variables
that will be stored on database and are updated through admin. On this project
the call charges can be updated using constance.
* mock 3.0.5 - Used to write tests that need to mock method, classes, etc.

### Continuous Delivery

To implement a Continuous Delivery on this project I configured [Travis](https://travis-ci.org/msfernandes/work-at-olist)
that run all tests and `flake8` (python linter) after every commit on repository.
It's important to say that Travis was setted to run tests on 4 different environments:
python 3.6, python 3.6-dev, python 3.7 and python3.7-dev.

If Travis run successfully it will trigger an automated build on Heroku
and update [Coveralls](https://coveralls.io/github/msfernandes/work-at-olist) index.

The Travis criteria to a successfull build is:

* All test must pass
* Code coverage must be 100%
* `flake8` linter should found 0 errors