# AI-Vision Semi-Autonomous Rover
## This is a Raspberry Pi 5 and Pi Pico W based system which has human detecttion and automatic braking features.

## Project Overview
Our project aims to provide a low-cost and high speed solution for human detection in live disaster/military surveillance systems using off-shelf components. 

## Hardware
Our system has a unique methodology composed of 2 processors, a Raspberry Pi 5 for AI vision processing and a Pico W to take commands from pi 5 feed and give signals to the DRV8833 motor driver.
The list of components used is:
1. Raspberry Pi 5(8gb RAM)
2. Geekworm X1202 - UPS hat with constant 5.1V 5A power to pi 5 via pogo pins, allowing pi 5 to operate at maximum compute capabilities wirelessly. It uses 
3. Pi 5 cooling module - a heat sink coupled coolong fan to keep processor in pi 5 at optimum temperatures.
4. Pico W - a microcontroller that takes serial inputs from pi 5 and generates signals for the motor driver.
5. DRV8833 - a dual H-bridge N-channel MOSFET based motor driver with built-in PWM generation with an effeciency of 92-95%.
6. Two 18650 Li-ion cells in series to power the motors via Vcc on DRV8833.
7. A treaded-wheel chassis with an aluminium frame for robust operations.
The image shown below is of the assembled rover:
<img width="480" height="540" alt="image" src="https://github.com/user-attachments/assets/b287b833-1c31-43eb-9eca-1f70fe9f23ec" />

## System Architecture
<img width="580" height="480" alt="image" src="https://github.com/user-attachments/assets/f8423339-afd1-4bc1-94ee-06940bb4e1c5" />

## Block Diagram
<img width="580" height="480" alt="image" src="https://github.com/user-attachments/assets/c5c56563-520f-4b5a-aae9-f2e0566bb2f2" />
