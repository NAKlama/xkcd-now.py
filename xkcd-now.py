#!/usr/bin/python
#
# Name:     xkcd-now.py
# Author:   Frederik Klama
# License:  GPL v3 (see included LICENSE file)
#
# This work was inspired by XKCD Comic 1335
# http://xkcd.com/1335/
#
# Credit goes to Randall Munroe for the pictures this script displays
#

from sys import exit
from datetime import datetime, timedelta
from os import system, mkdir
import os.path as path
import argparse

useurllib3 = False

try:
  import urllib3
  useurllib3 = True
except:
  pass

pict_dir   = ""                 # Change this to an existing directory to override default
viewer     = "/usr/bin/qiv"     # Path to image viewer binary (only qiv tested)
viewer_opt = ""                 # Optional options to image viewer (not tested)
wget_bin   = "/usr/bin/wget"    # Only needed when urllib3 is not installed

# URL to images for XKCD Comic 1335
pict_url   = "http://imgs.xkcd.com/comics/now/"


def checkPicture(pict_dir, h, m):
  # Check if file exists in cache directory, fetching it if it does not exist
  # returint absolute path

  # Generate two digit Strings for quater hour and minute
  q   = m  - (m % 15)
  H   = "%02i" % h
  M   = "%02i" % q

  # Use ~/.xkcd-now by default
  if not pict_dir:
    pict_dir = path.expanduser("~/.xkcd-now")
    if not path.exists(pict_dir):
      mkdir(pict_dir)

  # Check if caching directory exists
  if not path.isdir(pict_dir):
    print("Please adjust the 'pict_dir' variable in the script to match your setup.")
    exit()

  # Generate path to picture
  pict_file = "%sh%sm.png" % (H, M)
  picture   = path.join(pict_dir, pict_file)

  # Check if local picture exists. Download if not.
  url  = pict_url + pict_file
  if not path.isfile(picture) and useurllib3:
    http = urllib3.PoolManager()
    r    = http.request('GET', url)
    if r.status == 200:
      of = open(picture, "wb")
      of.write(r.data)
      of.close()
    elif r.status == 404:
      print("404: ", url)
    else:
      print("Error downloading picture: Status =", r.status)
      exit()
  elif not path.isfile(picture):
    cmd = wget_bin + " -O " + pict_dir + "/" + pict_file + " " + url
    system(cmd)

  return picture


def checkAll(pict_dir):
  # Run through all possible times and 'check' each. Will only fetch missing
  # pictures
  for h in range(24):
    for m in range(0, 60, 15):
      checkPicture(pict_dir, h, m)


def displayPicture(path):
  # Display the picture in 'path' using the configured viewer

  # Generate and execute command to display picture
  cmd = viewer + " "
  if viewer_opt:
    cmd += viewer_opt + " "
  cmd += picture

  # print picture
  system(cmd)


def getAdjustedTime():
  # Get current GMT time, add 7 minutes and 12h and round to quater hour
  #  7 minutes for rounding to the nearest quater hour
  # 12 hours due to the offset of the image names relative to GMT
  now = datetime.utcnow()
  delta = timedelta(0,0,0,0,7,12)
  now += delta
  return (now.hour, now.minute)


if __name__ == '__main__':
  # Parse arguments
  argParser = argparse.ArgumentParser(description="xkcd-now.py")
  argParser.add_argument('--all', '-a',
    action='store_true',
    help="Download all pictures that are missing. (Takes a bit longer)")
  args = vars(argParser.parse_args())

  if pict_dir:
    pict_dir = path.abspath(path.expanduser(pict_dir))

  if args['all']:
    checkAll(pict_dir)

  # Get adjusted time
  (h, m) = getAdjustedTime()

  # Get path of picture file
  picture = checkPicture(pict_dir, h, m)

  # Display picture
  displayPicture(picture)
