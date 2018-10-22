# eotest.py
from org.lsst.ccs.scripting import *
from REBlib import *

# set this value to the number of photons per second you get
fluence = 2830.0 #e-/pix/second

# serial CTE sweep
Lo_Start = -9.00
Lo_Count = 7
Lo_Step = 0.50
Range_Start = +9.00
Range_Count = 5
Range_Step = 0.50
og_sup_Start = -2
og_sup_Count = 5
og_sup_Step = 0.5

Par_Lo_Start = -9.5
Par_Lo_Count = 4
Par_Lo_Step = 0.5
Par_Swing_Start = 10
Par_Swing_Count = 3
Par_Swing_Step = 0.5


odometer = 1
imageCount = 1
etimes = [0,50000.0/float(fluence)]
# setDefaults()

for iLo in range(Lo_Count):
    Lo_Volts = Lo_Start + Lo_Step * iLo
    for iRange in range(Range_Count):
        Range = Range_Start + Range_Step * iRange
        Hi_Volts = Lo_Volts+Range
        vsetSerLo('w',Lo_Volts)
        vsetSerHi('w',Hi_Volts)
        # loop on difference between serial up and og
        for iog in range(og_sup_Count):
            og_sup = og_sup_Start + og_sup_Step * iog
            og_Volts = Hi_Volts + og_sup
            if og_Volts >= 5 : continue
            vsetOG('w',og_Volts)
            Par_Lo_Volts = Par_Lo_Start
            for iPar in range(Par_Lo_Count):
                Par_Lo_Volts = Par_Lo_Start + Par_Lo_Step * iPar
                # check that charges can flow into the serial register :
                if Par_Lo_Volts > Lo_Volts -0.9 : continue
                vsetParLo('w', Par_Lo_Volts)
                for iSwing in range(Par_Swing_Count):
                    Par_Swing = Par_Swing_Start + Par_Swing_Step * iSwing
                    Par_Hi = Par_Lo_Volts + Par_Swing
                    # check that charges can flow into the serial register :
                    if Par_Hi > Hi_Volts -0.9 : continue
                    vsetParHi('w', Par_Hi)
                    for c,exptime in enumerate(etimes):
                        for i in range(0, imageCount):
                            # 05.2f_%05.2f_%05.2f_%03i" % (Lo_Volts, Hi_Volts, og_Volts, i))
                            fbase = "scte_%04d_%1d"%(odometer,c)
                            odometer += 1
                            acquireExposure(exptime, fbase)
                            print fbase
# setDefaults()
print "Serial CTE sweep complete."

