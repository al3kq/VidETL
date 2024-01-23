import jwt
print(jwt.__file__)

jwt_secret = "DEVJWTSECRET"

token_full = "Bearer ..-"

token = token_full.split(' ')[1]

decoded_token = jwt.decode(token, jwt_secret, algorithms=['HS256'])

print(decoded_token)