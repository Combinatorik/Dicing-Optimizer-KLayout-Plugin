import pya
import math

def chipInWafer(x0, y0, slen, r, xmin, xmax, ymin, ymax):
  #Bottom left corner
  if not inRegion(x0, xmin, xmax):
    return False
  y = math.sqrt(r**2 - x0**2)
  y0min = max(-y, ymin)
  y0max = min(y, ymax)
  if not inRegion(y0, y0min, y0max):
    return False  

  #Top left corner
  if not inRegion(y0+slen, y0min, y0max):
    return False  
    
  #Bottom right corner
  if not inRegion(x0+slen, xmin, xmax):
    return False
  y = math.sqrt(r**2 - (x0+slen)**2)
  y0min = max(-y, ymin)
  y0max = min(y, ymax)
  if not inRegion(y0, y0min, y0max):
    return False 
  
  #Top right corner
  if not inRegion(y0+slen, y0min, y0max):
    return False
  
  #If we're here then all four corners are within the wafer
  return True
  
def chipInWaferLinBound(x0, y0, slen, r, xmin, xmax, m, b):
  #Bottom left corner
  if not inRegion(x0, xmin, xmax):
    return False
  y = math.sqrt(r**2 - x0**2)
  y0min = max(-y, m*x0+b)
  y0max = y
  if not inRegion(y0, y0min, y0max):
    return False  

  #Top left corner
  if not inRegion(y0+slen, y0min, y0max):
    return False  
    
  #Bottom right corner
  if not inRegion(x0+slen, xmin, xmax):
    return False
  y = math.sqrt(r**2 - (x0+slen)**2)
  y0min = max(-y, m*(x0+slen)+b)
  y0max = y
  if not inRegion(y0, y0min, y0max):
    return False 
  
  #Top right corner
  if not inRegion(y0+slen, y0min, y0max):
    return False
  
  #If we're here then all four corners are within the wafer
  return True

def inRegion (x0, minx, maxx):
  if x0 < minx or x0 > maxx:
    return False
  return True

def dicingSawOptimization(waferDiameter, chipSideLen, maxStepSize, flats=[], deg=45):
  #Function init
  dy = min(maxStepSize,chipSideLen / 100)
  maxCountStepX = 0
  maxCountStepY = 0
  maxCount = 0
  r=waferDiameter/2
  xmin=-r
  xmax=r
  ymin=-r
  ymax=r
  m=0
  b=0
  doubleFlatAngled = False
  
  #Adjust boundaries if we have flats to consider
  if len(flats) > 0:
    xmin = -math.sqrt(r**2 - (flats[0]/2)**2)
    
    if len(flats) > 1:
      if deg==45:
        m=-1
        b=-math.sqrt(2*r**2 - (flats[1]**2)/2)
        doubleFlatAngled = True
      elif deg==90:
        ymin=-math.sqrt(r**2 - (flats[1]/2)**2)
      elif deg==135:
        m=1
        b=-math.sqrt(2*r**2 - (flats[1]**2)/2)
        doubleFlatAngled = True
      elif deg==180:
        xmax = math.sqrt(r**2 - (flats[1]/2)**2)
      else:
        raise NameError('Invalid second flat angle')
     
     
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
      while x < xmax:
        #Vertical step through wafer
        while y < r:
          if not doubleFlatAngled and chipInWafer(x, y, chipSideLen, r, xmin, xmax, ymin, ymax):
              count = count + 1
          elif chipInWaferLinBound(x, y, chipSideLen, r, xmin, xmax, m, b):
            count = count + 1
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
  #Function init
  dy = min(maxStepSize,chipSideLen / 100)
  maxCountStepX = 0
  maxCountStepY = 0
  maxCount = 0
  r=waferDiameter/2
  
  #x sweep
  xstep = 0
  while xstep < chipSideLen:
    count = 0
    x = -r-chipSideLen+xstep
    while x < r:
      colCount, colStep = optimizeColumn(waferDiameter/2, chipSideLen, x, 0) 
      count = count + colCount      
      x = x + chipSideLen
    
    if count >= maxCount:
      maxCount = count
      maxCountStepX = xstep
    xstep = xstep + dy
    
  return maxCount, maxCountStepX, maxCountStepY
  
def optimizeColumn(r, chipSideLen, x0, ystep):
  if inRegion(x0, -r, r) and inRegion(x0 + chipSideLen, -r, r):
    y=min(math.sqrt(r**2 - x0**2), math.sqrt(r**2 - (x0 + chipSideLen)**2))
    return math.floor(2*y/chipSideLen), (ystep + chipSideLen/2)
  return 0, 0
  
#inputs
waferDiameter = 51
chipSideLen = 5
dicingSawWidth = 0.025
cutMachine="SAW"

#All units in mm
flats = {25:[], 51:[15.88, 8], 76:[22.22, 11.18], 100:[32.5, 18], 125:[42.5, 27.5], 130:[], 150:[57.5, 37.5], 200:[], 300:[], 450:[]}
machines = {"SAW": 0, "LASER":1}

#Max chip count calculation
areaTotal = math.pi*(waferDiameter/2)**2
chipDiameter = chipSideLen**2
maxChips = math.floor(areaTotal/chipDiameter)
print("Absolute max chips:  " + str(maxChips))
fs = flats[waferDiameter]

if cutMachine == "SAW":
  maxCount, maxCountStepX, maxCountStepY = dicingSawOptimization(waferDiameter, chipSideLen+dicingSawWidth, 1, fs, 90)
else:
  maxCount, maxCountStepX, maxCountStepY = laserOptimization(waferDiameter, chipSideLen, 1)

print("Max found:  " + str(maxCount))
print("Cut x offset:  " + str(-chipSideLen+maxCountStepX))
print("Cut y offset:  " + str(-chipSideLen+maxCountStepY))
print(str(round(100*maxCount/maxChips)) + "% yield")