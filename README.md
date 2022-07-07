# Capstone Project: Smart Fire Sprinkler

This repository contains the software for my Undergraduate Capstone Project. **The goal was to create a smart fire sprinkler to combat the water damage caused by conventional fire sprinklers due to their indiscriminate spray pattern**. A single conventional fire sprinkler pumps out 15 gallons of water per minute, resulting in potentially catastrophic damage even after the fire has been extinguished. Please see our project elevator pitch below:

<p align="middle">
  <a href="https://www.youtube.com/watch?v=y3B0_WWEmtY&list=PLKiuu4WpUq1-CE1xshvQDQ768bJ5ZX2bB&index=5" target="_blank">
    <img src="https://img.youtube.com/vi/y3B0_WWEmtY/maxresdefault.jpg" alt="Watch the video" width="640" height="360" border="10" />
  </a>
</p>

## How it Works


## Files 
- _fire_algo.py_ is the final fire detection algorithm, used to detect and create a bounding box around a fire in frame.
- _motor_control_v2.py_ is the final control algorithm, in charge of integrating the IR sensor and visual data to actuate the servo motors and aim at the fire as well as state switching.
- _sweep.py_ contains the function for the nozzle sweeping.
- _Control Algorithm_ contains older versions of the control algorithm, as well as an implementation that does not utilize the IR sensor.
- _Old Fire Detection Algorithms_ contains deprecated versions and prototyping of previous methods used to detect fires (Haar Cascade, CNN, etc.).
- _requirements.txt_ contains the modules necessary to run the project. 

## Hardware Components 💻
- Raspberry Pi Zero W
- [Raspberry Pi Camera Module 2](https://www.raspberrypi.com/products/camera-module-v2/)
- [MG996R Servo Motors](https://www.amazon.com/4-Pack-MG996R-Torque-Digital-Helicopter/dp/B07MFK266B)
- [IR Sensor Module](https://www.amazon.com/LGDehome-Infrared-Detection-Detecting-Distance/dp/B07TV1CZDK/ref=sr_1_5?crid=2GSWD944HS1X5&keywords=fire+ir+sensor&qid=1657234742&sprefix=fire+ir+senso%2Caps%2C134&sr=8-5)
- 12V Solenoid Valve
- 12V Power Supply
- 12V to 5V Buck Converter
- 3D Printed 2 DOF Gimbal Mechanism
- 3D Printed Nozzle
- Flexible PVC Tubing

## Demo :rocket:
