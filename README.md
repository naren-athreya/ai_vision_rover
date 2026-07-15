# AI-Vision Semi-Autonomous Rover
## This is a Raspberry Pi 5 and Pi Pico W based system which has human detecttion and automatic braking features.

## Project Overview
Our project aims to provide a low-cost and high speed solution for human detection in live disaster/military surveillance systems using off-shelf components. 

## Hardware
Our system has a unique methodology composed of 2 processors, a Raspberry Pi 5 for AI vision processing and a Pico W to take commands from pi 5 feed and give signals to the DRV8833 motor driver.
The list of components used is:
1. Raspberry Pi 5(8gb RAM)
2. Geekworm X1202 - UPS hat with constant 5.1V 5A power to pi 5 via pogo pins, allowing pi 5 to operate at maximum compute capabilities wirelessly.
3. Pi 5 cooling module - a heat sink coupled coolong fan to keep processor in pi 5 at optimum temperatures.
4. Pico W - a microcontroller that takes serial inputs from pi 5 and generates signals for the motor driver.
5. 
