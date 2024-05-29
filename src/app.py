"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def members():
    try:
        # this is how you can use the Family datastructure by calling its methods
        members = jackson_family.get_all_members()

        return jsonify(members), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route("/member/<int:member_id>", methods=["GET"])
def member_id(member_id):
    try:

        member = jackson_family.get_member(member_id)

        if member is None:
            return jsonify({"msg": "Member not found"}), 404

        return jsonify(member
                       ), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route("/member", methods=["POST"])
def member_add():
    try:
        member = request.get_json(force=True)
        response = jackson_family.add_member(member)

        return jsonify({"msg": f"Member {member['first_name']} added to family {jackson_family.last_name}", }
                       ), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route("/member/<int:member_id>", methods=["DELETE"])
def member_delete(member_id):
    try:

        response = jackson_family.delete_member(member_id)

        if response:
            return jsonify({"msg": f"Member with id {member_id} deleted", 
                            "done": True}
                           ), 200
        else:
            return jsonify({"msg": f"Member with id {member_id} doesn't exist", 
                            "done": False }
                           ), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 400


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)