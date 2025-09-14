from flask import request, Blueprint, jsonify
from app.services.contact_services import ContactServices
from app.schema.mycontact_schema import MyContactSchema
from app.utils.validator import FormValidator

contact_schema = MyContactSchema()
contacts_schema = MyContactSchema(many=True)

class ApiContactRoutes:
    def __init__(self):
        self.contact_api: Blueprint = Blueprint('contact_api', __name__)
        self.service = ContactServices()
        self.all_contact()
        self.contact_by_id()
        self.add_contact()
        self.edit_contact()
        self.delete_contact()

    def all_contact(self):
        @self.contact_api.route('/api/all-contact', methods=['GET'])
        def get_all_data():
            if request.method == "GET":
                datas = contacts_schema.dump(ContactServices().get_all_contact())
                response = {
                    'status': 200,
                    'messages': "OK",
                    'data': datas,
                    'error': None
                }
                return jsonify(response)
            else:
                response = {
                    'status': 405,
                    'messages': "Method Not Allowed",
                    'data': None,
                    'error': None
                }
                return jsonify(response)

    def contact_by_id(self):
        @self.contact_api.route("/api/contact/<int:id>", methods=["GET"])
        def get_data_by_id(id):
            if request.method == "GET":
                contact = contact_schema.dump(ContactServices().get_data_by_id(id=id))
                response = {
                    'status': 200,
                    'messages': "OK",
                    'data': contact,
                    'error': None
                }
                return jsonify(response)
            else:
                response = {
                    'status': 405,
                    'messages': "Method Not Allowed",
                    'data': None,
                    'error': None
                }
                return jsonify(response)
            
    def add_contact(self):
        @self.contact_api.route("/api/add-contact", methods=['POST'])
        def add_contact():
            if request.method == "POST":
                f_name = request.json.get('f_name', '').strip()
                l_name = request.json.get('l_name', '').strip()
                phone_number = request.json.get('phone_number', '').strip()
                email = request.json.get('email', '').strip()

                print(f_name, l_name, phone_number, email)

                error = FormValidator(f_name=f_name, l_name=l_name, phone_number=phone_number, email=email).validate_all()

                if error:
                    response = {
                    'status': 400,
                    'messages': "Bad Request",
                    'data': None,
                    'error': error
                    }
                    return jsonify(response), 400
                
                else:

                    is_created = ContactServices().create_contact(f_name=f_name, l_name=l_name, phone_number=phone_number, email=email)

                    if is_created:
                        response = {
                        'status': 201,
                        'messages': "Created",
                        'data': {
                            "id": is_created.id,
                            "f_name": is_created.f_name,
                            "l_name": is_created.l_name,
                            "phone_number": is_created.phone_number,
                            "email": is_created.email
                            },
                        'error': None
                        }
                        return jsonify(response), 201
                    
                    else:
                        response = {
                        'status': 400,
                        'messages': "Bad Request",
                        'data': None,
                        'error': is_created['error']
                        }
                        return jsonify(response), 400
                
            else:
                response = {
                    'status': 405,
                    'messages': "Method Not Allowed",
                    'data': None,
                    'error': None
                }
                return jsonify(response), 405
                
    def edit_contact(self):
        @self.contact_api.route("/api/edit-contact/<int:id>", methods=["PATCH"])
        def edit_contact(id):
            if request.method == "PATCH":

                user = ContactServices().get_data_by_id(id)

                f_name = request.json.get('f_name', '').strip()
                l_name = request.json.get('l_name', '').strip()
                phone_number = request.json.get('phone_number', '').strip()
                email = request.json.get('email', '').strip()

                is_edited = ContactServices().edit_contact(user=user, phone_number=phone_number, f_name=f_name, l_name=l_name, email=email)

                if is_edited:
                    response = {
                    'status': 200,
                    'messages': "OK",
                    'data': {
                        'id': user.id,
                        'phone_number': user.phone_number,
                        'f_name': user.f_name,
                        'l_name': user.l_name,
                        'email': user.email
                    },
                    'error': None
                    }
                    return jsonify(response), 200
                else:
                    response = {
                    'status': 400,
                    'messages': "bad Request",
                    'data': None,
                    'error': None
                    }
                    return jsonify(response), 400


            else:
                response = {
                    'status': 405,
                    'messages': "Method Not Allowed",
                    'data': None,
                    'error': None
                }
                return jsonify(response), 405

    def delete_contact(self):
        @self.contact_api.route("/api/delete-contact/<int:id>", methods=["DELETE"])
        def delete_contact(id):
            if request.method == "DELETE":
                user = ContactServices().get_data_by_id(id)

                is_deleted = ContactServices().remove_contact(user)

                if is_deleted:
                    response = {
                    'status': 200,
                    'messages': "OK",
                    'data': None,
                    'error': None
                    }
                    return jsonify(response), 200
                
                else:
                    response = {
                    'status': 400,
                    'messages': "Bad Request",
                    'data': None,
                    'error': None
                    }
                    return jsonify(response), 400

            else:
                response = {
                    'status': 405,
                    'messages': "Method Not Allowed",
                    'data': None,
                    'error': None
                }
                return jsonify(response), 405
