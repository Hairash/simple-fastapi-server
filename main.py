import base64
import json
import jwt

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse

app = FastAPI()


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


@app.post("/signup")
async def handle_signup(token: str = Form(...)):
    # Attempt to extract the JWT from the x-gcp-marketplace-token header
    # jwt_token = request.headers.get("x-gcp-marketplace-token", "No JWT token provided")
    print(f'Received x-gcp-marketplace-token: {token}')

    # For demonstration, print the JWT token to console
    # print(f"Received JWT token: {jwt_token}")

    # try:
    #     request_json = await request.json()
    #     print(f'Request json: {request_json}')
    # except Exception as e:
    #     print(e)
    #
    # try:
    #     request_body = await request.body()
    #     print(f'Request body: {request_body}')
    # except Exception as e:
    #     print(e)

    # If you need to parse and use the JWT token, do so here
    # try:
    #     decoded_jwt = jwt.decode(token, options={"verify_signature": False})
    # except Exception as e:
    #     print(e)


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
