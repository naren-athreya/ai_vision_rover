import machine
import sys
import uselect as select
import time

# Motor Setup for DRV8833
# Left Motor (IN1, IN2)
left_in1 = machine.PWM(machine.Pin(10))
left_in2 = machine.PWM(machine.Pin(11))
# Right Motor (IN3, IN4)
right_in3 = machine.PWM(machine.Pin(14))
right_in4 = machine.PWM(machine.Pin(15))

# Initialize PWM frequency and set to 0
for p in [left_in1, left_in2, right_in3, right_in4]:
    p.freq(1000)
    p.duty_u16(0)

# Power Level: 50000 (approx 76% duty cycle)
SPEED = 50000 

def move(l1, l2, r3, r4):
    left_in1.duty_u16(l1)
    left_in2.duty_u16(l2)
    right_in3.duty_u16(r3)
    right_in4.duty_u16(r4)

# Setup the poll object for non-blocking Serial
poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)

print("Pico W: DRV8833 Ready. Listening for commands...")

while True:
    if poll_obj.poll(0):
        cmd = sys.stdin.read(1).lower()
        
        if cmd == 'f':
            move(SPEED, 0, SPEED, 0) # Forward
        elif cmd == 'b':
            move(0, SPEED, 0, SPEED) # Backward
        elif cmd == 'l':
            move(0, SPEED, SPEED, 0) # Left Pivot
        elif cmd == 'r':
            move(SPEED, 0, 0, SPEED) # Right Pivot
        elif cmd == 's':
            move(0, 0, 0, 0)         # Stop
            
    time.sleep(0.01)
