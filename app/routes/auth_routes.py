from flask import request, Blueprint, jsonify
from app.services.user_services import UserServices
from app.schema.user_schema import UserSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from app.models.mycontact import Users

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class AuthRoutes:
    def __init__(self):
        self.auth = Blueprint('auth', __name__)
        self.service = UserServices()
        self.create_user()
        self.login_user()
        self.profile_user()
        self.change_password_user()

    def create_user(self):
        @self.auth.route('/register', methods=['POST'])
        def register():
            if request.method == "POST":
                username = request.json.get('username', '').strip()
                password = request.json.get('password', '').strip()

                is_created = self.service.register(username=username, password=password)

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
                    'status': 405,
                    'messages': "Method Not Allowed",
                    'data': None,
                    'error': "Method Not Allowed"
                }
                return jsonify(response), 405
            
    def login_user(self):
        @self.auth.route('/login', methods=["POST"])
        def login():
            if request.method == "POST":
                username = request.json.get('username', '').strip()
                password = request.json.get('password', '').strip()

                is_logged_in = self.service.login(username=username, password=password
                )

                if is_logged_in:

                    access_token: create_access_token = create_access_token(
                        identity=str(is_logged_in.id),
                        expires_delta=timedelta(hours=1)
                    )

                    response = {
                    'status': 200,
                    'messages': "Login succesful",
                    'data': {
                        "id": is_logged_in.id,
                        "username": is_logged_in.username,
                        "jwt_token": access_token,
                        "expires_in": 3600
                        },
                    'error': None
                    }
                    
                    return jsonify(response), 200
            else:
                response = {
                    'status': 405,
                    'messages': "Method Not Allowed",
                    'data': None,
                    'error': "Method Not Allowed"
                }
                return jsonify(response), 405
            
    def profile_user(self):
        @self.auth.route("/profile", methods=["GET"])
        @jwt_required()
        def profile():
            user_id = int(get_jwt_identity())
            user = Users.query.get(user_id)

            if not user:
                return jsonify({
                    'status': 404,
                    'messages': 'User not found',
                    'data': None,
                    'error': 'Not Found'
                }), 404
            
            return jsonify({
                "status": 200,
                "messages": "Profile fetched",
                "data": {
                    "id": user.id,
                    "username": user.username
                },
                "error": None
            }), 200

    def change_password_user(self):
        @self.auth.route("/profile/change-password", methods=["PATCH"])
        @jwt_required()
        def change_password():
            if request.method == "PATCH":
                user_id = int(get_jwt_identity())
                user = Users.query.get_or_404(user_id)

                new_password = request.json.get("new_password", '').strip()

                if not user:
                    return jsonify({
                        'status': 404,
                        'messages': 'User not found',
                        'data': None,
                        'error': 'Not Found'
                    }), 404
                
                result = self.service.change_password(user=user, new_password=new_password)
                

                if isinstance(result, Users):
                    response = {
                    'status': 200,
                    'messages': "Password changed!",
                    'data': {
                        "username": result.username
                    },
                    'error': None
                    }
                    return jsonify(response), 200

                else :
                    response = {
                    'status': 400,
                    'messages': "Failed to change password!",
                    'data': {
                        "username": result.username
                    },
                    'error': result.get("error")
                    }
                    return jsonify(response), 400
                

                
            else:
                response = {
                    'status': 405,
                    'messages': "Method Not Allowed",
                    'data': None,
                    'error': "Method Not Allowed"
                }
                return jsonify(response), 405

