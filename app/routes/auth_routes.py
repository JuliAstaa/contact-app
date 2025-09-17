from flask import request, Blueprint, jsonify
from app.services.user_services import UserServices
from app.schema.user_schema import UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class AuthRoutes:
    def __init__(self):
        self.auth = Blueprint('auth', __name__)
        self.service = UserServices()
        self.create_user()
        self.login_user()

    def create_user(self):
        @self.auth.route('/register', methods=['POST'])
        def register():
            if request.method == "POST":
                username = request.json.get('username', '').strip()
                password = request.json.get('password', '').strip()

                is_created = self.service.register(username=username, password=password)


                print(is_created)

                if is_created:
                    response = {
                    'status': 201,
                    'messages': "Created",
                    'data': {
                        "id": is_created.id,
                        "username": is_created.username,
                        "password": is_created.password,
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
            
    def login_user(self):
        @self.auth.route('/login', methods=["POST"])
        def login():
            if request.method == "POST":
                username = request.json.get('username', '').strip()
                password = request.json.get('password', '').strip()

                is_logged_in = self.service.login(username=username, password=password
                )

                if is_logged_in:
                    response = {
                    'status': 201,
                    'messages': "Created",
                    'data': {
                        "id": is_logged_in.id,
                        "username": is_logged_in.username,
                        "password": is_logged_in.password,
                        },
                    'error': None
                    }
                    return jsonify(response), 201
            else:
                response = {
                    'status': 400,
                    'messages': "Bad Request",
                    'data': None,
                    'error': is_logged_in['error']
                    }
                return jsonify(response), 400