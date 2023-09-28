from datetime import datetime as d
from typing import Union
from fastapi import FastAPI, BackgroundTasks
from fastapi import FastAPI, WebSocket
import serial
import re
from send_email import send_email_background

app = FastAPI()

@app.get("/")
def read_arduino(background_tasks: BackgroundTasks):
    ser = serial.Serial('/dev/cu.usbmodem14201', 9800, timeout=1)

    smoke = None
    while True:
        reading = re.findall('\d+',ser.readline().decode())
        if len(reading) > 0:
            smoke = int(reading[0])
            if smoke >= 60:
                # try:
                send_email_background('abuzar_12@hotmail.com', str(smoke), background_tasks)
                # except:
                #     'Failed to send'
            break

    return smoke
