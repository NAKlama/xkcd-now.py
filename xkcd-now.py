#!/usr/bin/python
#
# Name:   xkcd-now.py
# Author: Frederik Klama
# License:  GPL v3 (see included LICENSE file)
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
import argparse
import urllib3

pict_dir   = "/home/fklama/xkcd/now"      # Change this to an existing directory
viewer     = "/usr/bin/qiv"               # Path to image viewer binary (only qiv tested)
viewer_opt = ""                           # Optional options to image viewer (not tested)

# URL to images for XKCD Comic 1335
pict_url   = "http://imgs.xkcd.com/comics/now/"


def checkPicture(pict_dir, h, m):
  # Generate two digit Strings for quater hour and minute
  q   = m  - (m % 15)
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

  return picture


def checkAll(pict_dir):
  for h in range(24):
    for m in range(0, 60, 15):
      checkPicture(pict_dir, h, m)


if __name__ == '__main__':
  argParser = argparse.ArgumentParser(description="xkcd-now.py")
  argParser.add_argument('--all', '-a',
    action='store_true',
    help="Download all pictures that are missing. (Takes a bit longer)")
  args = vars(argParser.parse_args())

  # Get current time, add 7 minutes and round to quater hour
  now = datetime.utcnow()
  delta = timedelta(0,0,0,0,7,12)
  now += delta
  h   = now.hour
  m   = now.minute

  if args['all']:
    checkAll(pict_dir)

  picture = checkPicture(pict_dir, h, m)

  # Generate and execute command to display picture
  cmd = viewer + " "
  if viewer_opt:
    cmd += viewer_opt + " "
  cmd += picture
  # print picture
  system(cmd)
