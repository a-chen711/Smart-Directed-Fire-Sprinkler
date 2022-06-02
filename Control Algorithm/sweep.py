from gpiozero import AngularServo
from time import sleep
import RPi.GPIO as GPIO
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()
motor_1 = 23
motor_2 = 24
myCorrection=0.45
maxPW=2.5/1000
minPW=0.5/1000
 
servo1 = AngularServo(motor_1,min_pulse_width=minPW,max_pulse_width=maxPW, pin_factory = factory)
servo2 = AngularServo(motor_2,min_pulse_width=minPW,max_pulse_width=maxPW, pin_factory = factory)

#nozzle range = 40
noz_max = -10
noz_mid = 35
noz_min = 80

gim_max = -45
gim_mid = 0
gim_min = 45

hor_center = 480/2
vert_center = 480/2

#LEDs
led_1 = 17 #pin 11, gpio 17
led_2 = 27 #pin 13, gpio 27
led_3 = 22 #pin 15, gpio 22

#IR Sensor
ir_pin = 4 #pin 7, gpio 4

#Solenoid 
sol_pin = 25 #pin 22, GPIO 25

def get_angle(point, center):
    return ((point - center)/center)*45

def zigzag(x, y, w, h):
    pt1 = (x, y)
    pt2 = (x + w, y + h/2)
    pt3 = (x, y + h/2)
    pt4 = (x + w, y + h)
    point_map = [pt1, pt2, pt3, pt4]
    return point_map

def reverse_test():
    mapz = [1, 2, 3, 4, 5]
    rmapz = mapz[::-1]
    for j in range(3):
        print("FORWARD")
        for i in range(len(mapz)):
            print(mapz[i])
        print("REVERSE")
        for i in range(len(mapz)):
            print(rmapz[i])

def sweep(x, y, w, h):
    area = w * h
    #need a check for the size of the bounding box, otherise there will be a problem?
    if area < 90: #PUT THIS IN THE CONTROL ALGORITHM MAYBE INSTEAD, check for this before calling the sweep, otherwise just do a normal target
        return False
    point_map = zigzag(x, y, w, h)
    rpoint_map = point_map[::-1] #get reverse list
    map_len = len(point_map)
    for j in range(4): #goes back and forth 4 times
        print("FORWARD")
        for i in range(map_len):
            azimuth = get_angle(point_map[i][0], hor_center) #angle along the horizontal axis
            elevation = -get_angle(point_map[i][1], vert_center) #angle along the vertical axis (negative because pixel values grow downwards)
            servo1.angle = azimuth
            servo2.angle = elevation
            sleep(0.2)
        print("BACKWARDS")
        for i in range(map_len):
            azimuth = get_angle(rpoint_map[i][0], hor_center) #angle along the horizontal axis
            elevation = -get_angle(rpoint_map[i][1], vert_center) #angle along the vertical axis (negative because pixel values grow downwards)
            servo1.angle = azimuth
            servo2.angle = elevation
            sleep(0.2)
# sweep(0, 0, 80, 80)

def ir_test():
    GPIO.setmode(GPIO.BCM) #GPIO.BCM
    GPIO.setup(ir_pin, GPIO.IN)
    while GPIO.input(ir_pin) == True:
        print("Nothing detected")
    print("FIRE DETECTED")
    GPIO.cleanup()
# ir_test()

def angle_test():
    servo1.angle = 30 #UP
    sleep(2)
    servo2.angle = 30 #LEFT
    sleep(2)
    GPIO.cleanup()
angle_test()

def basic_test():
    print("Setting up GPIO...")
    GPIO.setmode(GPIO.BCM) #GPIO.BCM
    GPIO.setup(led_1, GPIO.OUT)
    GPIO.setup(led_2, GPIO.OUT)
    GPIO.setup(led_3, GPIO.OUT)
    GPIO.output(led_1, GPIO.LOW)
    GPIO.output(led_2, GPIO.LOW)
    GPIO.output(led_3, GPIO.LOW)

    #solenoid setup
    GPIO.setup(sol_pin, GPIO.OUT)
    GPIO.output(sol_pin, GPIO.LOW) #ACTIVATE SOLENOID VALVE

    print("Testing LED's")
    GPIO.output(led_1, GPIO.HIGH)
    GPIO.output(led_2, GPIO.LOW)
    GPIO.output(led_3, GPIO.LOW)
    sleep(1)
    GPIO.output(led_1, GPIO.HIGH)
    GPIO.output(led_2, GPIO.HIGH)
    GPIO.output(led_3, GPIO.LOW)
    sleep(1)
    GPIO.output(led_1, GPIO.HIGH)
    GPIO.output(led_2, GPIO.HIGH)
    GPIO.output(led_3, GPIO.HIGH)
    sleep(1)
    GPIO.output(led_1, GPIO.LOW)
    GPIO.output(led_2, GPIO.LOW)
    GPIO.output(led_3, GPIO.LOW)
    sleep(1)

    print("Testing Servo 1")
    print("Go to MIDDLE")
    servo1.angle = gim_mid #approximately middle
    sleep(2)
    print("Go to min")
    servo1.angle = gim_min
    sleep(2)
    print("Go to max") #moving clockwise
    servo1.angle = gim_max
    sleep(2)
    print("Go to MIDDLE")
    servo1.angle = gim_mid #approximately middle
    sleep(4)
    servo1.value = None;

    print("Testing Servo 2")
    print("Go to MIDDLE")
    servo2.angle = noz_mid
    sleep(2)
    print("Go to min")
    servo2.angle = noz_min
    sleep(2)
    print("Go to max") #moving clockwise
    servo2.angle = noz_max
    sleep(2)
    print("Go to MIDDLE")
    servo2.angle = noz_mid
    sleep(2)
    servo2.value = None;

    print("Testing Solenoid")
    GPIO.output(sol_pin, GPIO.LOW) #ACTIVATE SOLENOID VALVE
    sleep(2)
    GPIO.output(sol_pin, GPIO.HIGH) #ACTIVATE SOLENOID VALVE
    sleep(2) #spray at the middle for 2 seconds
    GPIO.output(sol_pin, GPIO.LOW) #ACTIVATE SOLENOID VALVE
    print("CLEANING GPIO")
    GPIO.cleanup()
# basic_test()
    
# from gpiozero import Servo
# from time import sleep

# from gpiozero.pins.pigpio import PiGPIOFactory

# factory = PiGPIOFactory()
# motor_1 = 23
# motor_2 = 24
# myCorrection=0.45
# maxPW=2.5/1000
# minPW=0.5/1000
 
# servo1 = Servo(motor_1,min_pulse_width=minPW,max_pulse_width=maxPW, pin_factory = factory)
# servo2 = Servo(motor_2,min_pulse_width=minPW,max_pulse_width=maxPW, pin_factory = factory)

# noz_rom = 0.5 #nozzle range of motion
# noz_mid = 0
# noz_min = -1 * noz_rom
# noz_max = noz_rom

# gim_rom = 0.7 #gimbal range of motion
# gim_mid = -0.4
# gim_min = -1 * (gim_rom)
# gim_max = (gim_rom)

# print("Start in the middle")
# servo1.value = gim_mid
# servo2.value = noz_mid
# sleep(2)
# print("Go to min") #moving clockwise
# servo1.value = gim_min
# servo2.value = noz_min
# sleep(2)
# print("Go to max") #moving counter-clockwise
# servo1.value = gim_max
# servo2.value = noz_max
# sleep(2)
# print("Go to min") #moving clockwise
# servo1.value = gim_min
# servo2.value = noz_min
# sleep(2)
# print("Go to max") #moving counter-clockwise
# servo1.value = gim_max
# servo2.value = noz_max
# sleep(2)
# print("Start in the middle")
# servo1.value = gim_mid
# servo2.value = noz_mid
# sleep(2)

# # print("Go to min") #moving clockwise
# # servo1.min()
# # servo2.min()
# # sleep(1.2)
# # print("Go to max") #moving counter-clockwise
# # servo1.max()
# # servo2.max()
# # sleep(1.2)
# # print("Go to min")
# # servo1.min()
# # servo2.min()
# # sleep(1.2)
# # print("Go to max")
# # servo1.max()
# # servo2.max()
# # sleep(1.2)
# # print("And back to middle")
# # servo1.mid()
# # servo2.mid()
# # sleep(2)
# servo1.value = None;
# servo2.value = None;


# print("Go to min") #moving clockwise
# servo1.min()
# servo2.min()
# sleep(1.2)
# print("Go to max") #moving counter-clockwise
# servo1.max()
# servo2.max()
# sleep(1.2)
# print("Go to min")
# servo1.min()
# servo2.min()
# sleep(1.2)
# print("Go to max")
# servo1.max()
# servo2.max()
# sleep(1.2)
# print("And back to middle")
# servo1.mid()
# servo2.mid()
# sleep(2)
servo1.value = None;
servo2.value = None;
