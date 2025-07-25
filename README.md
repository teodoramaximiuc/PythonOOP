# Math Microservice (FastAPI + Oracle + JWT)

This project implements a production-ready microservice for solving basic mathematical operations via a REST API. It includes secure user authentication, logging to a database, and is container-ready for deployment. The client side was done using the click python library (Command Line Interface).

---

## Features

- Exposes API endpoints for:
  - Power (`/pow/base=...&exponent=...`) 
  - N-th Fibonacci number (`/n-th_fibonacci/{n}`) 
  - Factorial (`/factorial/{n}`)
  - Logistic Regression (`/file/{file.name}`)
- JWT-based user authentication (`/signup`, `/login`, `/logout`), for each user a token is saved for authorization
- Logs all requests to an Oracle database (`cliusers_audit`) with request id, user id, action and timestamp
- Passwords are hashed with SHA-256 for increased security
---

## API Endpoints

### `GET /pow/base={base}&exponent={exponent}`

**Description:**  
Computes the result of `base` raised to the power of `exponent`.

**Parameters:**
- `base` (float) — the base number
- `exponent` (float) — the exponent

**Example:**
GET /pow/base=2&exponent=5
Response: { "pow": 32.0 }


### `GET /n-th_fibonacci/{n}`

**Description:**  
Returns the `n`-th Fibonacci number (0-based index).

**Parameters:**
- `n` (integer) — the position in the Fibonacci sequence

**Example:**
GET /n-th_fibonacci/7
Response: { "n-th_fibonacci": 13 }

### `GET /factorial/{n}`

**Description:**  
Calculates the factorial of `n`.

**Parameters:**
- `n` (integer) — the number to compute the factorial for

**Example:**
GET /factorial/5
Response: { "factorial": 120 }

**Note:** Returns HTTP 400 for negative values.

### `GET /file/{file_name}`

**Description:**  
Loads training data from a file, trains a logistic regression model, and returns prediction results.

**Parameters:**
- `file_name` (string) — name of the file (must exist on server or be mounted into container)

**Expected file format:**
A plain text file where each line contains a space-separated feature-label pair, e.g.:

1.0 0
2.0 0
3.0 1
4.0 1

**Returns:**
- Predictions for `[1.5], [2.0], [2.6], [3.5]`
- Trained model weights and bias
- Username of the caller (extracted from token)

**Example:**
GET /file/train.txt
Response:
{
"username": "teo",
"predictions": [0, 0, 1, 1],
"weights": [4.69],
"bias": -10.77
}