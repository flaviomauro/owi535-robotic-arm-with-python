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
# @date:   29-Jan-2017
# @version: 1.1
# LinkedIn: https://br.linkedin.com/in/flaviomauro
# *******************************************************************************


import sys
import argparse
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
def get_arm_command(unique_durations, raw_durations, raw_commands):

    result = [[None for y in range(2)] for x in range(len(unique_durations))]

    for i, udVal in enumerate(unique_durations):
        result[i][0] = udVal
        result[i][1] = [0, 0, 0]

    for i, udVal in enumerate(unique_durations):
        for j, rdVal in enumerate(raw_durations):
            if udVal == rdVal:
                for z, item in enumerate(result[i][1]):
                    raw_commands[j] = raw_commands[j].replace('[', '')
                    raw_commands[j] = raw_commands[j].replace(']', '')
                    result[i][1][z] = result[i][1][z] + map(int, raw_commands[j].split(','))[z]
    return result


def get_unique_durations(raw_duration):
    duration_set = set(raw_duration)
    duration = list(duration_set)

    return duration


# Define a procedure to execute the movement and/or LED command
def move_arm(raw_durations, raw_commands):

    if len(raw_durations) != len(raw_commands):
        print 'Please provide the same number of items for durations and movements arrays.'
        print 'duration array length: ' + str(len(raw_durations))
        print 'duration array items: ' + str(raw_durations)
        print 'movements array length: ' + str(len(raw_commands))
        print 'movements array items: ' + str(raw_commands)
    else:

        unique_durations = get_unique_durations(raw_durations)
        arm_commands = get_arm_command(unique_durations, raw_durations, raw_commands)

        for arm_command in arm_commands:
            # Start moving the arm or switch the led
            robotArm.ctrl_transfer(0x40, 6, 0x100, 0, arm_command[1], 3)
            time.sleep(arm_command[0])

            # Stop moving the arm
            robotArm.ctrl_transfer(0x40, 6, 0x100, 0, [0, 0, 0], 3)


def main(argv):
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--d', type=str)
        parser.add_argument('--m', type=str)
        args = parser.parse_args()

        durations = args.d.split('-')
        durations = map(int, durations)

        raw_movements = args.m.split('-')
        raw_movements = [w.replace('M1_CLOSE', '[1, 0, 0]') for w in raw_movements]
        raw_movements = [w.replace('M1_OPEN', '[2, 0, 0]') for w in raw_movements]
        raw_movements = [w.replace('M2_UP', '[4, 0, 0]') for w in raw_movements]
        raw_movements = [w.replace('M2_DOWN', '[8, 0, 0]') for w in raw_movements]
        raw_movements = [w.replace('M3_UP', '[16, 0, 0]') for w in raw_movements]
        raw_movements = [w.replace('M3_DOWN', '[32, 0, 0]') for w in raw_movements]
        raw_movements = [w.replace('M4_BACK', '[64, 0, 0]') for w in raw_movements]
        raw_movements = [w.replace('M4_FORWARD', '[128, 0, 0]') for w in raw_movements]
        raw_movements = [w.replace('M5_CLOCKWISE', '[0, 2, 0]') for w in raw_movements]
        raw_movements = [w.replace('M5_ANTI_CLOCKWISE', '[0, 1, 0]') for w in raw_movements]
        raw_movements = [w.replace('LED_ON', '[0, 0, 1]') for w in raw_movements]
        raw_movements = [w.replace('LED_OFF', '[0, 0, 0]') for w in raw_movements]
    except:
        print 'ControlOWI535RoboticArm.py --d =<duration array> --m=<movements array>'
        print 'ControlOWI535RoboticArm.py --d[1]" --m=[M1_CLOSE]'
        print 'ControlOWI535RoboticArm.py --d=1-2-1-3-2 --m=M1_CLOSE-M2_UP-M3_UP-M4_BACK-M5_CLOCKWISE'
        print sys.exc_info()[0]
        raise

    move_arm(durations, raw_movements)


if __name__ == "__main__":
    main(sys.argv[1:])
