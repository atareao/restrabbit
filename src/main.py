#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import sys
from fastapi import FastAPI
from pydantic import BaseModel
from publisher import Publisher

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)
app = FastAPI()

APP_ID = os.getenv("RABBIT_APP_ID")
HOST = os.getenv("RABBIT_HOST")
PORT = os.getenv("RABBIT_PORT")
QUEUE = os.getenv("RABBIT_QUEUE")

publisher = Publisher(APP_ID, HOST, PORT, QUEUE)

class Event(BaseModel):
    src: str
    dst: str
    kind: str
    action: str
    content: str

@app.get("/")
async def root_get():
    return {"code": 200,
            "status": "ok",
            "message": "up and running"}

@app.post("/")
async def root_post(event: Event):
    headers = {"src": event.src,
               "dst": event.dst,
               "kind": event.kind,
               "action": event.action}
    response = publisher.send(headers, event.content)
    LOGGER.debug(response)
    print(response)
    return event
