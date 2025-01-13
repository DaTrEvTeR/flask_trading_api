# 2xx
STRATEGY_CREATED_RESPONSE = {"message": "Strategy created successfully"}, 201
STRATEGY_UPDATED_RESPONSE = {"message": "Strategy updated successfully"}, 200
STRATEGY_DELETED_RESPONSE = {"message": "Strategy deleted successfully"}, 200
REGISTERED_SUCCESSFULLY_RESPONSE = {"message": "User registered successfully"}, 201


def acces_token_response(access_token):
    return {"access_token": access_token}, 200


# 4xx
INVALID_INPUT_RESPONSE = {"error": "Invalid input"}, 400
USER_ALREADY_EXISTS_RESPONSE = {"error": "User already exists"}, 400
INVALID_CREDENTIALS_RESPONSE = {"error": "Invalid credentials"}, 401
FORBIDDEN_RESPONSE = {"error": "Forbidden"}, 403
STRATEGY_NOT_FOUND_RESPONSE = {"error": "Strategy not found"}, 404
