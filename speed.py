import RPi.GPIO as GPIO
import time
import pyrebase
import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

config = {
    "apiKey": "*******************************",
    "authDomain": "************************************",
    "databaseURL": "************************************",
    "storageBucket": "************************************",
    "serviceAccount": "************************************"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

GPIO.setup(14, GPIO.IN, pull_up_down = GPIO.PUD_UP)

circum = 66 # cirumference of the wheel in inches
start = time.time()
sensorStatus = False
mph = 0
dist = 0
odo = int(db.child("odometer").get().val())


def main():
    try:
        global start, sensorStatus, mph, dist, odo
        while True:
            if (time.time() - start) > 1:
                mph = 0
            db.update({'speed': mph})
            db.update({'odometer': odo})
            db.update({'trip_distance': round((dist / 63360), 2)})
            db.update({'last_update': str(datetime.datetime.utcnow())})
            f = open("speed.txt", "w")
            f.write(str(mph))
            f.close()
                
    except KeyboardInterrupt:
        GPIO.cleanup()  
    


def speedy(number):
    global start, mph, dist, odo
    end = time.time()
    dur = end - start
    start = end
    dist += 66
    odo += 66
    mph = round((circum * 3600) / (dur * 63360), 2)
    print(mph)
    


GPIO.add_event_detect(14, GPIO.RISING, callback=speedy)

if __name__=="__main__":
   main()
