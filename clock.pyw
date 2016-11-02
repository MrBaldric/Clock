#Written by Owen Mulders 2013
from Tkinter import *
from math import *
import thread
import time
locx = '170'
locy = '80'
dimx = '610'
dimy = '610'
window = Tk()
window.resizable(FALSE,FALSE)
window.geometry(dimx + 'x' + dimy + '+' + locx + '+' + locy)
#window.geometry('{}x{}+{}+{}'.format(dimx,dimy,locx,locy))
window.overrideredirect(True)
window.attributes('-alpha', 0.9,'-transparent',True)

displayGaugeValues = {}
inputedGaugeValues = {}

class gauge_round:
    def __init__(self):
        self.panel = Canvas(window, width = dimx, height = dimy, background="#ffffff",highlightcolor= "#ffffff",highlightbackground= "#ffffff" )
        self.gaugeZeroPoint = -90
        self.fullDeflection = 360
    def storeData(self,No,readPV):
        inputedGaugeValues[No] = int(readPV.get())
    def newGauge(self,x,y,gaugeNo,gaugeSize,timeV,dateV):
        self.x = x
        self.y = y
        self.gaugeNo = gaugeNo
        HrVal = displayGaugeValues[1]
        minVal = displayGaugeValues[2]
        secVal = displayGaugeValues[3]
        self.gaugeSize = gaugeSize
        self.timeV = timeV
        self.dateV = dateV
        w = self.gaugeSize * 0.0625 #centre of gauge radius scale
        v = self.gaugeSize - (self.gaugeSize * 0.02)#inside gauge area radius
        radius = self.gaugeSize/2
        self.centreX = (self.x + (self.gaugeSize/2))
        self.centreY = (self.y + (self.gaugeSize/2))
        self.k1 = self.panel.create_oval(self.x, self.y,(self.x + self.gaugeSize),(self.y + self.gaugeSize), fill = "red")
        self.k2 = self.panel.create_oval(self.x + v, self.y + v,((self.x + self.gaugeSize)-v),((self.y + self.gaugeSize)-v), fill = "#FFFFFF")
        self.k3 = self.panel.create_oval(self.centreX - w,self.centreY - w,self.centreX + w,self.centreY + w, fill = "black")
        self.t1 = self.panel.create_text(self.centreX,y + 50, justify = CENTER, text = self.timeV)
        self.d1 = self.panel.create_text(self.centreX,y + 150, justify = CENTER, text = self.dateV)
        self.k4 = self.panel.create_line(self.centreX,self.centreY,self.centreX + ((cos(radians(self.gaugeZeroPoint+(float((float(secVal) / 100) * self.fullDeflection))))) * (radius - 4)),self.centreY + ((sin(radians(self.gaugeZeroPoint+(float((float(secVal) / 100) * self.fullDeflection))))) * (radius - 4)), width = 1, arrow = "last", fill = "black")
        self.k5 = self.panel.create_line(self.centreX,self.centreY,self.centreX + ((cos(radians(self.gaugeZeroPoint+(float((float(minVal) / 100) * self.fullDeflection))))) * (radius - 4)),self.centreY + ((sin(radians(self.gaugeZeroPoint+(float((float(minVal) / 100) * self.fullDeflection))))) * (radius - 4)), width = 4, arrow = "last", fill = "black")
        self.k6 = self.panel.create_line(self.centreX,self.centreY,self.centreX + ((cos(radians(self.gaugeZeroPoint+(float((float(HrVal) / 100) * self.fullDeflection))))) * (radius - 4)),self.centreY + ((sin(radians(self.gaugeZeroPoint+(float((float(HrVal) / 100) * self.fullDeflection))))) * (radius - 4)), width = 4, arrow = "last", fill = "black")
        self.panel.pack()
    def RefreshGauge(self,x,y,gaugeNo,gaugeSize,timeV,dateV):
        self.x = x
        self.y = y
        self.gaugeSize = gaugeSize
        self.centreX = (self.x + (self.gaugeSize/2))
        self.centreY = (self.y + (self.gaugeSize/2))
        HrVal = displayGaugeValues[1]
        minVal = displayGaugeValues[2]
        secVal = displayGaugeValues[3]
        radius = self.gaugeSize/2
        self.timeV = timeV
        self.dateV = dateV
        self.panel.delete(self.k4)
        self.k4 = self.panel.create_line(self.centreX,self.centreY,self.centreX + ((cos(radians(self.gaugeZeroPoint+(float((float(secVal) / 100) * self.fullDeflection))))) * (radius - 4)),self.centreY + ((sin(radians(self.gaugeZeroPoint+(float((float(secVal) / 100) * self.fullDeflection))))) * (radius - 4)), width = 1, arrow = "last", fill = "black")
        self.panel.delete(self.k5)
        self.k5 = self.panel.create_line(self.centreX,self.centreY,self.centreX + ((cos(radians(self.gaugeZeroPoint+(float((float(minVal) / 100) * self.fullDeflection))))) * (radius - 4)),self.centreY + ((sin(radians(self.gaugeZeroPoint+(float((float(minVal) / 100) * self.fullDeflection))))) * (radius - 4)), width = 4, arrow = "last", fill = "black")
        self.panel.delete(self.k6)
        self.k6 = self.panel.create_line(self.centreX,self.centreY,self.centreX + ((cos(radians(self.gaugeZeroPoint+(float((float(HrVal) / 100) * self.fullDeflection))))) * (radius - 4)),self.centreY + ((sin(radians(self.gaugeZeroPoint+(float((float(HrVal) / 100) * self.fullDeflection))))) * (radius - 4)), width = 4, arrow = "last", fill = "black")
        self.panel.delete(self.t1)
        self.t1 = self.panel.create_text(self.centreX,y + 50, justify = CENTER, text = self.timeV)
        self.panel.delete(self.d1)
        self.d1 = self.panel.create_text(self.centreX,y + 150, justify = CENTER, text = self.dateV)
        self.panel.pack()
def gaugeStart():
    a = 5;b = 5; c = 3; d = 600
    gauge1 = gauge_round()
    timeValue = time.strftime("%H:%M:%S",time.localtime((time.time())))
    dateValue = time.strftime("%b %d %Y",time.localtime((time.time())))
    gauge1.newGauge(a,b,c,d,timeValue,dateValue)


    def GauageRefreshFunction():
        loopc = 0
        while loopc < 5:
            HrValue = int(time.strftime("%H",time.localtime((time.time()))))
            minValue = int(time.strftime("%M",time.localtime((time.time()))))
            secValue = int(time.strftime("%S",time.localtime((time.time()))))
            inputedGaugeValues[1] = (HrValue * 0.1) * 83.33333
            inputedGaugeValues[2] = (minValue * 0.1) * 16.67
            inputedGaugeValues[3] = (secValue * 0.1) * 16.67
            time.sleep(0.9)
            if displayGaugeValues[3] != inputedGaugeValues[3]:
                displayGaugeValues[1] = inputedGaugeValues[1]
                displayGaugeValues[2] = inputedGaugeValues[2]
                displayGaugeValues[3] = inputedGaugeValues[3]
                timeValue = time.strftime("%H:%M:%S",time.localtime((time.time())))
                dateValue = time.strftime("%b %d %Y",time.localtime((time.time())))
                gauge1.RefreshGauge(a,b,c,d,timeValue,dateValue)

    thread.start_new_thread(GauageRefreshFunction,(),)
    mainloop()
displayGaugeValues = {1: 0,2: 0, 3: 0}
inputedGaugeValues = {1: 0,2: 0, 3: 0}
gaugeStart()


