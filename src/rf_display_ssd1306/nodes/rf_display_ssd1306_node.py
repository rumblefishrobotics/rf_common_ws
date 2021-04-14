#!/usr/bin/env python3
"""
    display_ssd1306 provides a ROS wrapper for the SSD1306 LED, using the
    Adafruit drivers for their display. It provides four lines of text,
    stacked one above the other. Each line has up to 32 characters.
"""
import time
import subprocess

import rospy

from PIL import Image, ImageDraw, ImageFont
from rf_display.msg import RFDisplayData

from board import SCL, SDA
import busio

import adafruit_ssd1306

#-------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------
RF_DISPLAY_WIDTH = 128
RF_DISPLAY_HEIGHT = 32

#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------
def shutdown_hook():
    """Clear the display on shutdown."""
    global g_draw
    # Clear the display
    g_display.fill(0)
    g_display.show()

def init_display():
    """Startup initilization of display."""
    global g_i2c
    global g_display
    global g_draw
    global g_image
    global g_font

    g_i2c = busio.I2C(SCL, SDA)
    g_display = adafruit_ssd1306.SSD1306_I2C(RF_DISPLAY_WIDTH,
                                             RF_DISPLAY_HEIGHT, g_i2c)

    # Clear the display
    g_display.fill(0)
    g_display.show()

    # Create a blank image for drawing
    width = g_display.width
    height = g_display.height
    g_image = Image.new("1", (width, height))

    # Draw a filled box to clear the image
    g_draw = ImageDraw.Draw(g_image)
    g_draw.rectangle((0, 0, width, height), outline=0, fill=0)


    g_font = ImageFont.load_default()

def display_callback(display_data):
    """Pushes incomming data to display onto display"""
    rospy.loginfo("(%s) heard: (%s),(%s),(%s),(%s)" % (rospy.get_name(),
                                                       display_data.screen_line1,
                                                       display_data.screen_line2,
                                                       display_data.screen_line3,
                                                       display_data.screen_line4))
    g_draw.rectangle((0, 0, RF_DISPLAY_WIDTH, RF_DISPLAY_HEIGHT),
                     outline=0, fill=0)
    top = -2

    g_draw.text((0, top +  0), display_data.screen_line1, font=g_font, fill=255)
    g_draw.text((0, top +  8), display_data.screen_line2, font=g_font, fill=255)
    g_draw.text((0, top + 16), display_data.screen_line3, font=g_font, fill=255)
    g_draw.text((0, top + 24), display_data.screen_line4, font=g_font, fill=255)

    g_display.image(g_image)
    g_display.show()

def listen_for_messages():
    """Creates ROS display node and starts listening for data to display."""
    init_display()

    rospy.init_node("rf_display_ssd1306_node")
    #(topic),(custom message name),(name of callback function)
    rospy.Subscriber("rf_display_ssd1306_topic",
                     RFDisplayData,
                     display_callback)
    rospy.spin()

    # Register the ROS shutdown hook
    # rospy.on_shutdown(shutdown_hook)
    
#-------------------------------------------------------------------------------
# Startup source singleton
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    try:
        listen_for_messages()
    except rospy.ROSInterruptException:
        pass
