Code written for my multi-robot thesis project. Robot is the main control class, with an instance variable for each key subsystem (i.e Comms, Motors).

robot.py
  - Main control class, has various high level functionality functions, such as thesis experiments
  
comms.py
  - Communication module for robot. Uses socket based UDP broadcasts to transmit messages between robots. Also stores incomming messages in an inbox until read
  
IMU.py
  - Interacts with the on-board LSM303C IMU to obtain accelerometer and compass readings. Main feature is the absolute heading calculation that has a moving average filter
  
motors.py
  - Uses gpiozero to interact with a DRV8835 motor driver to implement differential drive motion.

camera.py
  - Uses PiCamera to take a stream of images from a PiCamera v1.3 while also implementing all image processing functionality (i.e. colour masking)
  
TOMLSM303C.py
  - Modified version of an LSM303 python class to interact with an LSM303C. Mainly just updates address locations and picks the correct configurations options for project.
  
colourmask.py
  - Contains colour mask values for each target
  
magoffsets.py
  - Contains robot specific compass offsets for calibration. Needs to be set per robot
