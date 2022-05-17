import pya
import math as m

def chipInWafer(x0, y0, r, slen):
  #Calc wafer radius
  
  #Bottom left corner
  if not inRegion(x0, r):
    return False
  y = m.sqrt(r**2 - x0**2)
  if not inRegion(y0, y):
    return False  

  #Top left corner
  if not inRegion(y0+slen, y):
    return False  
    
  #Bottom right corner
  if not inRegion(x0+slen, r):
    return False
  y = m.sqrt(r**2 - (x0+slen)**2)
  if not inRegion(y0, y):
    return False 
  
  #Top right corner
  if not inRegion(y0+slen, y):
    return False
  
  #If we're here then all four corners are within the wafer
  return True

def inRegion (x0, x):
  if x0 < -x or x0 > x:
    return False
  return True

def dicingSawOptimization(waferDiameter, chipSideLen, maxStepSize, flats=[], deg=45):
  #Function init
  dy = min(maxStepSize,chipSideLen / 100)
  print(dy)
  maxCountStepX = 0
  maxCountStepY = 0
  maxCount = 0
  r=waferDiameter/2
  
  #x sweep
  xstep = 0
  while xstep < chipSideLen:
    ystep = 0
    
    #y sweep
    while ystep < chipSideLen:
      #Horizontal step through wafer
      count = 0
      x = -r-chipSideLen+xstep
      y = -r-chipSideLen+ystep
      while x < r:
        #Vertical step through wafer
        while y < r:
          if chipInWafer(x, y, r, chipSideLen):
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
    
  return maxCount, maxCountStepX, maxCountStepY

def laserOptimization(waferDiameter, chipSideLen, maxStepSize, flats=[]):
  return 0, 0, 0
  
#inputs
waferDiameter = 51
chipSideLen = 10
cutMachine="SAW"

#All units in mm
flats = {25:[], 51:[15.88, 8], 76:[22.22, 11.18], 100:[32.5, 18], 125:[42.5, 27.5], 130:[], 150:[57.5, 37.5], 200:[], 300:[], 450:[]}
machines = {"SAW": 0, "LASER":1}

#Max chip count calculation
areaTotal = m.pi*(waferDiameter/2)**2
chipDiameter = chipSideLen**2
maxChips = m.floor(areaTotal/chipDiameter)
print("Absolute max chips:  " + str(maxChips))

if cutMachine == "SAW":
  maxCount, maxCountStepX, maxCountStepY = dicingSawOptimization(waferDiameter, chipSideLen, 0.1)
else:
  maxCount, maxCountStepX, maxCountStepY = laserOptimization(waferDiameter, chipSideLen, 0.1)

print("Max found:  " + str(maxCount))
print("Cut x offset:  " + str(-chipSideLen+maxCountStepX))
print("Cut y offset:  " + str(-chipSideLen+maxCountStepY))
print(str(100*maxCount/maxChips) + "% yield")