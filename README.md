# Simple Binance Order Recorder for CScalp by 1vere$k
Simple order recorder for the first deal in the row.  
Was made for my wife's trading practises.  
Lot's of space for the future improvements.  
Planning to rework it for async recording for the few orders.  
Will rebuild it totally then - that's the first draft to start practises.
Hasn't planned an `escape scenario` for it yet.  

## Usage for Windows
```
1. git clone https://github.com/iveresk/binance-order-recorder.git && cd binance-order-recorder
2. Create a new API vendor in you Binance account and add it to the "keys.txt" file
3. run - first_start.bat
4. run - run.bat
5. Escape scenario on "Esc" button press on the keyboard or system reboot ofcourse
```

## Usage for Linux or Mac
```
1. git clone https://github.com/iveresk/binance-order-recorder.git && cd binance-order-recorder
2. Create a new API vendor in you Binance account and add it to the "keys.txt" file
3. pip install -r requirements.txt
4. python3 cscalp_video_recorder.py
```