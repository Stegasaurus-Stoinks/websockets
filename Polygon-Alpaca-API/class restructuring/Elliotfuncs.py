import numpy as np

def calculateslope(x1,y1,x2,y2):
        slope = (y2-y1)/(x2-x1)
        return slope

class ElliotImpulse:

    # |              6
    # |         4   /
    # |    2   / \ /
    # |   / \ /   5
    # |  /   3
    # | 1
    # |________________


    def __init__(self, plotSize):

        self.plotSize = plotSize

        self.x1 = np.NaN
        self.y1 = np.NaN
        self.x2 = np.NaN
        self.y2 = np.NaN
        self.x3 = np.NaN
        self.y3 = np.NaN
        self.x4 = np.NaN
        self.y4 = np.NaN
        self.x5 = np.NaN
        self.y5 = np.NaN
        self.x6 = np.NaN
        self.y6 = np.NaN

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

    



    

