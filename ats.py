#
# A simple script for taking data with the ATS. 
#
from org.lsst.ccs.scripting import *
from org.lsst.ccs.bus.states import AlertState
from datetime import date
from optparse import OptionParser
from org.lsst.ccs.subsystem.rafts.fpga.compiler import FPGA2ModelBuilder
from java.io import File
import time
from org.lsst.ccs.utilities.image.samp import SampUtils
from java.io import File

CCS.setThrowExceptions(True)

# Directory where output will be written

dataDir = "/data/ats/"+str(date.today())

# Parse command line options

parser=OptionParser()
parser.add_option("-e","--exp",dest="expose")
parser.add_option("-d","--dark",dest="dark")
parser.add_option("-s","--sequencer",dest="sequencer")
parser.add_option("-9","--ds9", action="store_true", dest="ds9")
(options, args) = parser.parse_args()

exposure = float(options.expose or 2)
dark = float(options.dark or 0)
if dark>0:
  exposure = 0

# Connect to subsystems
raftsub = CCS.attachSubsystem("ats-wreb")
powersub = CCS.attachSubsystem("ats-power")
bonnsub = CCS.attachSubsystem("bonn-shutter")

# Load the sequencer

if options.sequencer:
   compiler = FPGA2ModelBuilder()
   file = File(options.sequencer)
   model = compiler.compileFile(file)
   raftsub.sendSynchCommand("loadCompiledSequencer",model,file.getName())
   print "Loaded %s" % file

# Sanity checks

biasOn = raftsub.sendSynchCommand("isBackBiasOn")
if not biasOn:
  print "WARNING: Back bias is not on for WREB"

alerts = raftsub.sendSynchCommand("getRaisedAlertSummary")
if alerts.alertState!=AlertState.NOMINAL:
  print "WARNING: WREB subsystem is in alarm state %s" % alerts.alertState 

print "Clearing CCD "
raftsub.sendSynchCommand("setSequencerStart","Clear")
raftsub.sendSynchCommand("startSequencer")
raftsub.sendSynchCommand(100, "waitSequencerDone",30000)

raftsub.sendSynchCommand("setExposureTime",exposure)

if exposure>0:
   print "Exposing for %g seconds" % exposure
   bonnsub.sendSynchCommand("takeExposure",exposure)
   bonnsub.sendSynchCommand((int) (exposure+10),"waitForExposure")
 
fname = "ats_exp_%g_${timestamp}.fits" % exposure
raftsub.sendSynchCommand("setFitsFileNamePattern",fname)

if dark>0:
   print "Dark for %g seconds" % dark
   time.sleep(dark)
   fname = "ats_dark_%g_${timestamp}.fits" % dark
   raftsub.sendSynchCommand("setFitsFileNamePattern",fname)

print "Reading out"
raftsub.sendSynchCommand("setSequencerStart","ReadFrame")
raftsub.sendSynchCommand("acquireImage")
raftsub.sendSynchCommand(20, "waitForImage",10000)
result = raftsub.sendSynchCommand("saveFitsImage",dataDir)
print "Saved FITS image to %s/%s" % (dataDir,result[0])

if options.ds9:
  su = SampUtils("ats",True)
  file = File("%s/%s" % (dataDir,result[0]))
  su.display(file)
  # Kirk's favorite ds9 options
  su.ds9Set("scale scope local", None, 1000)
  su.ds9Set("scale zscale", None, 1000)
  su.ds9Set("color b", None, 1000) 

