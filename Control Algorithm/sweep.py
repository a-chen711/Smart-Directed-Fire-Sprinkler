from gpiozero import AngularServo
from time import sleep

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
noz_mid = 35
noz_min = -10
noz_max = 75

gim_mid = 0
gim_min = -45
gim_max = 45

#90 is max
#-90 is min

# print("Start in the middle")
# servo1.mid()
# servo2.mid()
# sleep(2)
print("Testing Servo 1")
print("Go to 0")
servo1.angle = gim_mid #approximately middle
sleep(2)
print("Go to min")
servo1.angle = gim_min
sleep(2)
print("Go to 90") #moving clockwise
servo1.angle = gim_max
sleep(2)
print("Go to 0")
servo1.angle = gim_mid #approximately middle
sleep(4)
servo1.value = None;

print("Testing Servo 2")
print("Go to 30")
servo2.angle = noz_mid
sleep(2)
print("Go to -10")
servo2.angle = noz_min
sleep(2)
print("Go to 70") #moving clockwise
servo2.angle = noz_max
sleep(2)
print("Go to 30")
servo2.angle = noz_mid
sleep(2)
servo2.value = None;
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
