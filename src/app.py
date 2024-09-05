"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

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
    # return jsonify({
    #     "message": "Welcome to the Jackson Family API!",
    #     "endpoints": {
    #         "GET /members": "Get all family members",
    #         "GET /member/<int:member_id>": "Retrieve a single family member by ID",
    #         "POST /member": "Add a new family member",
    #         "DELETE /member/<int:member_id>": "Delete a family member by ID"
    #     }
    # }), 200

# 1) Obtene,os todos los miembros de la familia
@app.route('/members', methods=['GET'])
#def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    # members = jackson_family.get_all_members()
    # response_body = {
    #     "hello": "world",
    #     "family": members
    # }


    # return jsonify(response_body), 200
def get_all_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as e:
        return jsonify({"msg": "An error occurred while fetching members."}), 500

# 2) Obtenemos un miembro específico por su id member_id
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member:
            return jsonify(member), 200
        else:
            return jsonify({"msg": "Member not found"}), 404
    except Exception as e:
        return jsonify({"msg": "An error occurred while fetching the member."}), 500

# 3) Agregaremos un nuevo miembro a la familia
@app.route('/member', methods=['POST'])
def add_member():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"msg": "No input data provided"}), 400


        new_member = {  #diccionario de nuevo miembro
            "first_name": data.get("first_name"),
            "age": data.get("age"),
            "lucky_numbers": data.get("lucky_numbers")
        }


        if "id" in data:
            new_member["id"] = data["id"]

        added_member = jackson_family.add_member(new_member)
        return jsonify(added_member), 200
    except ValueError as ve:
        return jsonify({"msg": str(ve)}), 400
    except Exception as e:
        return jsonify({"msg": "An error occurred while adding the member."}), 500

# 4) Eliminar miembro
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        result = jackson_family.delete_member(member_id)
        if result["done"]:
            return jsonify(result), 200
        else:
            return jsonify({"msg": "Member not found"}), 404
    except Exception as e:
        return jsonify({"msg": "An error occurred while deleting the member."}), 500



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
