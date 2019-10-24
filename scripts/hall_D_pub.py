#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32, Int16MultiArray
from rosserial_arduino.msg import Adc
import matplotlib.pyplot as plt
from drawnow import *
import numpy as np

X_t = np.array([])
X_size = 100
numSensor = 10
nIter = 0
hallDefault = 0

def init_X():
	global X_t
	global X_size
	global numSensor
	X_t = 100*np.ones(numSensor)
	for i in range(X_size -1):
		temp = 100*np.ones(numSensor)
		X_t = np.vstack((X_t,temp))

init_X()

def getDefaultHall(X_t):
	print np.average(X_t, axis = 0)
	return np.average(X_t, axis = 0)


def callback(data):
	global X_t
	global nIter
	global hallDefault
	temp = np.array((data.data))
	X_t = np.vstack((X_t,temp))
	X_t = X_t[1:]
	
	if nIter == X_size + 1:
		hallDefault = getDefaultHall(X_t)
	if nIter > X_size +10:
		D = int(np.linalg.norm(X_t[-1] - hallDefault))
		D_pub.publish(data = D)
		# print X_t.shape

	nIter = nIter + 1

	
if __name__ == '__main__':
	
	rospy.init_node('listener', anonymous=True)
	rate = rospy.Rate(50)

	rospy.Subscriber("/arduino_green/hall_sensor", Int16MultiArray, callback)
	D_pub = rospy.Publisher('/arduino_blue/D_pub', Int32, queue_size = 1)
	while not rospy.is_shutdown():
		rate.sleep()
