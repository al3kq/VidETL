import jwt

jwt_secret = "DEVJWTSECRET"

token_full = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NiwiaWF0IjoxNzA1NTQ1MzAzfQ.Q-nKnrK_AQ9fq5ZKt8InBHnkbZ2u79X1BQCeiNshyjc"

token = token_full.split(' ')[1]

decoded_token = jwt.decode(token, jwt_secret, algorithms=['HS256'])

print(decoded_token)