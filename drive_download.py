# Copyright 2016-2019 California Institute of Technology.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#! /usr/bin/env python
#
# a skeleton script to download datset files from PODAAC Drive.
#
#
#   2019.12.20  Y. Jiang, version 0
#
##################################
# user parameters to be editted: #
##################################
#
# Caution: This is a Python script, and Python takes indentation seriously.
# DO NOT CHANGE INDENTATION OF ANY LINE BELOW!
#
# Here you set the input parameters:
#   -u = PO.DAAC Drive-specific login credential ("LOGIN:PASSWD")
#   -s = start date ("yyyymmdd")
#   -f = end date ("yyyymmdd")
#   -x = dataset shortname
#   -t = curl or wget command to be used in download
#
# Example:
# % ./drive_download.py -u USERNAME:PASSWORD -s 20100101 -t curl -f 20100201 -x MUR25-JPL-L4-GLOB-v04.2
# Download the data files from PODAAC Drive from 1 Jan 2010 to 1 Feb 2010 for dataset with shortName MUR25-JPL-L4-GLOB-v04.2

import sys,os
import time
from datetime import date, timedelta
from optparse import OptionParser
from xml.dom import minidom

if sys.version_info >= (3,0):
  import subprocess
  import urllib.request
else:
  import commands
  import urllib

#####################
# Global Parameters #
#####################
itemsPerPage = 10
PODAAC_WEB = 'https://podaac.jpl.nasa.gov'

###############
# subroutines #
###############
def yearday(day,month,year):
  months=[0,31,28,31,30,31,30,31,31,30,31,30,31]
  if isLeap(year):
    months[2]=29
  for m in range(month):
    day=day+months[m]
  return(day)

def isLeap(year):
  flag = ( (year%4)==0) and ( not ( (year%100)==0 and (year%400)!=0 ))
  return(flag)

def today():
  import datetime
  todays=datetime.date.today()
  return str(todays.year)+str(todays.month).zfill(2)+str(todays.day).zfill(2)

def yesterday():
  import datetime
  yesterdays=datetime.date.today() - timedelta(days=1)
  return str(yesterdays.year)+str(yesterdays.month).zfill(2)+str(yesterdays.day).zfill(2)

# input parameters handling
def parseoptions():
  usage = "Usage: %prog [options]"
  parser = OptionParser(usage)

  parser.add_option("-u", "--login", help="user login/passwd", dest="login")
  parser.add_option("-t", "--cmd", help="curl or wget", dest="cmd")
  parser.add_option("-x", "--shortname", help="product short name", dest="shortname")
  parser.add_option("-s", "--start", help="start date: Format yyyymmdd (eg. -s 20140502 for May 2, 2014) [default: yesterday %default]", dest="date0", default=yesterday())
  parser.add_option("-f", "--finish", help="finish date: Format yyyymmdd (eg. -f 20140502 for May 2, 2014) [default: today %default]", dest="date1", default=today())

  # Parse command line arguments
  (options, args) = parser.parse_args()

  # print help if no arguments are given
  if(len(sys.argv) == 1):
    parser.print_help()
    exit(-1)

  if options.shortname == None:
    print('\nShortname is required !\nProgram will exit now !\n')
    parser.print_help()
    exit(-1)

  return( options )

#############
# Main Code #
#############
def standalone_main():
  # get command line options:

  options=parseoptions()

  shortname = options.shortname
  login = options.login
  cmd = options.cmd

  date0 = options.date0
  if options.date1==-1:
    date1 = date0
  else:
    date1 = options.date1

  if len(date0) != 8:
    sys.exit('\nStart date should be in format yyyymmdd !\nProgram will exit now !\n')

  if len(date1) != 8:
    sys.exit('\nEnd date should be in format yyyymmdd !\nProgram will exit now !\n')

  year0=date0[0:4]; month0=date0[4:6]; day0=date0[6:8];
  year1=date1[0:4]; month1=date1[4:6]; day1=date1[6:8];

  timeStr = '&startTime='+year0+'-'+month0+'-'+day0+'&endTime='+year1+'-'+month1+'-'+day1

  print ('\nPlease wait while program searching for the granules ...\n')

  wsurl = PODAAC_WEB+'/ws/search/granule/?shortName='+shortname+'&itemsPerPage=1&sortBy=timeAsc&format=atom'
  if sys.version_info >= (3,0):
    response = urllib.request.urlopen(wsurl)
  else:
    response = urllib.urlopen(wsurl)
  data = response.read()

  if (len(data.splitlines()) == 1):
    sys.exit('No granules found for dataset: '+shortname+'\nProgram will exit now !\n')

  #************************************************************************************
  if sys.version_info >= (3,0):
    r=input('OK to download?  [yes or no]: ')
  else:
    r=raw_input('OK to download?  [yes or no]: ')
  if len(r)==0 or (r[0]!='y' and r[0]!='Y'):
    print ('... no download')
    sys.exit(0)

  # main loop:
  start = time.time()
  bmore = 1
  while (bmore > 0):
   if (bmore == 1):
       urllink = PODAAC_WEB+'/ws/search/granule/?shortName='+shortname+timeStr+'&itemsPerPage=%d&sortBy=timeAsc'%itemsPerPage+'&format=atom'
   else:
       urllink = PODAAC_WEB+'/ws/search/granule/?shortName='+shortname+timeStr+'&itemsPerPage=%d&sortBy=timeAsc&format=atom&startIndex=%d'%(itemsPerPage, (bmore-1)*itemsPerPage)
   bmore = bmore + 1
   if sys.version_info >= (3,0):
     response = urllib.request.urlopen(urllink)
   else:
     response = urllib.urlopen(urllink)
   data = response.read()
   doc = minidom.parseString(data)

   numGranules = 0
   for arrays in doc.getElementsByTagName('link'):
    names = arrays.getAttribute("title")
    if names == 'HTTP URL':
      numGranules = numGranules + 1
      datafile = arrays.getAttribute("href")
      if datafile.split(".")[-1] != "nc":
        continue
      if cmd == 'curl':
        fcmd='curl -u '+login+' -O '+ datafile
      elif cmd == 'wget':
        fcmd='wget --user='+login.rsplit( ":", 1 )[ 0 ]+' --password='+login.rsplit( ":", 1 )[ 1 ]+ ' ' +datafile
      else:
        sys.exit('\nThe script will need curl or wget on the system, please install them first before running the script !\nProgram will exit now !\n')

      os.system( fcmd )
      print (datafile + ' download finished !')

   if numGranules < itemsPerPage:
     bmore = 0

  end = time.time()
  print ('Time spend = ' + str(end - start) + ' seconds')

if __name__ == "__main__":
        standalone_main()