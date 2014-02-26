#!/usr/bin/python
#
# Name: 	xkcd-now.py
# Author:	Frederik Klama
# License:	GPL v3 (see included LICENSE file)
#
# This work was inspired by XKCD Comic 1335
# http://xkcd.com/1335/
#
# Credit goes to Randall Munroe for the pictures this script displays
# 

from sys import exit
from datetime import datetime, timedelta
from os import system
from time import sleep
import os.path as path
import urllib3

pict_dir   = "/home/fklama/xkcd/now"      # Change this to an existing directory 
viewer     = "/usr/bin/qiv"		# Path to image viewer binary (only qiv tested)
viewer_opt = "" 			# Optional options to image viewer (not tested)

# URL to images for XKCD Comic 1335
pict_url   = "http://imgs.xkcd.com/comics/now/"

# Get current time, add 7 minutes and round to quater hour
now = datetime.utcnow()
delta = timedelta(0,0,0,0,7,12)
now += delta
h   = now.hour
m   = now.minute
q   = m  - (m % 15)

# Generate two digit Strings for hour and minute
H   = "%02i" % h
M   = "%02i" % q

# Check if caching directory exists
if not path.isdir(pict_dir):
	print "Please adjust the 'pict_dir' variable in the script to match your setup."
	exit()

# Generate path to picture
pict_file = "%sh%sm.png" % (H, M)
picture   = path.join(pict_dir, pict_file)

# Check if local picture exists. Download if not.
if not path.isfile(picture):
	http = urllib3.PoolManager()
	url  = pict_url + pict_file
	r    = http.request('GET', url)
	if r.status == 200:
		of = open(picture, "wb")
		of.write(r.data)
		of.close()
	elif r.status == 404:
		print "404: ", url
	else:
		print "Error downloading picture: Status =", r.status
		exit()

# Generate and execute command to display picture
cmd = viewer + " "
if viewer_opt:
	cmd += viewer_opt + " "
cmd += picture
# print picture
system(cmd)

