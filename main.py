from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
app = FastAPI()
from Logistic_Regression_Model import LogisticRegressionModel
from Math_Functions import MathFunctions
import numpy as np
import oracledb
from jose import jwt
from datetime import datetime, timedelta
import os

conn = oracledb.connect(
    user="C##teo",
    password="parola123",
    dsn="localhost:1521/xe"
)
cur = conn.cursor()
items = []
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is not set!")
ALGORITHM = "HS256"

class Token(BaseModel):
    access_token: str
    token_type: str

class Item(BaseModel):
    item: str

class User(BaseModel):
    name: str
    password: str

from fastapi import Header, Depends

def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token header")
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    return payload["sub"]

def is_number(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def hash_password(password: str):
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str):
    return hash_password(plain_password) == hashed_password

def save_action(current_user: str, action: str):
    cur.execute("SELECT NVL(MAX(id), 0) + 1 FROM cliusers_audit")
    new_id = cur.fetchone()[0]
    cur.execute("SELECT id FROM cliusers WHERE username = :username", {"username": current_user})
    userid = cur.fetchone()[0]
    if not userid:
        raise HTTPException(status_code=404, detail="User not found")
    cur.execute("INSERT INTO cliusers_audit (id, userid, action, action_time) VALUES (:id, :userid, :action, SYSDATE)",
                {"id": new_id, "userid": userid, "action": action})
    conn.commit()

@app.get("/n-th_fibonacci/{n}")
async def nth_fibonacci(n: int, current_user: str = Depends(get_current_user)):
    save_action(current_user, "n-th_fibonacci")
    return {"n-th_fibonacci": MathFunctions().nth_fibbonaci(n)}

@app.get("/pow/base={base}&exponent={exponent}")
async def pow(base: float, exponent: float, current_user: str = Depends(get_current_user)):
    save_action(current_user, "pow")
    return {"pow": MathFunctions().pow(base, exponent)}
@app.get("/factorial/{n}")
async def factorial(n: int, current_user: str = Depends(get_current_user)):
    save_action(current_user, "factorial")
    result = MathFunctions().factorial(n)
    if result is None:
        raise HTTPException(status_code=400, detail="Factorial of negative number is not defined")
    return {"factorial": result}
@app.post("/login")
async def login(user: User):
    cur.execute("SELECT * FROM cliusers WHERE username = :username",
               {"username": user.name}
    )
    row = cur.fetchone()
    if row:
        print("DB password:", row[2])
        print("Input password:", user.password)
        print("Input hashed:", hash_password(user.password))
        if verify_password(user.password, row[2]):
            expire = datetime.utcnow() + timedelta(minutes=30)
            token = jwt.encode({"sub": user.name, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
            return Token(access_token=token, token_type="bearer")
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")
@app.post("/signup")
async def signup(user: User):
    cur.execute("SELECT * FROM cliusers WHERE username = :username", {"username": user.name})
    if cur.fetchone():
        return {"message": "Username already exists, please choose another one"}
    user.password = hash_password(user.password)
    cur.execute("SELECT NVL(MAX(id), 0) + 1 FROM cliusers")
    new_id = cur.fetchone()[0]
    cur.execute(
        "INSERT INTO cliusers (id, username, password) VALUES (:id, :username, :password)",
        {"id": new_id, "username": user.name, "password": user.password}
    )
    conn.commit()
    return {"message": "User created successfully, you can now login"}
@app.post("/logout")
async def logout():
    return {"message": "Logout successful. Please delete the token on the client side."}
@app.get("/file/{file_name}")
async def read_file(file_name: str, current_user: str = Depends(get_current_user)):
    try:
        save_action(current_user, "read_file")
        with open(file_name, 'r') as file:
            content = file.read()

        lines = content.splitlines()
        X = []
        y = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) != 2:
                continue
            try:
                x_val = float(parts[0])
                y_val = int(parts[1])
                X.append([x_val])
                y.append(y_val)
            except ValueError:
                continue
        X = np.array(X).reshape(-1, 1)
        y = np.array(y)
        if X.size == 0 or y.size == 0:
            raise HTTPException(status_code=400, detail="No valid numeric data found in the file.")
        model = LogisticRegressionModel(learning_rate=0.05, epochs= 10000, threshold=0.5)
        weights, bias = model.train(X, y)
        predictions = model.predict([[1.5], [2.0], [2.6], [3.5]])
        return {
            "username": current_user,
            "predictions": predictions.tolist(),
            "weights": weights.tolist(),
            "bias": bias
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")