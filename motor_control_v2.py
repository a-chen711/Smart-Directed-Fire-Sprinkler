from gpiozero import AngularServo
import RPi.GPIO as GPIO
from gpiozero.pins.pigpio import PiGPIOFactory
import math
from time import sleep, time

#STATES
DATACOLL = 0 
EXT = 1
RESET = 2

#CAMERA
height_constant = 10 #depends on the resolution CHANGE
hor_res = 480
vert_res = 480
vert_center = vert_res/2 #center pixel vertically CHANGE THIS
offset = 0
hor_center = hor_res/2 + offset #center pixel horizontally CHANGE THIS


#MOTORS
motor_1 = 23 #pin 16, gpio 23, controls horizontal movement
motor_2 = 24 #pin 18, gpio 24, controls vertical movement (nozzle head)
maxPW=2.5/1000
minPW=0.5/1000
#values are flipped because images grow downwards in pixel index
noz_max = -10
noz_mid = 35
noz_min = 80

gim_max = -45
gim_mid = 0
gim_min = 45

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
    GPIO.output(sol_pin, GPIO.LOW)
    #IR setup
    GPIO.setup(ir_pin,GPIO.IN) #ir_pin will be LOW if a fire is detected
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

def get_angle(point, center, type):
    if type == 'v':
        return ((point - center)/center)*45
    offset = -35
    return ((point - center)/center)*45 + offset

def zigzag(x, y, w, h):
    pt1 = (x, y)
    pt2 = (x + w, y + h/2)
    pt3 = (x, y + h/2)
    pt4 = (x + w, y + h)
    point_map = [pt1, pt2, pt3, pt4]
    return point_map

def sweep(servo1, servo2, x, y, w, h):
    point_map = zigzag(x, y, w, h)
    rpoint_map = point_map[::-1] #get reverse list
    map_len = len(point_map)
    for j in range(4): #goes back and forth 4 times
        print("FORWARD")
        for i in range(map_len):
            azimuth = -get_angle(point_map[i][0], vert_center, 'h') #angle along the vertical axis
            elevation = -get_angle(point_map[i][1], hor_center, 'v') #angle along the horizontal axis (negative because pixel values grow downwards)
            servo1.angle = elevation
            servo2.angle = azimuth
            sleep(0.2)
        print("BACKWARDS")
        for i in range(map_len):
            azimuth = -get_angle(rpoint_map[i][0], vert_center, 'h') #angle along the vertical axis
            elevation = -get_angle(rpoint_map[i][1], hor_center, 'v') #angle along the horizontal axis (negative because pixel values grow downwards)
            servo1.angle = elevation
            servo2.angle = azimuth
            sleep(0.2)
    #end pn the middle
    box_center_x = x + w/2
    box_center_y = y + h/2
    azimuth = -get_angle(box_center_x, vert_center, 'h') #angle along the vertical axis
    elevation = -get_angle(box_center_y, hor_center, 'v') #angle along the horizontal axis
    servo1.angle = elevation
    servo2.angle = azimuth

#turn motors according to the coordinates fed from the fire detection algorithm
def turn_motor(servo1, servo2, coordinates, state, updating): #coordinates will give the x, y, w, h in pixel values
    #depends on the resolution
    trig_count = 0
    if state == EXT: #extinguishing
        print("EXTINGUISH")
        GPIO.output(led_1, GPIO.HIGH)
        GPIO.output(led_2, GPIO.HIGH)
        GPIO.output(led_3, GPIO.LOW)

        x, y, w, h = coordinates[0], coordinates[1], coordinates[2], coordinates[3]
        box_center_x = x + w/2
        box_center_y = y + h/2
        azimuth = -get_angle(box_center_x, vert_center, 'h') #angle along the vertical axis
        elevation = -get_angle(box_center_y, hor_center, 'v') #angle along the horizontal axis
        servo1.angle = elevation
        servo2.angle = azimuth
        sleep(1)
        
        if updating == False: #if it hasn't been triggered yet
            verify = time()
            while time() - verify <= 2: #verify for 2 seconds before resetting (if ir_pin is high)
                print("Verifying...")
                while GPIO.input(ir_pin) == 0 and w*h >= 200: #if ir_pin low and area of box is larger than 90
                    trig_count += 1
                    if trig_count == 1:
                        start = time()
                    elif time() - start >= 3: #if IR is high for 3 seconds, we activate the solenoid
                        print("Activating Solenoid...")
                        GPIO.output(sol_pin, GPIO.HIGH) #ACTIVATE SOLENOID VALVE
                        sleep(2) #spray at the middle for 2 seconds
                        sweep(servo1, servo2, x, y, w, h)  #sweep a set amount of times (end at the middle)
                        activated = not GPIO.input(ir_pin) #check IR after, if it's low, then it still needs to activate
                        return activated
                print("IR pin is low or area is " + str(w*h))
        else: # if it has been triggered previously and we're only updating the position, we don't need the checks
            if GPIO.input(ir_pin) == 0 and w*h >= 90: #if ir_pin low and area of box is larger than 90 pixels squared
                print("Updating Position of Nozzle...")
                sweep(servo1, servo2, x, y, w, h)  #sweep a set amount of times (end at the middle)
                activated = not GPIO.input(ir_pin)
                return activated
            # turn_motor(servo1, servo2, None, 2) #RESET (regardless of activation or not)
    elif state == RESET: #reset
        print("RESET")
        GPIO.output(led_1, GPIO.HIGH) #Change LEDs
        GPIO.output(led_2, GPIO.HIGH)
        GPIO.output(led_3, GPIO.HIGH)

        GPIO.output(sol_pin, GPIO.LOW) #Stop Solenoid for 2 seconds
        sleep(2)
        
        servo1.angle = gim_mid #approximately middle
        servo2.angle = gim_mid #approximately middle
        sleep(0.5)
    elif state == DATACOLL: #data collection 
        GPIO.output(led_1, GPIO.HIGH)
        GPIO.output(led_2, GPIO.LOW)
        GPIO.output(led_3, GPIO.LOW)
        print("DATA COLLECTION")
    else:
        print("Invalid State")
    return False

def position_handler(servo1, servo2, coords, triggered_before):
    activated = turn_motor(servo1, servo2, coords, EXT, triggered_before)
    if activated:
        return activated #this means that there was a fire and we've swept the box, update the position
    turn_motor(servo1, servo2, None, RESET, triggered_before)
    turn_motor(servo1, servo2, None, DATACOLL, triggered_before) #DATA COLLECTION
    return activated

def cleanup():
    GPIO.cleanup()