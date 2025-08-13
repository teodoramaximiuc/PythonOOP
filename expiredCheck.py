import jwt
import time

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZW8iLCJleHAiOjE3NTUwODE5NjF9.589BoYTs1yShnLem4Dl_9OZpmIf56Y_DiHdpQ_Sgomw"
SECRET_KEY = "0fa3a137d8b9256f900e88f6dd83e1d6c8274ece0d7cd3a2e27c08150d8fa880"

try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    print("Token is valid. Expires at:", payload["exp"])
except jwt.ExpiredSignatureError:
    print("Token is expired.")