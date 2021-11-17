# workout-plan-server
Python restful server of WorkoutPlan project.

It is a Flask application and use SQLAlchemy as ORM.

[![codecov](https://codecov.io/gh/vitorsm/workout-plan-server/branch/main/graph/badge.svg)](https://codecov.io/gh/vitorsm/workout-plan-server)

## Requirements

This directory must exist, and the user that will execute the workout-plan-server should have permission to write it:
* /var/log/workout-plan

In your development environment you can execute these commands:
```
sudo mkdir /var/log/myhome-server
sudo chmod 777 /var/log/myhome-server
```

## Tests

The tests are in the directory:
``` 
tests/
```

The tests are separated in two groups: unit tests and integration tests.
The purpose of integration tests is to test the controller and database integration.

To execute all tests run the command:

```
python3 -m unittest discover -s tests/
```

#### Coverage

To measure the test coverage you can use the coverage tool (https://coverage.readthedocs.io/).
To install run the following command:

```
pip3 install coverage
```

Then, execute the analysis:

```
coverage run --branch --source=workout_plan_server -m unittest discover -s tests/
```

The analysis will generate a file that contains the coverage data. To print the coverage data run the following command:
```
coverage report -m
```


## Security

The Flask-JWT lib was used to guarantee that all endpoints will be accessed only for authorized users.
According to the Flask documentation, the route decorator must be used as outermost.
To guarantee right behavior to access endpoint, the second decorator must be jwt_required from Flask-JWT.

The sequence of decorators in the controller layer must be route and jwt_required:
```
@exercise_controller.route("/", methods=["POST"])
@jwt_required()
def create_exercise(exercise_service: ExerciseService):
    exercise = ExerciseMapper.to_entity(request.json)
    exercise = exercise_service.create(exercise)
    return jsonify(ExerciseMapper.to_dto(exercise)), 200
```

## Layers and directories organization
