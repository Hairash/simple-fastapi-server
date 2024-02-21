from fastapi import FastAPI, Request

app = FastAPI()


# class Item(BaseModel):
#     data: str


@app.post("/webhook/")
async def receive_webhook(request: Request):
    body = await request.json()
    print(f"Received webhook: {body}")
    return {"message": "Received successfully", "body": body}
