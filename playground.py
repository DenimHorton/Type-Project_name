import time
import sys 
import datetime
import threading
import RPi.GPIO as GPIO


sys.path.append("~/Documents/Projects/BurgularAlarm/LCDScreen")
from LCDScreen import lcddriver


GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

class BurgularAlarm:
    def __init__(self):
        
        self.AlarmSet=False

        # LCD Driver
        self.lcd = lcddriver.lcd()
        # this command clears the display (captain obvious)
        self.lcd.lcd_clear()
        # now we can display some characters (text, line)
        self.lcd.lcd_display_string("Welcome", 1)
        self.lcd.lcd_display_string("UNARMED", 2)
        dateTime = datetime.datetime.now()
        self.lcd.lcd_display_string(f"{dateTime.month}/{dateTime.day}/{dateTime.year}", 3)
        
        self.lcd.lcd_display_string(dateTime.strftime("%H:%M:%S"), 4)
        self.timeThread = threading.Thread(target=self.updateTimer,)
        self.timeThread.start()

        self.armButtonEvent = threading.Thread(target=self.ArmButtonPressed,)
        self.armButtonEvent.start()

    def ArmButtonPressed(self):

        while GPIO.input(37) != GPIO.HIGH:
            print("Button not Pressed")

        print("Button was pushed!")
        self.alarmLightMenm = threading.Thread(target=self.armedAlarm,)
        self.alarmLightMenm.start()

    def updateTimer(self):
        self.updateTime = True
        while self.updateTime:
            dateTime = datetime.datetime.now()
            self.lcd.lcd_display_string(dateTime.strftime("%H:%M:%S"), 4)

    def armedAlarm(self):

        self.updateTime = False 
        self.lcd.lcd_clear()       
        time.sleep(1)
        self.lcd.lcd_display_string("Secure", 1)
        self.lcd.lcd_display_string("ARMED", 2)
        dateTime = datetime.datetime.now()
        self.lcd.lcd_display_string(f"{dateTime.month}/{dateTime.day}/{dateTime.year}", 3)
        self.armedTimeThread = threading.Thread(target=self.updateTimer,)
        self.armedTimeThread.start()

        self.AlarmSet = True

        while self.AlarmSet:
            time.sleep(2)
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(40, GPIO.OUT)
            GPIO.output(40, GPIO.HIGH)
            time.sleep(1.5)
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(40, GPIO.OUT)            
            GPIO.output(40, GPIO.LOW)

        GPIO.output(40, GPIO.LOW)
        self.lcd.lcd_clear()

    def disarmAlarm(self):
        self.AlarmSet=False
        self.updateTime=False
        self.lcd.lcd_clear()
        time.sleep(1)
        self.lcd.lcd_display_string("Welcome", 1)
        self.lcd.lcd_display_string("UNARMED", 2)
        dateTime = datetime.datetime.now()
        self.lcd.lcd_display_string(f"{dateTime.month}/{dateTime.day}/{dateTime.year}", 3)
        self.unarmedTimeThread = threading.Thread(target=self.updateTimer,)
        self.unarmedTimeThread.start()










bugularAlarm = BurgularAlarm()

time.sleep(5)
bugularAlarm.disarmAlarm()
GPIO.cleanup()

