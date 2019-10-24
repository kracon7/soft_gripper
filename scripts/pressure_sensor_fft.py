#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
from rosserial_arduino.msg import Adc
import matplotlib.pyplot as plt
from drawnow import *
import numpy as np

X_t = []
X_size = 200

nSec = 0.1
nSec_prev = 0.0
dXdt = 0.0

def init_X():
	global X_t
	for i in range(X_size):
		X_t.append(float(100))

init_X()

def Gauss_filter():
	return np.array(1/17 * [1,4,7,4,1])

# def Smoothing(window_len = 5, filter_g):
# 	global X_t
# 	sample = np.array(X_t(X_size-5:).append(X_t(-2:-1-ceil(X_size/2):-1)))
# 	half_wid = ceil(window_len/2)
# 	for i in range(half_wid):
# 		X_t(X_size - half_wid + i) = np.dot(sample(i:i+window_len), filter_g)

def plot_ADC_reading():
    plt.grid(True)
    plt.ylabel('X_t')
    plt.plot(X_t, 'r-')
    plt.ylim([50, 400])

plt.figure()

def callback(data):
	global X_t
	global dXdt
	X_t.append(float(data.adc0))
	X_t.pop(0)
	# drawnow(plot_ADC_reading)
	# smoothing data
	X_t[X_size-1] = 1.0/84*( 40*X_t[X_size-1] + 30*X_t[X_size-2] + 12*X_t[X_size-3] + 2* X_t[X_size-4])


	now = rospy.get_rostime()
	nSec = now.nsecs
	dXdt = (X_t[X_size-1] - X_t[X_size-2]) / (nSec - nSec_prev) * 1000000000
	print dXdt
	print '\n'

	
if __name__ == '__main__':
	
	rospy.init_node('listener', anonymous=True)
	rate=rospy.Rate(50)
	nSec_prev = rospy.get_rostime().nsecs
	rospy.Subscriber("adc", Adc, callback)
	dXdt_pub = rospy.Publisher('/dXdt_pub', Int32, queue_size = 10)
	while not rospy.is_shutdown():
		dXdt_pub.publish(data = int(dXdt))
		rate.sleep()
