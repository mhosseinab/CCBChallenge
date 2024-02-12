from json import dumps as json_dumps
from flask import Blueprint, make_response, request, jsonify
from jsonschema import validate, ValidationError, Draft7Validator

from storage.file_storage import FileStorage
from utils.schema import load_schema
from utils.api_decorators import ApiDecorators

api = Blueprint("challenge_api", __name__)

# Load the schema once when the module is imported
VEHICLE_FEATURES_SCHEMA = load_schema("vehicle-features.v1.schema.json")


@api.route("/challenge", methods=["POST"])
@ApiDecorators.require_customer_id
def vehicle_features_post(user_id: str):
    """
    Save the request data to a file.
    """

    data = request.get_json()

    try:
        # Validate the data against the schema
        validate(instance=data, schema=VEHICLE_FEATURES_SCHEMA, cls=Draft7Validator)
    except ValidationError as e:
        # If the data is not valid, return a 400 response with the validation error message
        return jsonify({"error": str(e)}), 400

    # Save the data to a file
    store = FileStorage()
    folder_name = user_id
    for vehicle in data.get("vehicles", []):
        file_name = f"{vehicle.get('id')}.json"
        if not store.save_file(folder_name, file_name, json_dumps(data, indent=2).encode()):
            return make_response("Failed to save data", 500)
    return make_response("OK", 200)
