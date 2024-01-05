# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       vysha                                                        #
# 	Created:      12/30/2023, 3:58:39 PM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

from vex import *

# Brain should be defined by default
brain = Brain()

# 
#
# The controller
controller = Controller()

# Drive motors
left_drive_1 = Motor(Ports.PORT11, GearSetting.RATIO_6_1, False)
left_drive_2 = Motor(Ports.PORT16, GearSetting.RATIO_6_1, False)
left_drive_3 = Motor(Ports.PORT20, GearSetting.RATIO_6_1, False)

right_drive_1 = Motor(Ports.PORT1, GearSetting.RATIO_6_1, True)
right_drive_2 = Motor(Ports.PORT6, GearSetting.RATIO_6_1, True)
right_drive_3 = Motor(Ports.PORT10, GearSetting.RATIO_6_1, True)

Flywheel = Motor(Ports.PORT19, GearSetting.RATIO_6_1, False)

# Arm and claw motors will have brake mode set to hold
# Claw motor will have max torque limited
piston1= DigitalOut(brain.three_wire_port.a)
piston2= DigitalOut(brain.three_wire_port.b)

is_piston_open = False

# Auxilary motors


# Max motor speed (percent) for motors controlled by buttons
MAX_SPEED = 80

def stop_drivetrain():
    left_drive_1.stop()
    left_drive_2.stop()
    left_drive_3.stop()
    right_drive_1.stop()
    right_drive_2.stop()
    right_drive_3.stop()

def set_wing_open():
    piston1.set(True)
    piston2.set(True)

def set_wing_close():
    piston1.set(False)
    piston2.set(False)

def move_forward(speed, duration):
    left_drive_1.spin(FORWARD, speed, PERCENT)
    left_drive_2.spin(FORWARD, speed, PERCENT)
    left_drive_3.spin(FORWARD, speed, PERCENT)
    right_drive_1.spin(FORWARD, speed, PERCENT)
    right_drive_2.spin(FORWARD, speed, PERCENT)
    right_drive_3.spin(FORWARD, speed, PERCENT)
    sleep(duration, TimeUnits.MSEC)
    stop_drivetrain()
def move_Right(speed, duration):
    left_drive_1.spin(FORWARD, speed, PERCENT)
    left_drive_2.spin(FORWARD, speed, PERCENT)
    left_drive_3.spin(FORWARD, speed, PERCENT)
    right_drive_1.spin(REVERSE, speed, PERCENT)
    right_drive_2.spin(REVERSE, speed, PERCENT)
    right_drive_3.spin(REVERSE, speed, PERCENT)
    sleep(duration, TimeUnits.MSEC)
    stop_drivetrain()
def move_left(speed, duration):
    left_drive_1.spin(REVERSE, speed, PERCENT)
    left_drive_2.spin(REVERSE, speed, PERCENT)
    left_drive_3.spin(REVERSE, speed, PERCENT)
    right_drive_1.spin(FORWARD, speed, PERCENT)
    right_drive_2.spin(FORWARD, speed, PERCENT)
    right_drive_3.spin(FORWARD, speed, PERCENT)
    sleep(duration, TimeUnits.MSEC)
    stop_drivetrain()

def move_back(speed, duration):
    left_drive_1.spin(REVERSE, speed, PERCENT)
    left_drive_2.spin(REVERSE, speed, PERCENT)
    left_drive_3.spin(REVERSE, speed, PERCENT)
    right_drive_1.spin(REVERSE, speed, PERCENT)
    right_drive_2.spin(REVERSE, speed, PERCENT)
    right_drive_3.spin(REVERSE, speed, PERCENT)
    sleep(duration, TimeUnits.MSEC)
    stop_drivetrain()

def autonomous():
    stop_drivetrain()
    brain.screen.clear_screen()
    brain.screen.print("Aton Program running")
    wait(1, SECONDS)
    move_back(100,700) 
    move_left(50,300)
    move_forward(50,900)
    move_left(25,700)
    set_wing_open()
    wait(500)
    move_left(80,600)
    set_wing_close()
    wait(500)
    move_left(50,550)
    move_forward(50,1000)
    wait(500)
    move_forward(25,200)
   

def pre_autonomous():
    brain.screen.clear_screen()
    brain.screen.print("Pre Aton program running")
    wait(1, SECONDS)




#
# All motors are controlled from this function which is run as a separate thread
#
def drive_task():
    drive_left = 0
    drive_right = 0

    set_wing_close()
    is_piston_open = False 

    controller.buttonL1.pressed(set_wing_open)
    controller.buttonL2.pressed(set_wing_close)
    # setup the arm motor
    # loop forever
    while True:
        
        # joystick tank control
        drive_right = controller.axis3.position()
        drive_left = controller.axis2.position()

        
        # threshold the variable channels so the drive does not
        # move if the joystick axis does not return exactly to 0
        deadband = 23
        if abs(drive_left) < deadband:
            drive_left = 0
        if abs(drive_right) < deadband:
            drive_right = 0

        # Now send all drive values to motors

        # The drivetrain
        left_drive_1.spin(FORWARD, drive_left, PERCENT)
        left_drive_2.spin(FORWARD, drive_left, PERCENT)
        left_drive_3.spin(FORWARD, drive_left, PERCENT)
        
        right_drive_1.spin(FORWARD, drive_right, PERCENT)
        right_drive_2.spin(FORWARD, drive_right, PERCENT)
        right_drive_3.spin(FORWARD, drive_right, PERCENT)

        #The Flywheel
        if controller.buttonR1.pressing() == True:
            Flywheel.spin(FORWARD, MAX_SPEED, PERCENT)
        else:
            Flywheel.stop()
        sleep(10)

# Run the drive code
#drive = Thread(drive_task)

# Python now drops into REPL
comp = Competition(drive_task, autonomous)
pre_autonomous()
set_wing_close()
        
