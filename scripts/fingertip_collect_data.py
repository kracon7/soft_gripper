#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32, Int16MultiArray
from rosserial_arduino.msg import Adc
import matplotlib.pyplot as plt
from drawnow import *
import numpy as np

X_t = []
X_size = 25

nSec_prev = 0

region_class = '1' # 15 class in total, 3 vertically and 5 row horizontally. 
				  #	idx goes col,row 
label = '1'
DATA_DIR = "/home/jc/research/data/0429"

print 'region_class is:'
print region_class
print '\n'
print 'region label is:'
print region_class
print '\n'

def init_X():
	global X_t
	for i in range(X_size):
		X_t.append(100)

init_X()

def write_hall(fout, data, num_sensor):
	# data is a list of all sensor reading, i.e. [adc0, adc1 ....]
	try:
		for i in range(len(data)):
			for j in range(num_sensor):
				fout.write("%d," % data[i][j])
			fout.write('\n')
	except:
		print 'File output failed. Is the file opened?'
	# for i in range(len(data)):
	# 	for j in range(num_sensor):
	# 		fout.write("%d," % data[i][j])
	# 	fout.write('\n')

def write_label(fout, label, X_size):
	try:
		for i in range(X_size):
			fout.write(label)
			fout.write('\n')
	except:
		print 'File output failed. Is the file opened?'


def callback(data):
	global X_t
	global nSec_prev
	temp = list(data.data)
	X_t.append(temp)
	X_t.pop(0)
	# print X_t
	# now = rospy.get_rostime()
	# nSec = now.nsecs
	# print 'nSec is: {}'.format(nSec/1000000)+'  nSec_prev is: {}\n'.format(nSec_prev/1000000)
	# print (nSec - nSec_prev)/1000000
	# nSec_prev = nSec

def keyboard_cb(data):
	# On keyboard, v = 118, b = 98, n = 110
	# a = 97 z = 122
	global X_t
	global X_size
	global region_class
	global label
	c = data.data
	print c
	if c is 97:
		f_data = open("{}/data_{}.txt".format(DATA_DIR, region_class), 'a')
		write_hall(f_data, X_t, 10)
		f_data.close()
		f_label = open("{}/label_{}.txt".format(DATA_DIR, region_class), 'a')
		write_label(f_label, label, X_size)
		f_label.close()
	elif c is 98:
		label = '{}'.format(int(label) + 1)
		region_class = label
		print '\n\n======================\nregion_class is:'
		print region_class
		print '\n'
		print 'region label is:'
		print region_class
		print '\n'
		print X_t[-1]
		print '\n'
		

	
if __name__ == '__main__':
	
	rospy.init_node('listener', anonymous=True)
	rate=rospy.Rate(50)
	nSec_prev = rospy.get_rostime().nsecs
	Sec_prev = rospy.get_rostime().secs


	rospy.Subscriber("hall_sensor", Int16MultiArray, callback)
	rospy.Subscriber("keyboard_pub", Int32, keyboard_cb)
	while not rospy.is_shutdown():
		rate.sleep()
