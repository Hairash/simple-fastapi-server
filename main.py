import base64
import json

from fastapi import FastAPI, Request

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
