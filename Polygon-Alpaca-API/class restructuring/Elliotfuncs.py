import numpy as np

def calculateslope(x1,y1,x2,y2):
        slope = (y2-y1)/(x2-x1)
        return slope

def displaywaves(possibleWaves, array = []):
    wavesfordisplay = []
    print(array)
    if array == []:
        for wave in possibleWaves:
            waveplot = wave.assemble()
            wavesfordisplay.append(waveplot)

    else:
        for i in array:
            print(i)
            waveplot = possibleWaves[i].assemble()
            #print(waveplot)
            wavesfordisplay.append(waveplot)

    return wavesfordisplay
            

class ElliotImpulse:

    # |              6
    # |         4   /
    # |    2   / \ /
    # |   / \ /   5 
    # |  /   3
    # | 1
    # |________________


    def __init__(self, plotSize,x1= np.NaN,y1= np.NaN,x2= np.NaN,y2= np.NaN,x3= np.NaN,y3= np.NaN,x4= np.NaN,y4= np.NaN,x5= np.NaN,y5= np.NaN,x6= np.NaN,y6= np.NaN):

        self.plotSize = plotSize

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.x4 = x4
        self.y4 = y4
        self.x5 = x5
        self.y5 = y5 
        self.x6 = x6
        self.y6 = y6

    def printdata(self):
        print(self.x1,self.y1,self.x2,self.y2,self.x3,self.y3,self.x4,self.y4,self.x5,self.y5,self.x6,self.y6)

    def assemble(self,print=False):
        #calculate slopes between each line and create a plotable line

        #check to see if all the values have been defined
        #NEED TO CHANGE THIS TO TRIGGER ON BEING NANS IF I WANT IT TO WORK?
        if(self.y1 == 0 or self.y2 == 0 or self.y3 == 0 or self.y4 == 0 or self.y5 == 0 or self.y5 == 0):
            print("Error! Could not assemble the Elliot wave due to missing/undefined data")
            print("Y1:{} Y2:{} Y3:{} Y4:{} Y5:{} Y6:{}".format(self.y1,self.y2,self.y3,self.y4,self.y5,self.y6))
            return()

        if(print):
            print("Assembling the Elliot wave with the given parameters")
            self.printdata()

        self.slope1 = calculateslope(self.x1, self.y1, self.x2, self.y2)
        self.slope2 = calculateslope(self.x2, self.y2, self.x3, self.y3)
        self.slope3 = calculateslope(self.x3, self.y3, self.x4, self.y4)
        self.slope4 = calculateslope(self.x4, self.y4, self.x5, self.y5)
        self.slope5 = calculateslope(self.x5, self.y5, self.x6, self.y6)

        #print(self.slope1,self.slope2,self.slope3,self.slope4,self.slope5)
        wave = [np.NaN] * self.plotSize
        try:
            x = 0
            for k in range(self.x1, self.x2+1):
                wave[k] = float(x*self.slope1) + self.y1
                x += 1

            x = 0
            for k in range(self.x2, self.x3+1):
                wave[k] = float(x*self.slope2) + self.y2
                x += 1

            x = 0
            for k in range(self.x3, self.x4+1):
                wave[k] = float(x*self.slope3) + self.y3
                x += 1

            x = 0
            for k in range(self.x4, self.x5+1):
                wave[k] = float(x*self.slope4) + self.y4
                x += 1

            x = 0
            for k in range(self.x5, self.x6+1):
                wave[k] = float(x*self.slope5) + self.y5
                x += 1
        except:
            return(wave)

        return(wave)


    def checkpoint3(self,x3,y3):
        #add rules and conditions that would make this point work in the elliot wave
        if x3>self.x2 and y3>self.y1:
            return True

        else:
            return False

    def checkpoint4(self,x4,y4):
        #add rules and conditions that would make this point work in the elliot wave
        if x4>self.x3 and y4>self.y2:
            return True

        else:
            return False

    def checkpoint5(self,x5,y5):
        #add rules and conditions that would make this point work in the elliot wave
        if x5>self.x4 and y5>self.y3:
            return True

        else:
            return False

    def checkpoint6(self,x6,y6):
        #add rules and conditions that would make this point work in the elliot wave
        if x6>self.x5 and y6>self.y4:
            return True

        else:
            return False


    def definepoints(self,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.x4 = x4
        self.y4 = y4
        self.x5 = x5
        self.y5 = y5
        self.x6 = x6
        self.y6 = y6

        
    def score():
        print("Give the Elliot Wave a score of certainty based on how many rules it followed")

    



    

############ Big boy function. father of all functions. Tamper with if you dare. A single wrong change will cause a cataclysmic chain of events

def elliotRecursiveBlast(backtest,plotSize):
    #Calculating mins and maxs
    n = 20 #Adjust this to add more or less mins and maxs (2 was the best one I found for short term)
    ilocs_min = argrelextrema(backtest.low.values, np.less_equal, order=n)[0]
    ilocs_max = argrelextrema(backtest.high.values, np.greater_equal, order=n)[0]

    #print(ilocs_min)
    #print(ilocs_max)

    #array of min and max plotpoints
    #fill array with nan's first, then replace nan's with min and max values where necessary
    mins = [np.NaN] * plotSize
    for i in range (0,len(ilocs_min)):
        mins[ilocs_min[i]] = backtest.iloc[ilocs_min[i]].low * 0.999

    maxs = [np.NaN] * plotSize
    for i in range (0,len(ilocs_max)):
        maxs[ilocs_max[i]] = backtest.iloc[ilocs_max[i]].high * 1.001

    #---------------Now I just need to find these points automatically----------------

    #wave = Elliotfuncs.ElliotImpulse(plotSize)
    #wave.definepoints(x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6)
    #wave.printdata()
    #waveplot = wave.assemble()
    #print(waveplot)
    #extraplots.append(plotting.make_addplot(waveplot,ax=ax1))

    #-----------------------------------------------------------------------------------

    reach = 2
    possibleWaves = []
    counter = 0

    #for every min in chart
    for i in range (0,len(ilocs_min)):
        if(1):
        #try:
            wave = Elliotfuncs.ElliotImpulse(plotSize)
            wave.x1 = ilocs_min[i]
            wave.y1 = mins[ilocs_min[i]]

            if(endX != np.NaN):
                ilocs_max_valid = [x for x in ilocs_max if (x>wave.x1 and x<endX)]#max's in wave 1
            else:    
                ilocs_max_valid = [x for x in ilocs_max if x>wave.x1]#all max's past point 1

            #print(wave.x1, ilocs_max_valid)
            maxval2 = wave.y1
            for x in ilocs_max_valid[0:reach+1]:
                if(maxs[x] > maxval2):
                    maxval2 = maxs[x]
                    wave.x2 = x
                    wave.y2 = maxs[x]
                    

                    ilocs_min_valid = [x for x in ilocs_min if x>wave.x2]

                    minval3 = wave.y2
                    for x in ilocs_min_valid[0:reach+1]:
                        if(wave.checkpoint3(x,mins[x])):
                            if(mins[x] < minval3):
                                minval3 = mins[x]
                                wave.x3 = x
                                wave.y3 = mins[x]

                                ilocs_max_valid = [x for x in ilocs_max if x>wave.x3]
                            
                                maxval4 = wave.y3
                                for x in ilocs_max_valid[0:reach+1]:

                                    if(wave.checkpoint4(x,maxs[x])):
                                        if(maxs[x] > maxval4):
                                            maxval4 = maxs[x]
                                            wave.x4 = x
                                            wave.y4 = maxs[x]
                                            #print("found valid 4")

                                            ilocs_min_valid = [x for x in ilocs_min if x>wave.x4]

                                            minval5 = wave.y4
                                            for x in ilocs_min_valid[0:reach+1]:
                                                if(wave.checkpoint5(x,mins[x])):
                                                    if(mins[x] < minval5):
                                                        minval5 = mins[x]
                                                        wave.x5 = x
                                                        wave.y5 = mins[x]
                                                        #print("found valid 5")

                                                        ilocs_max_valid = [x for x in ilocs_max if x>wave.x5]

                                                        maxval6 = wave.y5
                                                        for x in ilocs_max_valid[0:reach+1]:

                                                            if(wave.checkpoint6(x,maxs[x])):
                                                                if(maxs[x] > maxval6):
                                                                    maxval6 = maxs[x]
                                                                    wave.x6 = x
                                                                    wave.y6 = maxs[x]
                                                                    #print("found valid 6")
                                                                    
                                                                    possibleWaves.append(wave)
                                                                    possWaves1 = elliotRecursiveBlast()
                                                                    possibleWaves.append(possWaves1)
                                                                    counter += 1
                                                                    #waveplot = wave.assemble()
                                                                    #print(wave.printdata())
                                                                    #print(waveplot)
                                                                    #extraplots.append(plotting.make_addplot(waveplot,ax=ax1))        
            
        else:
        #except:       
            print("something broke in the try thingy")
        return
