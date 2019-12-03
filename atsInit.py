#!/usr/bin/env ccs-script
#
# A simple script for initializing the ATS using Stuart's approved procedure 
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
if dphiOn:
   raise RuntimeError("DPHI must be off to run this script")
hvOn = powersub.sendSynchCommand("isHvBiasOn")
if hvOn:
   raise RuntimeError("HVBias must be off to run this script")

raftsub.sendSynchCommand("loadAspics", True)
raftsub.sendSynchCommand("loadSequencer", "/lsst/ccs/sequences/ats-2s-v7.seq")

ccdType = raftsub.sendSynchCommand("WREB getCcdType")
if ccdType.toString() != "ITL":
   raise RuntimeError("Invalid CCDType %s" % ccdType)

register = raftsub.sendSynchCommand("WREB getRegister 0x100000 1")
print register


raftsub.sendSynchCommand("WREB setCCDClocksLow")

register = raftsub.sendSynchCommand("WREB getRegister 0x100000 1")
print register

raftsub.sendSynchCommand("loadConfiguration Limits:pd_20190523 Rafts:pi_20190816 RaftsLimits:pd_20190523")

raftsub.sendSynchCommand(Duration.ofSeconds(300), "WREB testCCDShorts")
dphiOn = powersub.sendSynchCommand("dphiOn")
raftsub.sendSynchCommand(Duration.ofSeconds(300), "WREB powerCCDsOn")




# restore register
raftsub.sendSynchCommand("WREB setRegister 0x100000 [0x3d4]")
register = raftsub.sendSynchCommand("WREB getRegister 0x100000 1")
print register

