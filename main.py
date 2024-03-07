import base64
import json
import jwt
import os
import requests

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse

from google.oauth2 import service_account
import google.auth.transport.requests

# Path to your service account key file
SERVICE_ACCOUNT_FILE = 'gcp-connect-integration.json'

# Specify the scopes required for the Google Cloud Marketplace Procurement API
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']


app = FastAPI()

# From configuration
PROVIDER_ID = 'gcp-connect-integration'

# class Item(BaseModel):
#     data: str


@app.post("/webhook/")
async def receive_webhook(request: Request):
    request_json = await request.json()
    encoded_data = request_json['message']['data']
    data = json.loads(base64.b64decode(encoded_data).decode('utf-8'))
    request_json['message']['data'] = data
    print(f'Received webhook: {json.dumps(request_json, indent=4)}')
    # TODO: Hide decoded data from response
    return {"message": "Received successfully", "body": request_json}


@app.post("/signup/")
async def handle_signup(request: Request):
    # Attempt to extract the JWT from the x-gcp-marketplace-token header
    # jwt_token = request.headers.get("x-gcp-marketplace-token", "No JWT token provided")
    # print(f'Received x-gcp-marketplace-token: {token}')

    # For demonstration, print the JWT token to console
    # print(f"Received JWT token: {jwt_token}")

    # try:
    #     request_json = await request.json()
    #     print(f'Request json: {request_json}')
    # except Exception as e:
    #     print(e)
    #
    try:
        request_body = await request.body()
        print(f'Request body: {request_body}')
    except Exception as e:
        print(e)

    try:
        form_data = await request.form()
        token = form_data.get('x-gcp-marketplace-token')
        print(f'Received x-gcp-marketplace-token: {token}')
        decoded_jwt = jwt.decode(token, options={"verify_signature": False})
        print(f'Decoded token:', decoded_jwt)
        USER_ACCOUNT_ID = decoded_jwt["sub"]
        print(f'USER_ACCOUNT_ID: {USER_ACCOUNT_ID}')

        # Load the service account credentials from the key file
        # credentials = service_account.Credentials.from_service_account_file(
        #     SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        #
        # # Request a new token
        # request = google.auth.transport.requests.Request()
        # credentials.refresh(request)
        #
        # # Now you have the access token
        # access_token = credentials.token
        # Temporary get token from environment
        access_token = os.environ['SERVICE_ACCOUNT_TOKEN']
        print(f'access_token: {access_token}')

        url = f'https://cloudcommerceprocurement.googleapis.com/v1/providers/{PROVIDER_ID}/accounts/{USER_ACCOUNT_ID}:approve'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }
        body = {}
        response = requests.post(url, headers=headers, json=body)
        print(f'Account approval response: {response.json()}')

    except Exception as e:
        print(e)

    # Prepare a simple HTML response
    html_content = """
    <html>
        <head>
            <title>Sign Up Successful</title>
        </head>
        <body>
            <h1>Thank you for signing up!</h1>
            <p>Your account is now being set up.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


# @app.post("/signup.html")
# async def signup_html(request: Request):
#     # Extract the form data or raw body here, similar to your original /signup endpoint
#     form_data = await request.form()
#     token = form_data.get('x-gcp-marketplace-token')
#     print(f'Received x-gcp-marketplace-token: {token}')
#     # Process the token as needed...
#     return HTMLResponse(content="<h1>Thank you for signing up!</h1>", status_code=200)
