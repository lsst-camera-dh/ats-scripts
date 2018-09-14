import time
from datetime import date

from org.lsst.ccs.scripting import *

CCS.setThrowExceptions(True)

verbose = 1

prefix = "ats"
dataDir = "/data/ats/"+str(date.today())
#seqfile = "/u1/ccs/sequences/ITL_standard_TS8_resetfirst_CL_RD_RU.seq"

#subsystem = "crtest"                 # 'crtest' for use with CR in IR2
subsystem = "ats-wreb"               # 'crtest' for use with CR in IR2
bonnshutter = "bonn-shutter"
greb     = subsystem + "/GREB"        # 
g0biases = subsystem + "/GREB.Bias0"  # 
g1biases = subsystem + "/GREB.Bias1"  #
grails   = subsystem + "/GREB.DAC"    # 
wreb     = subsystem + "/WREB"        # 
wbiases  = subsystem + "/WREB.Bias0"  # 
wrails   = subsystem + "/WREB.DAC"    # 
 
# scaling parameters for the clock voltages
pHi_gain = 0.96
pHi_offset = 0.00
pLo_gain = 0.963
pLo_offset = 0.00
sHi_gain = 0.957
sHi_offset = 0.00
sLo_gain = 0.96
sLo_offset = 0.00
rgHi_gain = 0.96
rgHi_offset = 0.00
rgLo_gain = 0.955
rgLo_offset = 0.00

OD_gain =  1.003
OD_offset = 0.00
RD_gain = 0.9942
RD_offset = 0.00
OG_gain = 1.005
OG_offset = 0.00
GD_gain = 0.994
GD_offset = 0.00

# ------ Function Definitions -------- #

def getSubsystem():
    subsys = CCS.attachSubsystem(subsystem)
    return subsys

def getRaftSubsystem(reb):
    if reb in ['wreb','w']:
        raftsub = CCS.attachSubsystem(wreb)
    elif reb in ['greb','greb0','greb1','g0','g1','g']:
        raftsub = CCS.attachSubsystem(greb)
    else:
        print 'REB type ',reb,' not recognized'
        reftsub = 0
    return raftsub
    
def getRaftBiases(reb):
    if reb in ['wreb','w']:
        raftsub = CCS.attachSubsystem(subsystem);
        board = CCS.attachSubsystem(wreb)
        biases = CCS.attachSubsystem(wbiases)
    elif reb in ['greb','greb0','g0','g']:
        raftsub = CCS.attachSubsystem(subsystem);
        board = CCS.attachSubsystem(greb)
        biases = CCS.attachSubsystem(g0biases)
    elif reb in ['greb1','g1']:
        raftsub = CCS.attachSubsystem(subsystem);
        board = CCS.attachSubsystem(greb)
        biases = CCS.attachSubsystem(g1biases)
    else:
        print 'REB type ',reb,' not recognized'
        biases = 0
    return biases
    
def getRaftRails(reb):
    if reb in ['wreb','w']:
        raftsub = CCS.attachSubsystem(subsystem);
        board = CCS.attachSubsystem(wreb)
        rails = CCS.attachSubsystem(wrails)
    elif reb in ['greb','greb0','g0','g']:
        raftsub = CCS.attachSubsystem(subsystem);
        board = CCS.attachSubsystem(greb)
        rails = CCS.attachSubsystem(grails)
    elif reb in ['greb1','g1']:
        raftsub = CCS.attachSubsystem(subsystem);
        board = CCS.attachSubsystem(greb)
        rails = CCS.attachSubsystem(grails)
    else:
        print 'REB type ',reb,' not recognized'
        rails = 0
    return rails
        
def getDataDir():
    return dataDir
    
def getPrefix():
    return prefix

def setCCD(CCDtype):
    raftsub = CCS.attachSubsystem(subsystem)
    if CCDtype in ['itl','ITL']:
        ccd = 'itl'
    elif CCDtype in ['e2v', 'E2V']:
        ccd = 'e2v'
    else:
        print 'CCD type ', CCDtype, ' not recognized'
        return    
    print 'CCD = %s' % ccd
    result = raftsub.synchCommandLine(1000,"setCcdType %s" % ccd)    
    print result.getResult()

def getCCD():
    raftsub = CCS.attachSubsystem(subsystem)
    ccdType = raftsub.synchCommandLine(1000,"getCcdType").getResult() 
    print "CCD Type = ",ccdType
    return ccdType
    
def setFilebase(filebase):
    raftsub = CCS.attachSubsystem(subsystem)
    fname = filebase + "_${timestamp}.fits"
    raftsub.synchCommandLine(1000, "setFitsFileNamePattern " + fname)

def setFilename(filebase):
    raftsub = CCS.attachSubsystem(subsystem)
    #fname = prefix + "_CH${sensorId}_" + filebase + "_${timestamp}.fits" #for GREB
    fname = prefix + '_' + filebase + "_${timestamp}.fits" #for WREB
    print "Filename : ",fname
    raftsub.synchCommandLine(1000, "setFitsFileNamePattern " + fname)

def aspicGain(reb, value):
    if verbose: print "Setting ASPIC gain on " + reb
    board = getRaftSubsystem(reb)
    board.synchCommandLine(1000,"setAllAspicGain %d" % value)    
    board.synchCommandLine(1000,"loadAspics true")   
    time.sleep(0.1)

def aspicRC(reb, value):
    if verbose: print "Setting ASPIC RC on " + reb
    board = getRaftSubsystem(reb)
    board.synchCommandLine(1000,"setAllAspicRc %d" % value)    
    board.synchCommandLine(1000,"loadAspics true")   
    time.sleep(0.1)
    
def loadDACS(reb):
    if verbose: print "Loading DACs on " + reb
    board = getRaftSubsystem(reb)
    board.synchCommandLine(1000,"loadDacs true")    
    board.synchCommandLine(1000,"loadBiasDacs true")    
    # result = board.synchCommandLine(1000,"loadAspics true")   
    time.sleep(0.1)

def zeroVolts(reb):  # zeros values in memory, does not load DACs
    biases = getRaftBiases(reb)
    biases.synchCommandLine(1000,"change odP 0" )
    biases.synchCommandLine(1000,"change rdP 0" )
    biases.synchCommandLine(1000,"change gdP 0" )
    biases.synchCommandLine(1000,"change ogP 0" )
    rails = getRaftRails(reb)
    rails.synchCommandLine(1000,"change pclkLowP 0")
    rails.synchCommandLine(1000,"change pclkHighP 0")
    rails.synchCommandLine(1000,"change sclkLowP 0")
    rails.synchCommandLine(1000,"change sclkHighP 0")
    rails.synchCommandLine(1000,"change rgLowP 0")
    rails.synchCommandLine(1000,"change rgHighP 0")

def vsetOD(reb, volts):
    if verbose: print "Setting ", reb, " OD: ", volts
    biases = getRaftBiases(reb)
    volts = volts * OD_gain + OD_offset
    biases.synchCommandLine(1000,"change odP %f" % volts)
    loadDACS(reb)   

def vsetRD(reb, volts):
    if verbose: print "Setting ", reb, " RD: ", volts
    biases = getRaftBiases(reb)
    volts = volts * RD_gain + RD_offset
    biases.synchCommandLine(1000,"change rdP %f" % volts)
    loadDACS(reb)   

def vsetOG(reb, volts):
    if verbose: print "Setting ", reb, " OG: ", volts
    biases = getRaftBiases(reb)
    volts = volts * OG_gain + OG_offset
    biases.synchCommandLine(1000,"change ogP %f" % volts)
    loadDACS(reb)   

def vsetGD(reb, volts):
    if verbose: print "Setting ", reb, " GD: ", volts
    biases = getRaftBiases(reb)
    volts = volts * GD_gain + GD_offset
    biases.synchCommandLine(1000,"change gdP %f" % volts)
    loadDACS(reb)   

def vsetParLo(reb, volts):
    if verbose: print "Setting ", reb, " Parallel low: ", volts
    rails = getRaftRails(reb)
    volts = volts * pLo_gain + pLo_offset
    rails.synchCommandLine(1000,"change pclkLowP %f" % volts)
    loadDACS(reb)
 
def vsetParHi(reb, volts):
    if verbose: print "Setting ", reb, " Parallel high: ", volts
    rails = getRaftRails(reb)
    volts = volts * pHi_gain + pHi_offset
    rails.synchCommandLine(1000,"change pclkHighP %f" % volts)
    loadDACS(reb)
 
def vsetSerLo(reb, volts):
    if verbose: print "Setting ", reb, " Serial low: ", volts
    rails = getRaftRails(reb)
    volts = volts * sLo_gain + sLo_offset
    rails.synchCommandLine(1000,"change sclkLowP %f" % volts)
    loadDACS(reb)
 
def vsetSerHi(reb, volts):
    if verbose: print "Setting ", reb, " Serial high: ", volts
    rails = getRaftRails(reb)
    volts = volts * sHi_gain + sHi_offset
    rails.synchCommandLine(1000,"change sclkHighP %f" % volts)
    loadDACS(reb)
 
def vsetRGLo(reb, volts):
    if verbose: print "Setting ", reb, " RG low: ", volts
    rails = getRaftRails(reb)
    volts = volts * rgLo_gain + rgLo_offset
    rails.synchCommandLine(1000,"change rgLowP %f" % volts)
    loadDACS(reb)

def vsetRGHi(reb, volts):
    if verbose: print "Setting ", reb, " RG high: ", volts
    rails = getRaftRails(reb)
    volts = volts * rgHi_gain + rgHi_offset
    rails.synchCommandLine(1000,"change rgHighP %f" % volts)
    loadDACS(reb)

def ITLdefaults(reb):
    print "Seting default ITL voltages"
#  These are "B" ITL3800 voltages for 098 (ats)- kg 20180808
    vsetParLo(reb,-8.0)
    vsetParHi(reb,+3.0)
    vsetSerLo(reb,-8.0)
    vsetSerHi(reb,+4.0)
    vsetRGLo(reb,-2.0)
    vsetRGHi(reb,+8.0)
    vsetOG(reb,+1.75)
    vsetOD(reb,26.0)
    vsetGD(reb,20.0)
    vsetRD(reb,13.0)


def setSeqStart(reb,main):
    subsys=getRaftSubsystem(reb)
    subsys.synchCommand(10, "setSequencerStart", main)

def setParameterValue(reb, param, value):
    subsys=getRaftSubsystem(reb)
    subsys.synchCommand(10, "setSequencerParameter", param, value)

def startSeq(reb):
    subsys=getRaftSubsystem(reb)
    result = subsys.synchCommand(10, "startSequencer")
    print result.getResult()

def loadSeq(reb, seqfile):
    subsys=getSubsystem()
    result=subsys.synchCommand(20, "loadSequencer", seqfile)
    print result.getResult()

def getSeqParam(name):
    subsys=getSubsystem()
    result=subsys.synchCommand(200, "getSequencerParameter %s", name)
    print result.getResult()
    return result
    
def getBackBiasState(reb):
    if verbose: print "Getting BackBias status...",
    board = getRaftSubsystem(reb)
    result = board.synchCommand(10, "isBackBiasOn ")
    if verbose: print result.getResult()
    return result.getResult()

def setBackBiasOn(reb):
    if verbose: print "setting BackBias On...",
    board = getRaftSubsystem(reb)
    board.synchCommand(10, "setBackBias true")
    time.sleep(3) # allow some settling time
    if verbose: print 'Done.'
    state = getBackBiasState(reb)
    if verbose: print 'Back Bias State = ',state
    return state

def setBackBiasOff(reb):
    if verbose: print "setting BackBias Off...",
    board = getRaftSubsystem(reb)
    board.synchCommand(10, "setBackBias false")
    time.sleep(3) # allow some settling time
    if verbose: print 'Done.'
    state = getBackBiasState(reb)
    if verbose: print 'Back Bias State = ',state
    return state

# functions for acquiring image data

def readoutImage(fname):
    raftsub = CCS.attachSubsystem(subsystem)
    result = raftsub.sendSynchCommand("setFitsFileNamePattern",fname)
    result = raftsub.sendSynchCommand("setSequencerStart","ReadFrame")
    result = raftsub.sendSynchCommand("acquireImage")
    result = raftsub.sendSynchCommand(20,"waitForImage", 10000)
    result = raftsub.sendSynchCommand("saveFitsImage", dataDir)
    print "Saved FITS image to %s/%s" % (dataDir,result[0])
    return result

def acquireBias(filebase):
    print "Acquire Bias: Filebase = ",filebase
    raftsub = CCS.attachSubsystem(subsystem)
    result = raftsub.synchCommandLine(1000,"setSequencerStart Bias")
    print result.getResult()
    raftsub.synchCommandLine(1000,"setSequencerParameter ExposureTime 0")
    setFilename(filebase)
    return acquire(0)

def acquireDark(exptime, filebase):
    print "Acquire Dark:  Time = ", exptime, "   Filebase = ",filebase
    raftsub = CCS.attachSubsystem(subsystem)
    result = raftsub.synchCommandLine(1000,"setSequencerStart Dark")
    print result.getResult()
    raftsub.synchCommandLine(1000,"setSequencerParameter ExposureTime "+("%i" % long(exptime * 1000.0 / 25)))
    setFilename(filebase)
    return acquire(exptime)

def acquireExposure(exptime, filebase):
    print "Acquire Exposure:  Time = ", exptime, "   Filebase = ",filebase
    shutter = CCS.attachSubsystem(bonnshutter)
    result = shutter.sendSynchCommand("takeExposure", exptime)
    result = shutter.sendSynchCommand((int) (exptime+10),"waitForExposure")
    fname = filebase+"_exp_%g_${timestamp}.fits" % exptime
    return readoutImage(fname)    

def clearCCD():
    print "Clearing CCD "
    raftsub = CCS.attachSubsystem(subsystem)
    result = raftsub.synchCommandLine(1000,"setSequencerStart Clear")
    result = raftsub.synchCommandLine(1000,"startSequencer")
    result = raftsub.synchCommandLine(1000,"waitSequencerDone 30000")

def readout():
    print "Readout"
    raftsub = CCS.attachSubsystem(subsystem)
    result = raftsub.synchCommandLine(1000,"setSequencerStart ReadFrame")
    result = raftsub.synchCommandLine(1000,"acquireImage")
    result = raftsub.synchCommandLine(1000,"waitForImage 10000")
    print "Saving FITS image to ", dataDir
    result = raftsub.synchCommand(1000,"saveFitsImage " + dataDir)
    print result.getResult()

# end function definitions #
