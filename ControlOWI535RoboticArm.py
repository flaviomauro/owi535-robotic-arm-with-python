# *******************************************************************************
# Description:
# Sample code to control OWI-535 Robotic Arm Edge with its OWI-535-USB USB Interface
#   using python
# GitHub: https://github.com/flaviomauro/OWI-535-Robotic-Arm-with-Python
# *******************************************************************************
# Item list:
#
# - 1 x OWI-535 Robotic Arm Edge
# - 1 x OWI-535-USB USB Interface For Robotic Arm Edge
#
# External Library list:
# - PyUSB - "http://sourceforge.net/projects/pyusb/"
# - libusb
#   - Linux: libusb-1.0.9 - "http://libusb.org/"
#   - Windows: libusb-win32 - https://sourceforge.net/projects/libusb-win32/
# *******************************************************************************
# @author: Flavio H. C. Mauro
# @date:   22-Jan-2017
# LinkedIn: https://br.linkedin.com/in/flaviomauro
# *******************************************************************************

import usb
import usb.core
import usb.util
import time

# find Robotic Arm USB device (please note that you need to setup it first using libusb)
robotArm = usb.core.find(idVendor=0x1267, idProduct=0x000)

# Check if the arm is detected and warn if not
if robotArm is None:
    raise ValueError("OWI-535 robot arm not found!")
else:
    print "OWI-535 robot arm is ready."


M1_CLOSE = [1, 0, 0]
M1_OPEN = [2, 0, 0]
M2_UP = [4, 0, 0]
M2_DOWN = [8, 0, 0]
M3_UP = [16, 0, 0]
M3_DOWN = [32, 0, 0]
M4_BACK = [64, 0, 0]
M4_FORWARD = [128, 0, 0]
M5_CLOCKWISE = [0, 2, 0]
M5_ANTI_CLOCKWISE = [0, 1, 0]
LED_ON = [0, 0, 1]
LED_OFF = [0, 0, 0]


# Define a procedure to prepare the movement and/or LED command so we can deal with multiple motors at the same time
def get_arm_command(movements):
    result = [0, 0, 0]

    for movement in movements:
        for i in xrange(len(result)):
            result[i] = result[i] + movement[i]
    print "Arm command: "
    print result
    return result


# Define a procedure to execute the movement and/or LED command
def move_arm(duration, arm_command):
    # Start moving the arm or switch the led
    robotArm.ctrl_transfer(0x40, 6, 0x100, 0, arm_command, 3)

    # Stop moving the arm or switch the led after waiting a specified ammount of time
    time.sleep(duration)
    arm_command = [0, 0, 0]
    robotArm.ctrl_transfer(0x40, 6, 0x100, 0, arm_command, 3)


# Define a procedure to test the arm movements and led, both single and multiple movements
def test_arm():

    # Test each movement and LED light
    movement_list = [M1_OPEN, M1_CLOSE, M2_UP, M2_DOWN, M3_UP, M3_DOWN, M4_BACK, M4_FORWARD, M5_CLOCKWISE,
                     M5_ANTI_CLOCKWISE, LED_ON, LED_OFF]
    for movement in movement_list:
        move_arm(1, movement)
        time.sleep(1)

    # Test Multiple movements and LED light
    move_arm(1, get_arm_command([M1_OPEN, M2_DOWN, M3_DOWN, M4_FORWARD, M5_ANTI_CLOCKWISE, LED_ON]))
    time.sleep(1)

    # Test Multiple movements and LED light
    move_arm(1, get_arm_command([M1_CLOSE, M2_UP, M3_UP, M4_BACK, M5_CLOCKWISE, LED_OFF]))
    time.sleep(1)


test_arm()
