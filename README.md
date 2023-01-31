# elevator-simulation-django

**An elevator system, which can be initialised with N elevators and maintains the elevator states as well.**

# Setup

- Run `python -m venv venv`
- Run `venv\scripts\activate`
- Run `pip install -r requirements.txt`
- Change your directory to the `src` file
- Create a .env file in `src` folder using the `sample.env` file
- Run `python manage.py migrate --run-syncdb`
- Run `python manage.py runserver`
- Done.

## API-Contracts

- The API contracts are here as follows [here](https://github.com/ivinayakg/lift-simulation-django/blob/main/contracts/contracts.md)

## APIs Provided

- Initialise the elevator system to create ‘n’ elevators in the system
- Fetch all requests for a given elevator
- Fetch the next destination floor(or latest elevator requests) for a given elevator
- Fetch elevator data or a particular key of the elevator
- Saves user request to the list of requests for a elevator
- update elevator data (gates, direction, floor)

## Tests

- All APIs are covered with tests(+ edge cases)
- To run tests Run `python manage.py test` or `python manage.py test elevator`
