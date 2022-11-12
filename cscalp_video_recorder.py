from binance.client import Client
import time
import cv2
import numpy as np
import pyautogui
from datetime import datetime

# setting up APIs
API_KEY, SECRET_KEY = open("keys.txt", "r").read().split("\n")
client = Client(API_KEY, SECRET_KEY)
# checking for the screen resolution
SCREEN_SIZE = tuple(pyautogui.size())


def createWriter():
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    filename = "output-" + name + "-" + current_time + ".avi"
    out = cv2.VideoWriter(filename, fourcc, 20.0, SCREEN_SIZE)
    webcam = cv2.VideoCapture(0)
    return out, webcam


def captureVideo(out, webcam):
    while True:
        # Capture the screen
        img = pyautogui.screenshot()
        # Convert the image into numpy array
        img = np.array(img)
        # Convert the color space from BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        _, frame = webcam.read()
        # Finding the width, height and shape of our webcam image
        fr_height, fr_width, _ = frame.shape
        # setting the width and height properties
        img[0:fr_height, 0: fr_width, :] = frame[0:fr_height, 0: fr_width, :]
        # cv2.imshow('frame', img)
        # Write the frame into the file 'output.avi'
        out.write(img)
        # Press 'Esc' to quit
        if cv2.waitKey(1) & 0xFF == ord(chr(27).encode()):
            print("Recording is stopped by Esc key press.")
            break
        order = getOrders()
        # waiting on response
        time.sleep(1)
        if order is None:
            print(f" Order is ended. Ending recording for the symbol = {name}")
            break


def getOrders():
    try:
        order = client.futures_adl_quantile_estimate(recvWindow=60000)
    except:
        print("Your Binance is unavailable, check your API key and Internet")
        exit(0)
    return order


# the main algo is here
binance_orders_refresh_time = 31
print("STARTING Py Video Capturer by 1vere$k...")
while True:
    orders = getOrders()
    # waiting on response
    time.sleep(1)
    if orders is not None:
        name = orders[0]["symbol"]
        print(f"start recording symbol = {name}")
        try:
            captureVideo(createWriter())
        except:
            print("Something is wrong with video recording")
        # Values update every 30s. by Binance documentation no need to jerk it off every second as it was previously.
        # https://binance-docs.github.io/apidocs/futures/en/#notional-and-leverage-brackets-user_data
        # waiting on orders update and are checking if order is closed (no more orders).
        time.sleep(binance_orders_refresh_time)









