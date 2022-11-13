from binance.client import Client
import time
import cv2
import pyautogui
from numpy import asarray
from datetime import datetime


def createWriter(name, screensize):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    filename = "output-" + name + "-" + current_time + ".avi"
    out = cv2.VideoWriter(filename, fourcc, 20.0, screensize)
    webcam = cv2.VideoCapture(0)
    return out, webcam


def captureVideo(out, webcam, name, client):
    while True:
        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            out.release()
            cv2.destroyAllWindows()
            print("Recording is stopped by Esc key press.")
            break
        # Capture the screen
        img = pyautogui.screenshot()
        # Convert the image into numpy array
        img = asarray(img)
        # Convert the color space from BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        _, frame = webcam.read()
        # Finding the width, height and shape of our webcam image
        fr_height, fr_width, _ = frame.shape
        # setting the width and height properties
        img[0:fr_height, 0: fr_width, :] = frame[0:fr_height, 0: fr_width, :]
        cv2.imshow('frame', img)
        # Write the frame into the file 'output.avi'
        out.write(img)
        # checking if we have more to capture
        order = getOrders(client)
        # waiting on response
        if not order:
            out.release()
            cv2.destroyAllWindows()
            print(f" Order is ended. Ending recording for the symbol = {name}")
            break


def getOrders(client):
    try:
        order = client.futures_adl_quantile_estimate(recvWindow=60000)
    except:
        print("Your Binance is unavailable, check your API key and Internet")
        exit(0)
    return order


# the main algo is here
def main():
    # setting up APIs
    API_KEY, SECRET_KEY = open("keys.txt", "r").read().split("\n")
    client = Client(API_KEY, SECRET_KEY)
    # checking for the screen resolution
    screensize = tuple(pyautogui.size())
    binance_orders_refresh_time = 31
    print("STARTING Py Video Capturer by 1vere$k...")
    while True:
        orders = getOrders(client)
        # waiting on response
        if orders:
            name = orders[0]["symbol"]
            print(f"start recording symbol = {name}")
            try:
                out, webcam = createWriter(name, screensize)
                captureVideo(out, webcam, name, client)
            except:
                print("Something is wrong with video recording")
            # Values update every 30s. by Binance documentation no need to jerk it off every second as it was previously.
            # https://binance-docs.github.io/apidocs/futures/en/#notional-and-leverage-brackets-user_data
            # waiting on orders update and are checking if order is closed (no more orders).
            time.sleep(binance_orders_refresh_time)


if __name__ == "__main__":
    main()
