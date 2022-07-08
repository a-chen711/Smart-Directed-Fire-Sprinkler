# Capstone Project: Smart Fire Sprinkler

This repository contains the software portion of my Undergraduate Capstone Project for ECE 183DA-B

## Problem Statement and Goal
A single conventional fire sprinkler pumps out 15 gallons of water per minute in an indiscriminate spray pattern, resulting in potentially catastrophic water damage to the contents of a room even after the fire has been extinguished.**This project's goal was to create a smart fire sprinkler to minimize water damage using computer vision and targeted extinguishing.** Please see our project elevator pitch below:

<p align="middle">
  <a href="https://www.youtube.com/watch?v=y3B0_WWEmtY&list=PLKiuu4WpUq1-CE1xshvQDQ768bJ5ZX2bB&index=5" target="_blank">
    <img src="https://img.youtube.com/vi/y3B0_WWEmtY/maxresdefault.jpg" alt="Watch the video" width="640" height="360" border="10" />
  </a>
</p>

If you are interested in the comprehensive (~60 minute) presentation, it can be found [here](https://www.youtube.com/watch?app=desktop&v=1DF-TpntejU&list=PLKiuu4WpUq18h715fSSBkkSOx-3rHuwM5&index=4). The software portion pertaining to this repository begins at 42:00.

## How it Works
### State Diagram
<p align="middle">
  <img src="https://user-images.githubusercontent.com/59714253/177891359-8ffc2a0d-06e4-444a-a436-1dde99527a0c.png" alt="State Diagram" width="414" height="240"/>
</p> 

### Data Flowchart
<p align="middle">
  <img src="https://user-images.githubusercontent.com/59714253/177889858-f419c091-82bc-4851-9f92-dd09c8a0d7fc.png" alt="Data Flowchart" width="900" height="380"/>
</p>

### Logic Explanation
The system begins in the _Data Collection_ state. Here the camera passes visual data to the Fire Detection Algorithm where an HSV colormask is applied to the image. It is then thresholded to the pixels with values between (255, 105, 0) and (255, 220, 30). Subsequently, segmentation is performed to isolate the pixels within these boundaries from the image. Then a 3x3 dilation kernel is iterated over the image for 14 iterations in order to reduce short gaps between the contours detected. After this is completed, a bounding box is drawn around the detected contour. 

<p align="middle">
  <img src="https://user-images.githubusercontent.com/59714253/177890471-868bb227-80ec-4701-8077-95c9c9d81bd2.png" alt="Bounding Box"/>
</p>

If a contour is extracted, indicating a potential fire detection, the bounding box pixel coordinates are sent to the Control Algorithm, where a coordinate to angle conversion is performed. As the images are taken in a resolution of 480x480 pixels, the distance from the coordinates to the center of the image are normalized between the angles -45 and 45, with an angle of 0 representing the center of the frame.

This is performed on the horizontal and vertical axes. The normalized angles are then passed to a function from the _gpiozero_ module that converts the angles into a PWM signal for the servos controlling the 2-DOF gimbal mechanism. Once the targeting is complete and the nozzle is pointing at the supposed fire, the IR sensor attached to the nozzle is read continuously for 3 seconds to verify that the targeted location has the visual and IR signature of a fire. If 3 seconds of IR radiation are detected, the system verifies that there is a fire that is currently being targeted by the nozzle and the system enters the _**Extinguish**_ state. Anything other than a continuous stream of IR radiation is deemed not a fire, and the system enters the Reset state, in which the nozzle is reset back to a position normal to the ceiling. 

If in the _**Extinguish**_ state, the system activates the solenoid valve to begin a pressurized stream of water from the building infrastructure. The nozzle then moves in a sweeping “Z” pattern within the detected bounding box to best apply water to the fire. After 3 sweeps of the bounding box, the system points at the center of the bounding box and checks for an IR reading. If the IR radiation is no longer detected, the system deems the fire extinguished. It then moves into the _**Reset**_ state. If the IR radiation continues to be high, the system continues the sweeping motion until the fire is extinguished. 

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
- 3 LEDs
- 3D Printed 2 DOF Gimbal Mechanism
- 3D Printed Nozzle
- Flexible PVC Tubing

## Demos :rocket:
### Negative Detection

https://user-images.githubusercontent.com/59714253/177892495-123c028a-285c-4eb7-b774-d8f4a2c317af.mp4

### Positive Detection (with simulated IR source)

https://user-images.githubusercontent.com/59714253/177892520-c7e0f37b-46f0-4ca0-88c8-d35fca06de6f.mp4

Note the lit LED on the IR sensor (on the nozzle), indicating a constant stream of IR radiation from the lighter.

### Negative Detection (with IR interference from Remote Controller)

https://user-images.githubusercontent.com/59714253/177892569-114a93c2-2078-4daf-9dea-9b6d85c27205.mp4

Note the flickering LED on the IR sensor as it is receiving a pulse of IR radiation from the remote controller.

### Video from Demo Day!

https://user-images.githubusercontent.com/59714253/177893559-98bff813-416a-4662-b5bf-f5625fd59094.mp4



