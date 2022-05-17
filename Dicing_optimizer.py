import pya
import math as m

def chipInWafer(x0, y0, waferDiameter, slen):
  #Calc wafer radius
  r = waferDiameter/2
  
  #Bottom left corner
  if not inRegion(x0, r):
    return False
  if not inRegion(y0, m.sqrt(r**2 - x0**2)):
    return False  

  #Bottom right corner
  if not inRegion(x0+slen, r):
    return False
  if not inRegion(y0, m.sqrt(r**2 - (x0+slen)**2)):
    return False
  
  #Top left corner
  if not inRegion(y0+slen, m.sqrt(r**2 - x0**2)):
    return False   
  
  #Top right corner
  if not inRegion(y0+slen, m.sqrt(r**2 - (x0+slen)**2)):
    return False
  
  #If we're here then all four corners are within the wafer
  return True

def inRegion (x0, x):
  if x0 < -x or x0 > x:
    return False
  return True
  
#inputs
waferDiameter = 2
chipSideLen = 0.590551
waferOrientation = 100
cutMachine="SAW"

#All units in inches
flats = {2:[0.6259843, 0.314961], 3:[0.8740157, 0.4409449], 4:[1.279528, 0.708661], 6:[2.26378, 1.476378]}
machines = {"SAW": 0, "LASER":1}
areaTotal = m.pi*(waferDiameter/2)**2
chipDiameter = chipSideLen**2
maxChips = m.floor(areaTotal/chipDiameter)
r = waferDiameter/2
dy = min(0.01,chipSideLen / 100)

print("Absolute max chips:  " + str(maxChips))

#Script init
maxCountStepX = 0
maxCountStepY = 0
maxCount = 0

#y sweep
xstep = 0
while xstep < chipSideLen:
  ystep = 0
  
  while ystep < chipSideLen:
    #Horizontal step through wafer
    count = 0
    x = -r-chipSideLen+xstep
    y = -r-chipSideLen+ystep
    while x < r:
      #Vertical step through wafer
      while y < r:
        if chipInWafer(x, y, waferDiameter, chipSideLen):
          count = count+1
      
        y = y + chipSideLen
          
      x = x + chipSideLen
      y = -r - chipSideLen + ystep
  
    if count >= maxCount:
      maxCount = count
      maxCountStepY = ystep
      maxCountStepX = xstep
    ystep = ystep + dy
  xstep = xstep + dy

print("Max found:  " + str(maxCount))
print("Cut x offset:  " + str(-chipSideLen+maxCountStepX))
print("Cut y offset:  " + str(-chipSideLen+maxCountStepY))