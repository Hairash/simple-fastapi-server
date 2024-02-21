from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    data: str


@app.post("/webhook/")
async def receive_webhook(item: Item):
    print(f"Received webhook: {item.data}")
    return {"message": "Received successfully", "data": item.data}
