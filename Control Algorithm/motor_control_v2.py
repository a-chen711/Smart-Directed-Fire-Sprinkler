from gpiozero import AngularServo
import RPi.GPIO as GPIO
from gpiozero.pins.pigpio import PiGPIOFactory
import math
from time import sleep, time

#CAMERA
height_constant = 10 #depends on the resolution CHANGE
hor_res = 480
vert_res = 480
vert_center = vert_res/2 #center pixel vertically CHANGE THIS
hor_center = hor_res/2 #center pixel horizontally CHANGE THIS


#MOTORS
motor_1 = 23 #pin 16, gpio 23, controls horizontal movement
motor_2 = 24 #pin 18, gpio 24, controls vertical movement (nozzle head)
maxPW=2.5/1000
minPW=0.5/1000
noz_mid = 35
noz_min = -10
noz_max = 75
gim_mid = 0
gim_min = -45
gim_max = 45

#LEDs
led_1 = 17 #pin 11, gpio 17
led_2 = 27 #pin 13, gpio 27
led_3 = 22 #pin 15, gpio 22

#IR Sensor
ir_pin = 4 #pin 7, gpio 4

#Solenoid 
sol_pin = 25 #pin 22, GPIO 25

def gpio_setup():
    print("Setting up GPIO...")
    GPIO.setmode(GPIO.BCM) #GPIO.BCM
    
    #Servo setup
    factory = PiGPIOFactory() 
    # servo1 = Servo(motor_1,min_pulse_width=minPW,max_pulse_width=maxPW, pin_factory = factory)
    # servo2 = Servo(motor_2,min_pulse_width=minPW,max_pulse_width=maxPW, pin_factory = factory)
    servo1 = AngularServo(motor_1,min_pulse_width=minPW,max_pulse_width=maxPW, pin_factory = factory)
    servo2 = AngularServo(motor_2,min_pulse_width=minPW,max_pulse_width=maxPW, pin_factory = factory)
    servo1.angle = gim_mid #approximately middle
    servo2.angle = gim_mid #approximately middle
    sleep(1)

    #LED setup
    GPIO.setup(led_1, GPIO.OUT)
    GPIO.setup(led_2, GPIO.OUT)
    GPIO.setup(led_3, GPIO.OUT)
    GPIO.output(led_1, GPIO.LOW)
    GPIO.output(led_2, GPIO.LOW)
    GPIO.output(led_3, GPIO.LOW)

    #solenoid setup
    GPIO.setup(sol_pin, GPIO.OUT)

    #IR setup
    GPIO.setup(ir_pin,GPIO.IN)
    return servo1, servo2

def startup(): #blink lights three times to indicate the system startup
    print("Staring up...")
    for i in range(3):
        GPIO.output(led_1, GPIO.HIGH)
        GPIO.output(led_2, GPIO.HIGH)
        GPIO.output(led_3, GPIO.HIGH)
        sleep(1)
        GPIO.output(led_1, GPIO.LOW)
        GPIO.output(led_2, GPIO.LOW)
        GPIO.output(led_3, GPIO.LOW)
        sleep(1)
        i+=1

#turn motors according to the coordinates fed from the fire detection algorithm
def turn_motor(servo1, servo2, coordinates, state): #coordinates will give the x, y, w, h in pixel values
    # servo1, servo2 = gpio_setup()
    #depends on the resolution
    trig_count = 0
    if state == 1: #extinguishing
        print("EXTINGUISH")
        GPIO.output(led_1, GPIO.HIGH)
        GPIO.output(led_2, GPIO.HIGH)
        GPIO.output(led_3, GPIO.LOW)

        x, y, w, h = coordinates[0], coordinates[1], coordinates[2], coordinates[3]
        azimuth = ((x - hor_center)/hor_center)*45 #angle along the horizontal axis
        elevation = -((y - vert_center)/vert_center)*45 #angle along the vertical axis (negative because pixel values grow downwards)
        servo1.angle = azimuth
        servo2.angle = elevation
        sleep(1)
        verify = time()
        while time() - verify <= 2: #verify for 2 seconds before resetting (if ir_pin is not high)
            print("Verifying...")
            while GPIO.input(ir_pin):
                trig_count += 1
                if trig_count == 1:
                    start = time()
                elif time() - start >= 3: #if IR is high for 3 seconds, we activate the solenoid
                    print("Activating Solenoid...")
                    GPIO.output(sol_pin, GPIO.HIGH) #ACTIVATE SOLENOID VALVE
        turn_motor(servo1, servo2, None, 2) #RESET (regardless of activation or not)
    elif state == 2: #reset
        print("RESET")
        GPIO.output(led_1, GPIO.HIGH) #Change LEDs
        GPIO.output(led_2, GPIO.HIGH)
        GPIO.output(led_3, GPIO.HIGH)

        GPIO.output(sol_pin, GPIO.LOW) #Stop Solenoid for 2 seconds
        sleep(2)
        
        servo1.angle = gim_mid #approximately middle
        servo2.angle = gim_mid #approximately middle
        sleep(1)
        turn_motor(servo1, servo2, None, 0) #DATA COLLECTION
    elif state == 0: #data collection 
        GPIO.output(led_1, GPIO.HIGH)
        GPIO.output(led_2, GPIO.LOW)
        GPIO.output(led_3, GPIO.LOW)
        print("DATA COLLECTION")
    else:
        print("Invalid State")

def cleanup():
    GPIO.cleanup()