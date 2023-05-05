#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int16, Float32
from pymavlink import mavutil

from PyMavlink import ROV

def main(rov: ROV):
    pubBaseMode = rospy.Publisher('base_mode', Int16, queue_size=10)
    pubCustomMode = rospy.Publisher('custom_mode', Int16, queue_size=10)
    pubAltitude = rospy.Publisher('altitude', Float32, queue_size=10)
    pubHeading = rospy.Publisher('heading', Int16, queue_size=10)

    rospy.init_node('node_messeges', anonymous=True)

    rate = rospy.Rate(60)

    while not rospy.is_shutdown():
        message = rov.getAllMessages()
        
        try:
            if message.get_type() == 'HEARTBEAT':
                baseMode = message.base_mode
                customMode = message.custom_mode
                
                print('Base Mode', baseMode)
                print('Custom Mode', customMode)

                pubBaseMode.publish(baseMode)
                pubCustomMode.publish(customMode)
            elif message.get_type() == 'AHRS2':
                altitude = message.altitude
                
                print('Alt', altitude)

                pubAltitude.publish(altitude)
            elif message.get_type() == 'VFR_HUD':
                heading = message.heading
                
                print('Heading', heading)

                pubHeading.publish(heading)
        except:
            continue

        rate.sleep()

if __name__ == '__main__':
    master = mavutil.mavlink_connection("/dev/ttyACM0", baud=115200)
    # master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')

    rov = ROV(master)

    try:
        main(rov)
    except rospy.ROSInterruptException:
        pass