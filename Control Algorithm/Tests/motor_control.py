import RPi.GPIO as GPIO
from time import sleep
import math

#CAMERA
height_constant = 10 #depends on the resolution CHANGE
vert_center = 0 #center pixel vertically CHANGE THIS
hor_center = 0 #center pixel horizontally CHANGE THIS

#MOTORS
motor_1 = 16 #pin 16, gpio 23, controls horizontal movement
motor_2 = 18 #pin 18, gpio 24, controls vertical movement (nozzle head)

#LEDs
led_1 = 11 #gpio 17
led_2 = 13 #gpio 27
led_3 = 15 #gpio 22


#get duty cycle from angle
def get_pwm(angle):
    return (angle/18.0) + 2.5

def gpio_setup():
    GPIO.setmode(GPIO.BOARD) #GPIO.BCM
    GPIO.setup(motor_1, GPIO.OUT)
    GPIO.setup(motor_2, GPIO.OUT)
    GPIO.setup(led_1, GPIO.OUT)
    GPIO.setup(led_2, GPIO.OUT)
    GPIO.setup(led_3, GPIO.OUT)
    pwm1=GPIO.PWM(motor_1, 50) #50 Hz
    pwm2=GPIO.PWM(motor_2, 50) #50 Hz
    GPIO.output(led_1, GPIO.LOW)
    GPIO.output(led_2, GPIO.LOW)
    GPIO.output(led_3, GPIO.LOW)
    return pwm1, pwm2

def startup():
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
def turn_motor(pwm1, pwm2, coordinates, state): #coordinates will give the x, y, w, h in pixel values
    # pwm1, pwm2 = gpio_setup()

    #depends on the resolution
    if state == 1: #extinguishing
        GPIO.output(led_1, GPIO.HIGH)
        GPIO.output(led_2, GPIO.HIGH)
        GPIO.output(led_3, GPIO.LOW)

        azimuth = math.atan((coordinates[0] - hor_center)/height_constant) #angle along the horizontal axis
        elevation = math.atan((coordinates[1] - vert_center)/height_constant) #angle along the vertical axis
        azi_dc = get_pwm(azimuth)
        elev_dc = get_pwm(elevation)
        pwm1.start(0)
        pwm2.start(0)
        print(azi_dc, elev_dc)
        pwm1.ChangeDutyCycle(azi_dc)
        pwm2.ChangeDutyCycle(elev_dc)
        sleep(1)
        #the STOP below is questionable since we need to update the position continuously until the fire is no longer there
        pwm1.stop()
        pwm2.stop()
    elif state == 2: #reset
        #MAYBE JUST PASS THE MIDDLE OF THE SCREEN COORDINATES TO RESET
        GPIO.output(led_1, GPIO.HIGH)
        GPIO.output(led_2, GPIO.HIGH)
        GPIO.output(led_3, GPIO.HIGH)

    elif state == 0: #data collection 
        GPIO.output(led_1, GPIO.HIGH)
        GPIO.output(led_2, GPIO.LOW)
        GPIO.output(led_3, GPIO.LOW)
    else:
        print("Invalid State")
# startup()
# turn_motor([30, 30], 0)
# sleep(3)
turn_motor([30, 30], 1)
sleep(3)
turn_motor([-30, -30], 1)
sleep(3)
GPIO.cleanup()



# GPIO.cleanup()