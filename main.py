import os
import sys
# import logging.config
from fastapi import FastAPI, HTTPException, Body, BackgroundTasks
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import jwt
from pydantic import BaseModel
from typing import Annotated, Optional, Dict, Any
import uvicorn

from common.util import auth_util as auth
from kakaotalk_capture import get_chat_history, send_to_kakao

# Define messenger request model
class MessengerRequest(BaseModel):
    message: str

# Initialize FastAPI app
app = FastAPI(
    title="Messenger Agent API",
    description="RESTful API for interacting with messengers",
    version="1.0.0"
)

@app.post("/chat")
async def post_chat_message(
    request: MessengerRequest = Body(...),
):
    return send_to_kakao(request.message)


@app.get("/chat")
async def get_chat_history(
):
    return { "message": get_chat_history() }


def main():
    print("Hello from messengeragent!")


if __name__ == "__main__":
    main()
