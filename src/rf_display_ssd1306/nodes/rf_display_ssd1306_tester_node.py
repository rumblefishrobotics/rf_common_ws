#!/usr/bin/env python3
""" 
    Node generating test messages for the display node. Could just use
    rostopic pub to rf_display/rf_display_topic RFDisplayData <payload>,
    but payload is a fair bit to keep typing / editing. This node is
    purely a testing tool. 
"""

import rospy
#from std_msgs.msg import String
from rf_display.msg import RFDisplayData

def publish_rf_display_messages():
    # topic, message type, queue size
    pub = rospy.Publisher('rf_display_ssd1306_topic',
                          RFDisplayData, queue_size=10)

    rospy.init_node('rf_display_ssd1306_tester_node', anonymous=True)
    rate = rospy.Rate(0.2) # 0.2 hz

    # create custom message
    display_msg = RFDisplayData()

    count = 0
    while not rospy.is_shutdown():
        count = count + 1

        # Count just adds some changing text, on each line, with each message
        display_msg.screen_line1 = "line 1 (%s)" % count
        display_msg.screen_line2 = "line 2 (%s)" % count
        display_msg.screen_line3 = "line 3 (%s)" % count
        display_msg.screen_line4 = "line 4 (%s)" % count

        rospy.loginfo(display_msg)
        pub.publish(display_msg)
        rate.sleep()
 
if __name__ == '__main__':
    try:
        publish_rf_display_messages()
    except rospy.ROSInterruptException:
        pass
    



    
