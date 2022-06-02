from time import time, sleep

def turn_motor(ir_pin, state): #coordinates will give the x, y, w, h in pixel values
    # servo1, servo2 = gpio_setup()
    #depends on the resolution
    trig_count = 0
    if state == 1: #extinguishing
        print("EXTINGUISH")
        verify = time()
        while time() - verify <= 2: #verify for 2 seconds before resetting (if ir_pin is not high)
            print("Verifying")
            while ir_pin:
                # print("trig_count = " + str(trig_count))
                trig_count += 1
                if trig_count == 1:
                    ir_start = time()
                elif time() - ir_start >= 10: #DON'T INCLUDE THIS this is the theoretical when the ir_pin is falsE 
                    print("fire put out")
                    ir_pin = False
                elif time() - ir_start >= 3:
                    print("SOLENOID HIGH") #ACTIVATE SOLENOID VALVE
                    # break
        turn_motor(ir_pin, 2) #RESET
        #the STOP below is questionab\le since we need to update the position continuously until the fire is no longer there
        # servo1.stop()
        # servo2.stop()
    elif state == 2: #reset
        print("RESET")
        sleep(2)
        turn_motor(ir_pin, 0)
    elif state == 0: #data collection 
        print("DATA COLLECTION")
        sleep(2)
    else:
        print("Invalid State")

try:
    ir_pin = True
    turn_motor(ir_pin,1)
    # turn_motor(ir_pin,2)
except KeyboardInterrupt:
    print("DONZO")


