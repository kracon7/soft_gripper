#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
from rosserial_arduino.msg import Adc
import matplotlib.pyplot as plt
from drawnow import *
import numpy as np

X_t = []
X_size = 600

nSec = 0.1
nSec_prev = 0.0
Sec_prev = 0
dXdt = 0.0
toggle_track = False

init_pressure = 0
max_pressure = 0
pressure_default = 1023
track_cycle = 0

def init_X():
	global X_t
	for i in range(X_size):
		X_t.append(float(100))

init_X()


def callback(data):
	global X_t
	global dXdt
	global Sec_prev
	global max_pressure
	global pressure_default
	global toggle_track
	global track_cycle
	X_t.append(float(data.adc0))
	X_t.pop(0)
	# drawnow(plot_ADC_reading)
	# smoothing data
	X_t[X_size-1] = 1.0/84*( 40*X_t[X_size-1] + 30*X_t[X_size-2] + 12*X_t[X_size-3] + 2* X_t[X_size-4])


	now = rospy.get_rostime()
	Sec = now.secs
	nSec = now.nsecs
	
	if Sec - Sec_prev > 2 and Sec - Sec_prev < 4:
		pressure_default = np.average(np.array(X_t))
		print 'The default pressure reading is: \n'
		print pressure_default
		print '\n\n Press the balloon\n'
		Sec_prev = -5

	if X_t[X_size-1] - pressure_default >= 3:
		
		toggle_track = True

	if track_cycle == 1:
		print '\n\n***********************************\nYou just pressed it\n'


	if toggle_track and track_cycle <  X_size:
		max_pressure = np.max(np.array(X_t))
		track_cycle = track_cycle +1
	elif toggle_track and track_cycle == X_size:
		track_cycle = 0
		toggle_track = False
		pressure_default = np.average(np.array(X_t[-10:-1]))
		print 'The press reading just now is:'
		print max_pressure - pressure_default
		print '\n\n\n'






	
if __name__ == '__main__':
	
	rospy.init_node('listener', anonymous=True)
	rate=rospy.Rate(50)
	nSec_prev = rospy.get_rostime().nsecs
	Sec_prev = rospy.get_rostime().secs


	rospy.Subscriber("adc", Adc, callback)
	dXdt_pub = rospy.Publisher('/dXdt_pub', Int32, queue_size = 10)
	while not rospy.is_shutdown():
		dXdt_pub.publish(data = int(dXdt))
		rate.sleep()
