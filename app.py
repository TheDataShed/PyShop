from datetime import datetime
import json
from flask import (
    Flask,
    jsonify,
    request
)


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# Data to serve with our API
PEOPLE = {
    "Farrell": {
        "fname": "Doug",
        "lname": "Farrell",
        "timestamp": get_timestamp()
    },
    "Brockman": {
        "fname": "Kent",
        "lname": "Brockman",
        "timestamp": get_timestamp()
    },
    "Easter": {
        "fname": "Bunny",
        "lname": "Easter",
        "timestamp": get_timestamp()
    }
}

# Create the application instance
app = Flask(__name__, template_folder="templates")

# Create a URL route in our application for "/"
@app.route('/api/people')
def get_people():
    """
    This function responds to a GET request for /api/people
    with the complete list of people

    :return:
        sorted list of people and 200
    """
    return jsonify([PEOPLE[key] for key in sorted(PEOPLE.keys())]), 200


@app.route('/api/people/<lname>')
def get_person(lname):
    """
    This function responds to a GET request for /api/people/<lname>
    with the person with lname

    :return:
        person object (dict) and 200
        error object (dict) and 404
    """
    if lname in PEOPLE:
        return jsonify(PEOPLE[lname]), 200
    else:
        error = {
            "message": "That person does not exist"
        }
        return jsonify(error), 404


@app.route('/api/people', methods=['POST'])
def post_person():
    """
    This function creates a new person in the PEOPLE dict

    :return:
        person object (dict) and 201
        error object (dict) and 409
    """
    data = request.json
    if not data.get("lname") in PEOPLE:
        PEOPLE[data.get("lname")] = data
        return jsonify(data), 201
    else:
        error = {
            "message": "That person already exists"
        }
        return jsonify(error), 409


@app.route('/api/people/<lname>', methods=['DELETE'])
def delete_person(lname):
    """
    This function deletes a person in the PEOPLE dict

    :return:
        204
        error object (dict) and 404
    """
    if lname in PEOPLE:
        del PEOPLE[lname]
        return 204
    else:
        error = {
            "message": "That person does not exist"
        }
        return jsonify(error), 404


@app.route('/api/people/<lname>', methods=['PUT'])
def put_person(lname):
    """
    This function updates a person in the PEOPLE dict

    :return:
        person object (dict) and 201
        error object (dict) and 404
    """
    if lname in PEOPLE:
        PEOPLE[lname] = request.json
        return jsonify(request.json),  201
    else:
        error = {
            "message": "That person does not exist"
        }
        return jsonify(error), 404


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
