#!/usr/bin/env ccs-script
#
# A simple script for turning off the ATS  
#
from org.lsst.ccs.scripting import *
from org.lsst.ccs.bus.states import AlertState
from optparse import OptionParser
from org.lsst.ccs.subsystem.rafts.fpga.compiler import FPGA2ModelBuilder
from java.io import File
import time
from org.lsst.ccs.utilities.image.samp import SampUtils
from java.io import File
from java.time import Duration

CCS.setThrowExceptions(True)

# Connect to subsystems
raftsub = CCS.attachSubsystem("ats-wreb")
powersub = CCS.attachSubsystem("ats-power")

# Check initial state
dphiOn = powersub.sendSynchCommand("isDphiOn")
hvOn = powersub.sendSynchCommand("isHvBiasOn")
hvSwitchOn = raftsub.sendSynchCommand("WREB isBackBiasOn")

if hvSwitchOn:
   print "Setting back bias switch off"
   raftsub.setSynchCommand("WREB setBackBias false")

if hvOn:
   print "Setting back bias power off"
   powersub.sendSynchCommand("hvBiasOff")
   time.sleep(1.0)

raftsub.sendSynchCommand("WREB setCCDClocksLow")
if dphiOn:
   print "Setting dphi off"
   powersub.sendSynchCommand("hvBiasOff")
   time.sleep(1.0)
   
raftsub.sendSynchCommand("WREB powerCCDsOff")

# The following could be made optional

print "Setting main power off"
powersub.sendSynchCommand("powerOff")
time.sleep(1.0)

print "Setting OTM power off"
powersub.sendSynchCommand("otmOff")
time.sleep(1.0)

print "Setting Fan power off"
powersub.sendSynchCommand("fanOff")

