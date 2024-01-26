import jwt
print(jwt.__file__)

jwt_secret = "DEVJWTSECRET"

token_full = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6OCwiaWF0IjoxNzA1OTcyNjU3fQ.92JfI0o_2u1h6wuJ62Dtt6sS-IJF9ruoeM2Vy4i3ehs"

token = token_full.split(' ')[1]

decoded_token = jwt.decode(token, jwt_secret, algorithms=['HS256'])

print(decoded_token)