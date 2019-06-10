import matplotlib.pyplot as plt
import numpy as np
import math

# Assign default values to arrays
groundLvl = [75,70,67,65,66,24,14,5,31,24,52,70]
solidGroundLvl = [75,45,45,65,66,20,10,5,30,20,50,65]
#groundLvl = [110,81,50,38,36,21,20,21,36,60,96,112]
#solidGroundLvl = [108,80,48,24,12,10,8,9,25,59,95,110]
distance = [0,100,200,300,400,500,600,700,800,900,1000,1100]
surface = 80
water_level = 40



# Predict solid ground level at a certain point assuming straight slope between data points
def getSGLAt(x,interval=100):

    if x % interval != 0:
        prevH = surface

        if x // interval >= 1: prevH = solidGroundLvl[(int)(x//interval) -1]
        nextH = solidGroundLvl[(int)(x//interval)]

        yDiff = prevH - nextH
        return prevH - ((x % interval) / interval * yDiff)


    else:
        return surface - solidGroundLvl[(int)(x/interval)]

# Predict  ground level at a certain point assuming straight slope between data points
def getGLAt(x,interval=100):

    if x % interval != 0:
        prevH = surface

        if x // interval >= 1: prevH = groundLvl[(int)(x//interval) -1]
        nextH = groundLvl[(int)(x//interval)]

        yDiff = prevH - nextH
        return prevH - ((x % interval) / interval * yDiff)


    else:
        return surface - groundLvl[(int)(x/interval)]

# Returns volume of hollow piers given a height
def getPierVolume(height,topW=4,topH=2,thickness=0.3,outerTaper=0.04,innerTaper=0.004):


    volLarge = (topW * (topH + height * outerTaper)) + (topH * (topW + height * outerTaper)) + 2 * (topH * topW + (topH + height * outerTaper) *(topW + height * outerTaper))
    volLarge *= height / 6

    ltW = topW - thickness * 2
    ltH = topH - thickness * 2

    volSmall = (ltW * (ltH + height * innerTaper)) + (ltH * (ltW + height * innerTaper)) + 2 * (ltH * ltW + (ltH + height * innerTaper) *(ltW + height * innerTaper))
    volSmall *= height / 6


    hollowVol = volLarge - volSmall
    return hollowVol


# Plots data points
def plotBridge():
    #groundLvl, solidGroundLvl, distance = manualInput()
    plt.title("Design Data")



    plt.ylabel("Elevation (m)")
    plt.xlabel("Cross section (m)")
    plt.axhline(water_level, color='g')
    plt.axhline(surface, color='b')
    plt.plot(distance,groundLvl, "r")
    plt.grid(which="major")

    plt.plot(distance,solidGroundLvl)
    plt.show()

# Plots costs
def plotCost(costTrend,spanL):
    plt.title("Cost of different span lengths")


    plt.ylabel("Cost (GBP)")
    plt.xlabel("Span (m)")
    plt.grid(which="major")
    for i in range(len(spanL)):
        plt.scatter(spanL[i],costTrend[i])
    #plt.plot(spanL,costTrend)
    plt.show()


# Deck Variables and
tailRatio = 0.8
span = 0
depth = 0
optRatio = 17
length = 1000


# Price Constants
CONCRETE_PRICE = 180

REINF_STEEL = 1300 / 1000
PRESTR_STEEL = 3500 / 1000
SOFFIT_FW = 40
SIDE_FW = 25

PIER_REIN = 180
CAISSONS_DEPTH = 40000
FOOTING = 100000


# Loop variables
minimum = 0
optSp = 0
optDep = 0
optPierCount = 0


# Stores all the costs and spans
cost = []
spanList = []


# Test from 3 piers to 30 piers
for n in range(3,30):

    #Setting up initial properties
    sp = length / ((n-2) + 1.6)
    depth = sp / optRatio
    csa = 7 + depth
    steelRein = length * csa * 80
    preStressCon = length * csa * 50
    soffitFW = 26 * length
    sideFW = 4 * depth * length

    pierCost = n * FOOTING
    concreteCost = csa * length * CONCRETE_PRICE

    # Price of first and last pier
    sgl = getSGLAt(0)
    gl = getGLAt(0)
    pv = getPierVolume(sgl)
    pierCost += PIER_REIN * pv * REINF_STEEL

    sgl = getSGLAt(length)
    gl = getGLAt(length)
    pv = getPierVolume(sgl)
    pierCost += PIER_REIN * pv * REINF_STEEL


    # Price of every piers in between
    for x in range(n-2):
        dist = sp * 0.8 + x * sp
        sgl = getSGLAt(dist)
        gl = getGLAt(dist)
        pv = getPierVolume(sgl)
        if (gl-sgl) > 5: pierCost += (gl-sgl) * CAISSONS_DEPTH
        concreteCost += pv * CONCRETE_PRICE
        pierCost += PIER_REIN * pv * REINF_STEEL

    # Combines all the costs from various souces
    total = REINF_STEEL * steelRein + PRESTR_STEEL * preStressCon + soffitFW * SOFFIT_FW + SIDE_FW * sideFW + pierCost + concreteCost
    cost.append(total)
    spanList.append(sp)

    # Saves the span, pier combination with the minumum cost
    if ((total < minimum) or minimum == 0):
        minimum = total
        optSp = sp
        optDep = depth
        optPierCount = n



print("Lowest Cost: £%d \nOptimal Span = %.2f Optimal Depth = %.2f Pier Count = %d" % (minimum,optSp,optDep,optPierCount))
plotBridge()
plotCost(cost,spanList)
