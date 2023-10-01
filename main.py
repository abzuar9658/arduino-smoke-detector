from datetime import datetime as d
from typing import Union
from fastapi import FastAPI, BackgroundTasks
from fastapi import FastAPI, WebSocket
import serial
import re
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from send_email import send_email_background

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/fetch_temperature")
def read_arduino(email: str, background_tasks: BackgroundTasks):
    ser = serial.Serial('/dev/cu.usbmodem14201', 9800, timeout=1)

    smoke = None
    while True:
        reading = re.findall('\d+',ser.readline().decode())

        if len(reading) > 0:
            smoke = int(reading[0])
            if smoke >= 300:
                send_email_background(email, str(smoke), background_tasks)
            break

    return smoke
