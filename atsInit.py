# atsInit.py
# Initialize the ATS camera system
import time
from org.lsst.ccs.scripting import *
from REBlib import *

reb='wreb'

# Setting CCD type does not work yet
# setCCD('ITL')
# ccdtype = getCCD()
# print "CCD type = ",ccdtype

# Configure the ASPICs on the WREB
#aspicGain(reb,1)
#aspicRc(reb,15)

# configure the sequencer
seqfile = '/lsst/ccs/sequences/ats_20180511.seq'
print 'Loading sequencer file ',seqfile
loadSeq(reb,seqfile)

# set the default CCD clock volatges
#print "Make sure Back Bias is off..."
#setBackBiasOff(reb)
#print getBackBiasState(reb)

#ITLdefaults(reb)

#vsetParLo(reb,-8.0)
#vsetParHi(reb,+3.0)
#vsetSerLo(reb,-9.0)
#vsetSerHi(reb,+3.0)
#vsetRGLo(reb,-2.0)
#vsetRGHi(reb,+8.0)
#
#vsetOG(reb,3.0)
#vsetOD(reb,26.0)
#vsetGD(reb,20.0)
#vsetRD(reb,13.0)


print "turn Back Bias on..."
setBackBiasOn(reb)
print getBackBiasState(reb)


