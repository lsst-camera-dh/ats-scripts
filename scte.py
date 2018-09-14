# eotest.py
from org.lsst.ccs.scripting import *
from REBlib import *

# set this value to the number of photons per second you get
fluence = 2830.0 #e-/pix/second

# serial CTE sweep
Lo_Start = -9.00
Lo_End   = -5.00
Lo_Step  =  0.50
Range_Start = +10.00
Range_End   = +14.00
Range_Step  =  0.50
og_Start = 0.00
og_End   = 4.00
og_Step  = 0.25

imageCount = 1
etimes = [50000.0/float(fluence)]
Lo_Volts = Lo_Start
while (Lo_Volts <= Lo_End):
    Range = Range_Start
    while (Range <= Range_End):
        Hi_Volts = Lo_Volts + Range
        vsetSerLo('w',Lo_Volts)
        vsetSerHi('w',Hi_Volts)
        og_Volts = og_Start
        while (og_Volts <= og_End):
            vsetOG('w',og_Volts)
            for exptime in etimes:
                for i in range(0, imageCount):
                    fbase = ("scte_%05.2f_%05.2f_%05.2f_%03i" % (Lo_Volts, Hi_Volts, og_Volts, i))
                    acquireExposure(exptime, fbase)
            og_Volts = og_Volts + og_Step
        Range = Range + Range_Step
    Lo_Volts = Lo_Volts + Lo_Step
#setDefaults()
print "Serial CTE sweep complete."

