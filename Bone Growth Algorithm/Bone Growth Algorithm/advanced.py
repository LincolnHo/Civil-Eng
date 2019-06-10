import numpy as np
import math
import sys


class BGAlgorithm:

    def __init__(self, b, d, d_Dimension, eT, eC,ratio,stress,count):
        self.b = b
        self.d = d
        self.d_Dimension = d_Dimension
        self.eT = eT
        self.eC = eC
        self.stress = stress
        self.count = count


        self.totalArea = self.b * self.d
        self.blockArea = self.d_Dimension ** 2


        self.setNewDimensions(ratio)

    def translateAlgorithm(self):
        condition = 0
        failed = []
        while(condition < self.count):
            condition += 1
            tries = 1
            unstable = True

            self.updateProperties()

            legalShape = np.copy(self.curShape)

            while unstable:

                #perform checks
                #if failed add to list of failed y values
                #perform backtrack
                print("Run No.", condition, "Tries:", tries)
                curMax = self.returnMaxStress(condition % 4)
                curMin = self.returnMinStress(failed)
                self.fillAnEmptySquareAround(curMax,curMin)

                self.updateProperties()
                if self.isBlockMovable(curMin[1]):
                    unstable = False
                else:
                    tries +=1
                    failed.append(curMin[1])
                    self.curShape = np.copy(legalShape)


            #align to centre
            self.curShape = self.centreAlignment()

            print(self.curShape)
            #print(self.n_axis)

            print("\n")



    def fillAnEmptySquareAround(self,maxS,minS):

        for rx in range(-1,2):
            for ry in range(-1,2):
                if bool(rx == 0) != bool(ry == 0):
                    if ((maxS[0]+rx <self.curShape.shape[1]) and maxS[0]+rx >= 0) and ((maxS[1]+ry <self.curShape.shape[0]) and maxS[1]+ry >= 0):

                        if self.curShape[maxS[1]+ry][maxS[0]+rx] == 0:

                            self.curShape[maxS[1]+ry][maxS[0]+rx] = 1
                            self.curShape[minS[1]][minS[0]] = 0
                            print("(" + str(minS[0]) + "," + str(minS[1]) + ") moved to " + "(" + str(maxS[0]+rx) + "," + str(maxS[1]+ry) + ")")
                            return


    def setNewDimensions(self,ratio):
        width = self.b
        height = self.d
        nw = 0
        nh = 0

        if ((math.floor(ratio*width) - width) % 2 == 0):
            nw = math.floor(ratio*width)
        else:
            nw = math.ceil(ratio*width)


        if ((math.floor(ratio*height) - height) % 2 == 0):
            nh = math.floor(ratio*height)
        else:
            nh = math.ceil(ratio*height)


        wDiff = nw - width
        hDiff = nh - height


        if wDiff < 2 :
            nw = 2 + width
            wDiff = 2
        if hDiff < 2:
            nh = 2 + height
            hDiff = 2




        self.curShape = np.zeros([nh,nw],dtype = int)
        for x in range(self.b):
            for y in range(self.d):
                self.curShape[int(y+ hDiff/2)][int(x + wDiff/2)] = 1

        self.newShape = np.copy(self.curShape)
    def updateProperties(self):
        self.n_axis = self.returnNeutralAxis()
        self.sma  = self.returnSecondMomentofA()

    def returnNeutralAxis(self):
        sum1=0
        for x in range (0,self.curShape.shape[1]):
            for y in range (0,self.curShape.shape[0]):
                if self.curShape[y][x] == 1:
                    result1=self.blockArea*((y)+0.5)
                    sum1 +=result1
        n_axis=sum1/self.totalArea
        return n_axis

    def returnMaxStress(self,count):
        start = (0,0)
        end = (0,0)
        step = (0,0)
        if count == 0:
            start = (0,0)
            end = (self.curShape.shape[1],self.curShape.shape[0])
            step = (1,1)
        elif count == 1:
            start = (self.curShape.shape[1]-1,0)
            end = (-1,self.curShape.shape[0])
            step = (-1,1)
        elif count == 2:
            start = (0,self.curShape.shape[0] -1)
            end = (self.curShape.shape[1],-1)
            step = (1,-1)
        elif count == 3:
            start = (self.curShape.shape[1] -1,self.curShape.shape[0] -1)
            end = (-1,-1)
            step = (-1,-1)



        maxPos = (0,0)
        maxStress = -100000
        for x in range(start[0],end[0],step[0]):
            for y in range(start[1],end[1],step[1]):
                if self.curShape[y][x] == 1 and self.isBlockFree(x,y):
                    stress = math.fabs(((y+0.5) - self.n_axis) / self.sma)
                    if stress > maxStress:
                        maxStress = stress
                        maxPos = (x,y)
        return maxPos


    ### Check if adjacent blocks are zeros
    def isBlockFree(self,x,y):
        if (x-1 < 0):
            if (y-1 < 0):
                return self.curShape[y][x+1] == 0 or self.curShape[y+1][x] == 0
            elif (y+1 > self.curShape.shape[0]-1):
                return self.curShape[y][x+1] == 0 or self.curShape[y-1][x] == 0
            else:
                return self.curShape[y][x+1] == 0 or self.curShape[y-1][x] == 0 or self.curShape[y+1][x] == 0
        elif (x+1 > self.curShape.shape[1]-1):
            if (y-1 < 0):
                return self.curShape[y][x-1] == 0 or self.curShape[y+1][x] == 0
            elif (y+1 > self.curShape.shape[0]-1):
                return self.curShape[y][x-1] == 0 or self.curShape[y-1][x] == 0
            else:
                return self.curShape[y][x-1] == 0 or self.curShape[y-1][x] == 0 or self.curShape[y+1][x] == 0
        elif (y-1 < 0):
            if (x-1 < 0):
                return self.curShape[y][x+1] == 0 or self.curShape[y+1][x] == 0
            elif (x+1 > self.curShape.shape[1]-1):
                return self.curShape[y][x-1] == 0 or self.curShape[y+1][x] == 0
            else:
                return self.curShape[y][x-1] == 0 or self.curShape[y+1][x] == 0 or self.curShape[y][x+1] == 0
        elif (y+1 > self.curShape.shape[0]-1):
            if (x-1 < 0):
                return self.curShape[y-1][x] == 0 or self.curShape[x+1][x] == 0
            elif (x+1 > self.curShape.shape[1]-1):
                return self.curShape[y][x-1] == 0 or self.curShape[y-1][x] == 0
            else:
                return self.curShape[y][x+1] == 0 or self.curShape[y-1][x] == 0 or self.curShape[y][x-1] == 0
        else:
            return self.curShape[y-1][x] == 0 or self.curShape[y+1][x] == 0 or self.curShape[y][x-1] == 0 or self.curShape[y][x+1] == 0

        #if (x==1) and y ==2:
        #print(self.curShape[x-1][y],self.curShape[x+1][y], self.curShape[x][y-1],self.curShape[x][y+1])

    def returnMinStress(self,failed):
        minPos = (0,0)
        minStress = 100000
        for x in range(0,self.curShape.shape[1]):
            for y in range(0,self.curShape.shape[0]):
                if self.curShape[y][x] == 1 and y not in failed:
                    stress = math.fabs(((y+0.5) - self.n_axis) / self.sma)
                    if stress <= minStress:
                        minStress = stress
                        minPos = (x,y)
        return minPos



    ### Check if block can be moved
    def isBlockMovable(self,y):
        start = 0
        end = 0
        thickness = 0
        if y < self.n_axis:
            start = 0
            end = y + 1
        else:
            start = y
            end = self.curShape.shape[0]

        areaBelow = 0
        count = 0
        for i in range(start,end):
            for j in range(0,self.curShape.shape[1]):
                if(self.curShape[i][j] == 1):areaBelow += self.blockArea

        areaTimesNA = areaBelow * (self.n_axis - (self.curShape.shape[0] - self.d) /2)


        distSum = 0
        for i in range(start,end):
            for j in range(0,self.curShape.shape[1]):
                if(self.curShape[i][j] == 1):
                    #distance from n_axis to centroid of individual blocks
                    distSum += self.blockArea  * (math.fabs(i - self.n_axis+0.5))


        for i in range (0,self.curShape.shape[1]):
            if self.curShape[y][i] == 1: thickness += 1

        if thickness == 0: return False
        #replace with thickness later
        result = (areaTimesNA - distSum) / thickness
        '''
        print("Partial Area", areaBelow)
        print("N_Axis",self.n_axis)
        print("AZc", areaTimesNA - distSum)
        print("areaTimesNA",areaTimesNA)
        print("distSum", distSum)
        print("SMA", self.sma)
        print("Thickness", thickness)
        print("Shear Stress", result)
        '''

        if result < self.stress:
            return True
        else:
            return False

    def returnSecondMomentofA(self):
        sumResult = 0
        for x in range(0,self.curShape.shape[1]):
            for y in range(0,self.curShape.shape[0]):
                if self.curShape[y][x] == 1:
                    newTempArea = self.blockArea
                    if y < self.n_axis:
                        newTempArea = self.blockArea / (self.eC / self.eT)
                    num1 = newTempArea*((y+0.5) - self.n_axis)**2
                    num2 = (newTempArea**3/12)
                    sumResult += num1 + num2
        return sumResult

    def centreAlignment(self):
        result = np.copy(self.curShape)
        for row in range(result.shape[0]):
            zeroCount = 0
            rowNums = []
            for col in range(result.shape[1]):
                if result[row][col] == 0:
                    zeroCount += 1
                rowNums.append(result[row][col])
            rowNums = sorted(rowNums)
            for i in range(zeroCount//2):
                temp = rowNums.pop(0)
                rowNums.append(temp)

            for col in range(result.shape[1]):

                result[row][col] = rowNums[col]

        return result


bgBlock = BGAlgorithm(20,20,1,57.5,43.3,1.2,70,int(sys.argv[1]))
bgBlock.translateAlgorithm()
