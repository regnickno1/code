Here’s a clear, runnable example showing the main token types used in authentication and authorization, along with explanations and sample formats.
We’ll cover:

Access Token
Refresh Token
ID Token (OIDC)
API Key
JWT (JSON Web Token)


1. Access Token

Purpose: Grants access to protected resources (short-lived).
Format: Often opaque (random string) or JWT.
Example:

ya29.a0AfH6SMBEXAMPLE1234567890abcdef


Usage (HTTP request):

HttpGET /user/profile HTTP/1.1
Host: api.example.com
Authorization: Bearer ya29.a0AfH6SMBEXAMPLE1234567890abcdef


2. Refresh Token

Purpose: Used to obtain a new access token without re-authenticating.
Format: Opaque string, long-lived, stored securely.
Example:

1//0gEXAMPLEREFRESHTOKENabc123xyz


Usage (token refresh request):

HttpPOST /oauth2/token
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token&
refresh_token=1//0gEXAMPLEREFRESHTOKENabc123xyz&
client_id=CLIENT_ID&
client_secret=CLIENT_SECRET


3. ID Token (OIDC)

Purpose: Contains user identity claims (JWT format).
Example (JWT structure):

eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.
eyJsubIjoiMTIzNDU2Nzg5MCIsIm5hbWUiOiJKb2huIERvZSIsImVtYWlsIjoiam9obkBleGFtcGxlLmNvbSJ9.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c


Decoded Payload:

Json{
  "sub": "1234567890",
  "name": "John Doe",
  "email": "john@example.com"
}


4. API Key

Purpose: Simple static token for identifying the calling application.
Example:

AIzaSyD-EXAMPLEKEY1234567890abcdef


Usage:

HttpGET /maps/api/geocode/json?address=Hanoi&key=AIzaSyD-EXAMPLEKEY1234567890abcdef


5. JWT (JSON Web Token)

Purpose: Self-contained token with claims, signed for integrity.
Structure: header.payload.signature (Base64URL encoded).
Example:

Pythonimport jwt
import datetime

# Secret key for signing
SECRET_KEY = "mysecret"

# Create JWT
payload = {
    "user_id": 123,
    "role": "admin",
    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
}
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
print("JWT:", token)

# Decode JWT
try:
    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    print("Decoded:", decoded)
except jwt.ExpiredSignatureError:
    print("Token expired")
except jwt.InvalidTokenError:
    print("Invalid token")


✅ Security Notes:

Never expose refresh tokens or API keys in public code.
Store tokens securely (encrypted at rest, HTTPS in transit).
Use short lifetimes for access tokens and rotate keys regularly.


If you want, I can also make a full runnable Node.js or Python demo showing all token types in action with a mock API.
Do you want me to prepare that?
